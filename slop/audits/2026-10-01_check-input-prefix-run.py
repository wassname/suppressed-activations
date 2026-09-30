"""Reconstruct exclusions and full-vocabulary ranks, not model inference. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import re
import sys

import torch
from transformers import AutoTokenizer

torch.set_num_threads(4)
root=Path(sys.argv[1]);pipeline=json.loads((root/'pipeline.json').read_text())
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==pipeline['source_sha256']
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
first_scores=torch.load(root/'input_prefix_scores/000.pt',weights_only=True,map_location='cpu')
vocab_size=next(iter(first_scores.values())).numel()
vocab=[tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(vocab_size)))]
normalized=[v.strip().lower() for v in vocab]
rows=json.loads((root/'readout.json').read_text());index={(r['case_index'],r['method']):r for r in rows}
assert len(rows)==len(index)==88
cache=Path(json.loads((root/'replay_source.json').read_text())['run'])
for name,sha in pipeline['cache_sha256'].items():assert hashlib.sha256((cache/name).read_bytes()).hexdigest()==sha
old=json.loads((cache/'readout.json').read_text());assert len(old)==72
assert all(index[r['case_index'],r['method']]==r for r in old)
exclusions=json.loads((root/'input_prefix_exclusions.json').read_text());assert len(exclusions)==4

def ids(words):
    return {i for i,t in enumerate(normalized) if any(len(t)>=min(3,len(w)) and w.lower().startswith(t) for w in words)}

def rank(z,labels):
    assert labels
    best=z[list(labels)].max()
    return int((z>best).sum()) if torch.isfinite(best) else 10**9

checked=0;max_auc_error=0;added_counts=[]
for i,record in enumerate(exclusions):
    words=set(re.findall(r'\w+',record['prompt'].lower()))
    legacy=words|{w[:n] for w in words for n in range(3,len(w)+1)}
    expected={}
    for t,value in enumerate(normalized):
        origins=sorted(w for w in words if len(w)>=3 and value.startswith(w))
        if origins and value not in legacy:expected[t]=origins
    assert {r['id']:r['originating_words'] for r in record['added_input_exclusions']}==expected
    assert all(r['token']==vocab[r['id']] and r['normalized']==normalized[r['id']] for r in record['added_input_exclusions'])
    originals=torch.load(root/'input_prefix_scores'/f'{i:03d}.pt',map_location='cpu',weights_only=True)
    assert len(originals)==4;added_counts.append(len(expected))
    assert all((not bool(torch.isfinite(originals['end-pass J-lens'][r['id']])))==r['already_output_masked'] for r in record['added_input_exclusions'])
    for method,original in originals.items():
        prior=index[i,method];r=index[i,method.replace('end-pass ','end-pass input-prefix ',1)]
        assert original[prior['selected_ids']].tolist()==prior['selected_scores']
        z=original.clone();z[list(expected)]=-torch.inf
        selected=r['selected_ids'];assert len(selected)==len(set(selected))==32
        assert not set(selected)&set(expected)
        assert z[selected].tolist()==r['selected_scores'] and [vocab[t] for t in selected]==r['top32']
        cutoff=z.topk(32).values[-1]
        assert torch.isfinite(z[selected]).all() and (z[selected]>=cutoff).all()
        assert set((z>cutoff).nonzero().flatten().tolist())<=set(selected)
        h,s=ids(r['hidden_aliases']),ids(r['answer_aliases']);shared=h&s;h-=shared;s-=shared
        assert rank(z,h)==r['pair_hidden_rank'] and rank(z,ids(r['partner_aliases']))==r['pair_partner_rank']
        p,n=z[list(h),None],z[list(s)][None,:]
        auc=float(((p>n).double()+.5*(p==n).double()).mean())
        max_auc_error=max(max_auc_error,abs(auc-r['alias_checked_auroc']));assert max_auc_error<1e-7
        lexical_pass=bool(set(selected)&h) and not bool(set(selected)&s)
        assert lexical_pass==r['alias_checked_pass']
        assert rank(z,ids([r['concept']]))==r['r_hidden'] and rank(z,ids([r['answer']]))==r['r_said']
        checked+=1
result={'signature':'PI/OpenAI','scope':'independent exclusion provenance and saved full-vocabulary score/rank reconstruction; tied cutoff membership checked, not CPU/GPU tied ordering; no neural or semantic certification',
        'rows_checked':checked,'old_rows_exact':72,'added_input_exclusion_counts':added_counts,'max_auc_error':max_auc_error,'passed':True}
(root/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1))
