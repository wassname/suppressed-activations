"""Pre-outcome dataset/guard checks only; no model inference. -- PI/OpenAI"""
import ast
import json
from pathlib import Path
import re

from tokenizers import Tokenizer

path=Path('data/english_hidden_words_v5_matched_output.json')
data=json.loads(path.read_text())
tok=Tokenizer.from_file('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json')
vocab=[tok.decode([i],skip_special_tokens=False).strip().lower() for i in range(tok.get_vocab_size())]
def labels(word):
    return {i for i,t in enumerate(vocab) if len(t)>=min(3,len(word)) and word.lower().startswith(t)}
assert len(data['cases'])==8 and sorted(i for p in data['pairs'] for i in p['case_indices'])==list(range(8))
for pair in data['pairs']:
    a,b=[data['cases'][i] for i in pair['case_indices']]
    assert a['answer']==b['answer']==pair['expected_answer'] and a['concept']!=b['concept']
for c in data['cases']:
    prompt=data['prefix']+c['prompt'];h=labels(c['concept']);s=labels(c['answer'])
    assert h and s and not h&s
    assert not re.search(r'\b'+re.escape(c['concept'])+r'\b',prompt,re.I)
    assert not re.search(r'\b'+re.escape(c['answer'])+r'\b',prompt,re.I)
    assert prompt.endswith(' is') and not prompt.endswith(' ')
    print(json.dumps({'concept':c['concept'],'answer':c['answer'],'hidden_ids_n':len(h),'said_ids_n':len(s),
        'unscoreable_aliases':[w for w in c['hidden_aliases']+c['answer_aliases'] if not labels(w)]}),flush=True)
tree=ast.parse(Path('scripts/english/08_jlens_one_pass.py').read_text())
guard=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and ast.unparse(n.test)=='\'required_max_new_tokens\' in dataset')
for n in (8,32):
    try:
        exec(compile(ast.Module(body=[guard],type_ignores=[]),'production dataset guard','exec'),{'dataset':{'required_max_new_tokens':n}})
    except AssertionError:
        assert n==32
    else:
        assert n==8
print('PASS eight prompt/label pairs, four same-expected-answer contrasts, canonical scorability and production horizon guard; no neural inference, factual/semantic ambiguity remains',flush=True)
