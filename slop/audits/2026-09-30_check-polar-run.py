"""CPU reconstruction from saved full probabilities and independent polar SVD. -- PI/OpenAI"""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import torch
from tokenizers import Tokenizer

torch.set_num_threads(1)
root=Path(sys.argv[1]); load=lambda p:json.loads(p.read_text())
assert (root/'source.py').read_bytes()==subprocess.check_output(['git','show','0ae6378:scripts/english/08_jlens_one_pass.py'])
reference=Path('out/2026-09-30_185058_jlens-one-pass')
assert load(root/'cases.json')==load(reference/'cases.json')
for record in ('replay_source.json','polar_cache_sha256.json'):
    data=load(root/record)
    hashes=data['sha256'] if record=='replay_source.json' else data
    for name,digest in hashes.items():
        assert hashlib.sha256((reference/name).read_bytes()).hexdigest()==digest
assert load(root/'replay_source.json')['model_forward_calls']==0
for path,digest in load(root/'helper_sha256.json').items():
    assert hashlib.sha256((root/'helpers'/path).read_bytes()).hexdigest()==digest
states=torch.load(root/'prefill.pt',map_location='cpu',weights_only=True)
full=torch.load(reference/'prefill_positions.pt',map_location='cpu',weights_only=True)
assert len(states)==len(full)==8
assert all(torch.equal(h,full[i][r][-1]) for i,s in enumerate(states) for r,h in s.items())
assert load(root/'generation_traces.json')==load(reference/'generation_traces.json')
fit=torch.load(root/'polar_factor.pt',map_location='cpu',weights_only=True)
meta=load(root/'polar_factor.json'); Q=fit['Q']
lens_path=Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt')
assert hashlib.file_digest(lens_path.open('rb'),'sha256').hexdigest()==meta['lens_sha256']
J=torch.load(lens_path,map_location='cpu',weights_only=True)['J'][23].float()
for name,tensor in [('J',J),('Q',Q)]:
    assert hashlib.sha256(tensor.numpy().tobytes()).hexdigest()==meta[name+'_sha256']
u,s,vh=torch.linalg.svd(J.double(),full_matrices=False)
expected_Q=(u@vh).float(); polar_error=float((expected_Q-Q).abs().max())
assert polar_error<1e-6, polar_error
assert torch.allclose(s,fit['singular_values'],atol=1e-8,rtol=1e-8)
assert s[-1]>torch.finfo(torch.float64).eps*2560*s[0]
assert not meta['determinant_correction'] and meta['fit_dtype']=='float64' and meta['applied_dtype']=='float32'
spans=load(reference/'question_spans.json'); priors=load(root/'polar_prior_positions.json')
tok=Tokenizer.from_file('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json')
prefix=load(root/'cases.json')['prefix']; special=set(load(root/'tokenizer_special_ids.json')['r2_excluded_ids'])
for span,prior in zip(spans,priors,strict=True):
    enc=tok.encode(span['prompt'],add_special_tokens=False)
    assert enc.ids==span['input_ids'] and [list(x) for x in enc.offsets]==span['offsets']
    positions=[j for j,((a,b),token,flag) in enumerate(zip(enc.offsets,enc.ids,enc.special_tokens_mask,strict=True)) if not flag and token not in special and len(prefix)<=a<b<=len(span['prompt'])]
    assert positions==span['positions'] and prior['position']==positions[2]
    assert prior['pieces']==[tok.decode([enc.ids[j]],skip_special_tokens=False) for j in positions[:3]]
    assert prior['pieces'][:2]==['Fact',':'] and prior['pieces'][2] in (' The',' In')
    assert prior['consumed_prefix']==span['prompt'][:enc.offsets[positions[2]][1]]
rows={(r['case_index'],r['method']):r for r in load(root/'readout.json')}; assert len(rows)==224
old=load(Path('out/2026-09-30_151032_jlens-one-pass/readout.json'))
assert len(old)==168 and all(rows[r['case_index'],r['method']]==r for r in old)
components=load(root/'polar_components.json'); assert len(components)==56
masks={m['case_index']:set(m['prompt_mask_ids'])|set(m['output_mask_ids']) for m in load(root/'polar_masks.json')}
probabilities=[torch.load(root/'polar_probabilities'/f'{i:03d}.pt',weights_only=True) for i in range(8)]
for i,p in enumerate(probabilities):
    assert torch.equal(p['other'],probabilities[(i+1)%8]['final'])
    for values in p.values():
        assert values.shape==p['Q'].shape and values.dtype==torch.float32
        assert torch.isfinite(values).all() and (values>=0).all() and (values<=1).all()
        assert abs(float(values.double().sum())-1)<3e-6
