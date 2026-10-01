"""Corpus selection, name-spill fixtures and fixed prefix IDs; no inference. — PI/OpenAI"""
import ast
from collections import OrderedDict
import csv
import hashlib
import json
from pathlib import Path
import re

from transformers import AutoTokenizer

root=Path.cwd();data=json.loads((root/'data/english_person_pairs_chat_v1.json').read_text())
source=root/data['source_dataset'];assert hashlib.sha256(source.read_bytes()).hexdigest()==data['source_dataset_sha256']
rows=list(csv.DictReader(source.open()));groups=OrderedDict()
for i,r in enumerate(rows):
    if r['category']=='novel-author-birthcntry':groups.setdefault(r['e3.value'],OrderedDict()).setdefault(r['e2.value'],(i,r))
selected=[item for _,authors in [(k,v) for k,v in groups.items() if len(v)>=2][:2] for item in list(authors.values())[:2]]
assert [i for i,_ in selected]==[c['source_row'] for c in data['cases']]
for (i,r),c in zip(selected,data['cases'],strict=True):
    assert c['source_uid']==r['uid'] and c['concept']==r['e2.value']
    assert c['answer']=={'India':'India', "People's Republic of China":'China'}[r['e3.value']]
    assert c['prompt']=='Complete the fact with only the missing country name. Use present-day country names:\nFact: '+r['r2(r1(e1)).prompt']
    assert c['concept'].casefold() not in c['prompt'].casefold()
    assert len(c['hidden_aliases'])==len(c['hidden_alias_min_chars'])
source08=ast.parse((root/'scripts/english/08_jlens_one_pass.py').read_text())
statement=next(n for n in ast.walk(source08) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='hidden_is_said' for t in n.targets))
code=compile(ast.Expression(statement.value),'production hidden_is_said','eval')
def said(text,aliases):
    return eval(code,{'hidden_aliases':aliases,'actual_words':sorted(set(re.findall(r'[^\W_]+',text.lower())))})
for c,surname,fragment in zip(data['cases'],['Orwell','Rushdie','Cao','Wu'],['Orw','Rush','Ca','W'],strict=True):
    assert said('The author is '+c['concept']+'.',c['hidden_aliases'])
    assert said(c['concept'].upper(),c['hidden_aliases']) and said(surname,c['hidden_aliases'])
    assert not said(fragment,c['hidden_aliases']) and not said(c['answer'],c['hidden_aliases'])
    assert not said(c['concept'],[c['concept']])
print('PASS corpus selection and all four full-name/surname/fragment fixtures; full-name-only limitation reproduced, not fixed.',flush=True)
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
vocab=[tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(248320)))]
qsource=ast.parse((root/'scripts/english/01_detector_baselines_and_pair_transfer.py').read_text())
fn=next(n for n in qsource.body if isinstance(n,ast.FunctionDef) and n.name=='is_prefix_hit')
ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'production prefix matcher','exec'),ns)
labels=[]
for c in data['cases']:
    ids=sorted({i for alias,minimum in zip(c['hidden_aliases'],c['hidden_alias_min_chars'],strict=True) for i,t in enumerate(vocab) if ns['is_prefix_hit'](t,alias,minimum)})
    labels.append({'concept':c['concept'],'ids':ids,'tokens':[vocab[i] for i in ids],'scorable':bool(ids)})
    print(c['concept'],len(ids),'eligible prefix IDs',flush=True)
    messages=[{'role':'user','content':c['prompt']}]
    rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
    assert tok(rendered,add_special_tokens=False).input_ids==tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,enable_thinking=False,return_dict=False)
result={'signature':'PI/OpenAI','data_sha256':hashlib.sha256((root/'data/english_person_pairs_chat_v1.json').read_bytes()).hexdigest(),
 'selection_rows':[i for i,_ in selected],'full_name_only_limitation_reproduced':True,'cases':labels,
 'pair_ambiguous_ids':[sorted(set(labels[i]['ids'])&set(labels[i+1]['ids'])) for i in (0,2)],
 'scope':'Evaluation-only prefix IDs; surname/fragment matches are not automatically full person identification. No generated outputs observed.'}
(root/'slop/audits/2026-10-01_person-pairs-labels.json').write_text(json.dumps(result,ensure_ascii=False,indent=1))
print('PASS exact native rendering; labels saved before inference. — PI/OpenAI',flush=True)
