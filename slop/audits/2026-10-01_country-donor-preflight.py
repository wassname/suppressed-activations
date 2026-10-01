"""Prospective country facts/rendering/tokenization, no model inference. — PI/OpenAI"""
import json
from pathlib import Path
from transformers import AutoTokenizer

donor=json.loads(Path('data/sweden_japan_donors_chat_v1.json').read_text())
data=json.loads(Path('data/sweden_japan_joint_chat_v1.json').read_text())
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
assert donor['concepts']==['Sweden','Japan']
records=[]
for user in [t.format(concept=c) for c in donor['concepts'] for t in donor['templates']]+[c['user_content'] for c in data['cases']]:
    messages=[{'role':'system','content':donor['system']},{'role':'user','content':user}]
    rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
    ids=tok(rendered,add_special_tokens=False).input_ids
    assert ids==tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,enable_thinking=False,return_dict=False)
    records.append({'user':user,'rendered':rendered,'token_ids':ids})
values=[' Sweden',' Japan','Stockholm','Tokyo','SEK','JPY','4','even']
tokens={v:tok(v,add_special_tokens=False).input_ids for v in values}
assert len(tokens[' Sweden'])==len(tokens[' Japan'])==1
assert tokens['Stockholm'][0]!=tokens['Tokyo'][0]
assert all(c not in s for c in donor['concepts'] for s in [r['user_content'] for r in data['cases']])
assert all(not any(v in r['user'] for v in ('Gothenburg','Osaka','Stockholm','Tokyo','SEK','JPY')) for r in records[:8])
result={'signature':'PI/OpenAI','no_inference':True,'rendering':records,'tokenizations':tokens,
        'probability_scope':'first-token probabilities only; full continuations establish capitals/codes'}
Path('slop/audits/2026-10-01_country-donor-tokenization.json').write_text(json.dumps(result,ensure_ascii=False,indent=1))
print(json.dumps(tokens,ensure_ascii=False),flush=True)
print('PASS eight generic and three evaluation renders; source/target names only in preparation; city/code strings absent from preparation; distinct capital first IDs. No model inference. — PI/OpenAI',flush=True)