scores={}
for c in components:
    i,name=c['case_index'],c['method']; variant=name.removeprefix('end-pass polar '); p=probabilities[i]
    key={'mismatched excess':'Q','unsubtracted':'Q','early-prefix excess':'early'}.get(variant,variant.removesuffix(' excess'))
    comparison=p['other'] if variant=='mismatched excess' else p['final']
    signed=p[key]-comparison; raw=p[key] if variant=='unsubtracted' else signed
    z=raw.masked_fill(raw<=0,-torch.inf); z[list(masks[i])]=-torch.inf
    scores[i,name]=z
    top=[t for t in z.argsort(descending=True,stable=True)[:32].tolist() if torch.isfinite(z[t])]
    assert c['selected_ids']==top and c['eligible_n']==int(z.isfinite().sum())
    assert c['cutoff_ties']==(int((z==z[top[-1]]).sum()) if top else 0)
    row=rows[i,name]; tokens={t['id']:t for t in c['tokens']}
    assert row['top32']==[tokens[t]['token'] for t in top]
    for t,item in tokens.items():
        assert item['token']==tok.decode([t],skip_special_tokens=False)
        assert item['p']==float(p[key][t]) and item['comparison_p']==float(comparison[t])
        assert item['signed_excess']==float(signed[t])
        assert item['score']==(float(z[t]) if torch.isfinite(z[t]) else None)
    hidden,said=c['hidden_label_ids'],c['said_label_ids']
    found=bool(set(hidden)&set(top)); excluded=not set(said)&set(top)
    assert row['alias_checked_hidden_found']==found and row['alias_checked_said_excluded']==excluded
    passed=row['alias_checked_evaluable'] and not row['hidden_is_said'] and found and excluded and not row['input_hits']
    assert row['alias_checked_pass']==passed
    if row['alias_checked_evaluable'] and not row['hidden_is_said']:
        auc=float(((z[hidden,None]>z[said]).float()+.5*(z[hidden,None]==z[said]).float()).mean())
        assert math.isclose(auc,row['alias_checked_auroc'],abs_tol=1e-7)
    for labels in c['other_hidden_labels'].values():
        best=z[labels['ids']].max()
        assert labels['rank']==(int((z>best).sum()) if torch.isfinite(best) else 10**9)
summary={r['method']:r for r in load(root/'summary.json')}
for name,item in summary.items():
    matched=[r for (_,method),r in rows.items() if method==name]
    assert len(matched)==item['n']==8 and sum(r['alias_checked_pass'] for r in matched)==item['alias_checked_joint_pass']
selection=load(root/'polar_selection.json')
for variant,count in selection['counts'].items():
    assert count==summary['end-pass polar '+variant]['alias_checked_joint_pass']
for margin in selection['prefix_comparisons']:
    i=margin['case_index']; name='end-pass polar Q excess'
    c=next(c for c in components if c['case_index']==i and c['method']==name)
    a=float(scores[i,name][c['hidden_label_ids']].max()); b=float(scores[i,'end-pass polar early-prefix excess'][c['hidden_label_ids']].max())
    finite=lambda x:x if math.isfinite(x) else None
    assert margin['full_max']==finite(a) and margin['early_max']==finite(b)
    assert margin['eligible_margin']==finite(a-b) and margin['strictly_increased']==(a>b)
    assert margin['alias_checked_pass']==rows[i,name]['alias_checked_pass']
counts=selection['counts']
passed=counts['Q excess']>=7 and all(counts['Q excess']>counts[k] for k in ('original-J excess','plain24 excess','plain27 excess','mismatched excess')) and all(m['strictly_increased'] for m in selection['prefix_comparisons'] if m['alias_checked_pass'])
assert selection['numeric_screen_passed']==passed
report={'author':'PI/OpenAI','status':'PASS independent CPU polar SVD, source/cache/span parity and full-vocabulary ranking reconstruction',
        'polar_max_abs_error':polar_error,'old_rows':168,'new_rows':56,'production_forward_calls':0,'new_generations':0,
        'selection':selection,'limits':'Full-vocabulary probabilities are saved production outputs, not independently recomputed from model weights. Alias/evaluability IDs and flags inherit the frozen scorer; semantic exclusion is not certified. Zero-forward count depends on inspected source/guards, not hardware tracing.'}
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=1,allow_nan=False))
print(json.dumps(report,ensure_ascii=False,indent=1,allow_nan=False))
