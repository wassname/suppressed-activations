"""Reconstruct saved-score ranks/labels and paired margins; not neural replication. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys

import torch
from transformers import AutoTokenizer

torch.set_num_threads(4)
master=Path(sys.argv[1]);root=Path.cwd()
p=json.loads((master/'pipeline.json').read_text());assert p['stage']=='completed'
manifest=json.loads((master/'manifest.json').read_text())
assert hashlib.sha256((master/'manifest.json').read_bytes()).hexdigest()==p['manifest_sha256']
assert hashlib.sha256((master/'source.py').read_bytes()).hexdigest()==p['source_sha256']
for name,sha in manifest['pins'].items():
    path=root/name if name.startswith('out/') else master/'inputs'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,name
reference_path=Path(p['reference'])
assert hashlib.sha256(reference_path.read_bytes()).hexdigest()==p['reference_sha256']
reference=torch.load(reference_path,weights_only=True,map_location='cpu')
tok=AutoTokenizer.from_pretrained(reference['model'],revision=reference['revision'],local_files_only=True)
config=json.loads((master/'inputs/data/generic_readout_reference_v1.json').read_text())
prompt=tok.apply_chat_template([{'role':'user','content':config['user_content']}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
input_ids=tok(prompt,add_special_tokens=False).input_ids
assert reference['config']==config and reference['stage']=='completed'
assert reference['prompt']==prompt and reference['input_ids']==input_ids
assert reference['coverage']=={r:[len(input_ids)] for r in (24,27,32)}
assert reference['ignored_generated_token_count']==1
forwards=[json.loads(s) for s in (master/'forward_trace.jsonl').read_text().splitlines()]
assert forwards==[{'phase':'generic-preparation','sequence_length':len(input_ids),'grad_enabled':False}]
assert p['generic_forward_calls']==1 and p['case_forward_calls']==0
launcher=runpy.run_path(str(master/'launcher.py'))
first=torch.load(Path(p['groups'][0]['run'])/'reference_readout_scores/000.pt',weights_only=True)
n_vocab=next(iter(first.values())).numel()
vocab=[tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(n_vocab)))]
normalized=[t.strip().lower() for t in vocab]
helper=ast.parse((root/'slop/audits/2026-10-01_check-native-v4-run.py').read_text())
exec(compile(ast.Module(body=[n for n in helper.body if isinstance(n,ast.FunctionDef) and n.name in ('ids','disjoint','rank')],type_ignores=[]),'independent-label-helpers','exec'))
checked=0;max_auc_error=0.;max_prematch_error=0.;max_pair_error=0.;old_rows=0
for group in p['groups']:
    run=Path(group['run']);index=launcher['check_cached'](group,run);old_rows+=22*group['n']
    traces=json.loads((run/'generation_traces.json').read_text())
    exclusions=json.loads((run/'input_prefix_exclusions.json').read_text())
    refs=torch.load(run/'normalized_references.pt',weights_only=True,map_location='cpu')
    d=refs['generic']['J-lens'].numel()
    u=torch.randn(d,generator=torch.Generator().manual_seed(0));u=u/u.norm()
    for name in launcher['BASES']:
        expected=u*refs['generic'][name].norm()
        error=float((expected-refs['random'][name]).abs().max());max_prematch_error=max(max_prematch_error,error)
        assert error<1e-4
    for i in range(group['n']):
        raw=torch.load(run/'reference_readout_scores'/f'{i:03d}.pt',weights_only=True)
        originals=torch.load(run/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True)
        words=set(re.findall(r'\w+',traces[i]['prompt'].lower()))
        legacy=words|{w[:n] for w in words for n in range(3,len(w)+1)}
        extensions={t:sorted(w for w in words if len(w)>=3 and value.startswith(w)) for t,value in enumerate(normalized) if value not in legacy}
        extensions={t:origins for t,origins in extensions.items() if origins}
        assert {r['id']:r['originating_words'] for r in exclusions[i]['added_input_exclusions']}==extensions
        assert set(raw)==set(launcher['NEW'])
        for method,score in raw.items():
            r=index[i,method]
            old_method=method.replace('input-prefix ','').replace('generic-reference ','').replace('random-reference ','')
            z=score.masked_fill(~torch.isfinite(originals[old_method]),-torch.inf)
            z[list(extensions)]=-torch.inf
            selected=r['selected_ids'];assert len(selected)==len(set(selected))==32
            assert z[selected].tolist()==r['selected_scores'] and [vocab[t] for t in selected]==r['top32']
            cutoff=z.topk(32).values[-1]
            assert torch.isfinite(z[selected]).all() and (z[selected]>=cutoff).all()
            assert set((z>cutoff).nonzero().flatten().tolist())<=set(selected)
            actual_words=sorted(set(re.findall(r'[^\W_]+',traces[i]['scoring_text'].lower())))
            assert actual_words==r['actual_words']
            hidden_is_said=any(a.casefold() in actual_words for a in r['hidden_aliases'])
            expected_observed=any(re.search(r'\b'+re.escape(a)+r'\b',traces[i]['scoring_text'],re.I) for a in r['answer_aliases'])
            assert hidden_is_said==r['hidden_is_said'] and expected_observed==r['intended_answer_observed']
            h0,s0=ids(r['hidden_aliases']),ids(r['answer_aliases'])
            ah,an=disjoint(h0,ids(actual_words));_,sn=disjoint(h0,s0)
            ch,cn=disjoint(ah,an|(sn if expected_observed else set()))
            unscorable=[w for w in actual_words if not ids([w])]
            assert unscorable==r['unscorable_actual_words']
            evaluable=hidden_is_said or bool(ah and an and not unscorable and ch and cn)
            assert evaluable==r['alias_checked_evaluable']
            assert (evaluable and not hidden_is_said and bool(set(selected)&ch) and not bool(set(selected)&cn))==r['alias_checked_pass']
            if evaluable and not hidden_is_said:
                a,b=z[list(ch),None],z[list(cn)][None,:]
                auc=float(((a>b).double()+.5*(a==b).double()).mean())
                max_auc_error=max(max_auc_error,abs(auc-r['alias_checked_auroc']));assert max_auc_error<1e-7
            else:assert r['alias_checked_auroc'] is None
            h,s=disjoint(ids([r['concept']]),ids([r['answer']]))
            assert rank(z,h)==r['r_hidden'] and rank(z,s)==r['r_said']
            checked+=1
    if group['name']=='animals':
        labels=json.loads((master/'inputs/slop/audits/2026-10-01_animal-pairs-labels.json').read_text())['labels']
        saved=json.loads((master/'animal_margins.json').read_text())
        assert len(saved)==12
        for row in saved:
            a,b=row['pair'];j=0 if a=='horse' else 2
            margins=[]
            for i in (j,j+1):
                z=torch.load(run/'reference_readout_scores'/f'{i:03d}.pt',weights_only=True)[row['method']].double()
                margins.append(float(z[[t['id'] for t in labels[a]]].max()-z[[t['id'] for t in labels[b]]].max()))
            da,db=margins
            error=max(abs(da-row['own_margins'][0]),abs(-db-row['own_margins'][1]),abs(da-db-row['D']))
            max_pair_error=max(max_pair_error,error);assert error<1e-5
            assert row['reversal']==(da>0>db)
assert checked==72 and old_rows==264
result={'signature':'PI/OpenAI','passed':True,'candidate_rows_checked':checked,'old_rows_exact':old_rows,
        'generic_forward_calls':1,'case_forward_calls':0,'max_auc_error':max_auc_error,
        'max_random_reference_component_error':max_prematch_error,'max_pair_margin_error':max_pair_error,
        'scope':'Saved-logit/mask/label/rank and paired-margin reconstruction; old replay parity via archived launcher; reference metadata and prematched random checked. Not neural, GPU head, postprojection norm or semantic certification.'}
(master/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1),flush=True)
