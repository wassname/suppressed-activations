"""Independent saved-gradient algebra and condition checks; no neural replay. -- PI/OpenAI"""
import hashlib
import json
import math
from pathlib import Path
import torch

torch.set_num_threads(4)
root=Path('out/2026-10-01_063917_vjp-intervention')
pipeline=json.loads((root/'pipeline.json').read_text())
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==pipeline['source_sha256']
prepared=Path(pipeline['runs']['preparation'])
a=torch.load(prepared/'vjp.pt',map_location='cpu',weights_only=True)
assert hashlib.sha256((prepared/'vjp.pt').read_bytes()).hexdigest()==pipeline['vjp_sha256']
mean=a['gradients'].double().mean(0);direction=mean/mean.norm();coefficient=a['donor_difference'].double()@direction
expected=coefficient*direction
assert coefficient>0 and expected.norm()<=a['donor_difference'].double().norm()
max_error=float((expected-a['delta'].double()).abs().max());assert max_error<1e-6
contexts=[torch.load(f,map_location='cpu',weights_only=True) for f in sorted((prepared/'vjp-contexts').glob('*.pt'))]
assert len(contexts)==8
assert torch.equal(torch.stack([r['gradient'] for r in contexts]),a['gradients'])
assert torch.equal(torch.stack([r['state'] for r in contexts]),a['states'])
assert [r['record'] for r in contexts]==a['provenance']['records']
all_rows=[];reference_vectors=None;comparison=[]
for relation in ('legs','skeleton_body','arithmetic_control'):
    out=Path(pipeline['runs'][relation]);rows=json.loads((out/'interventions.json').read_text())
    vectors=torch.load(out/'applied_vectors.pt',map_location='cpu',weights_only=True)
    if reference_vectors is None:reference_vectors=vectors
    assert all(torch.equal(v,reference_vectors[k]) for k,v in vectors.items())
    assert torch.equal(vectors['offline naming VJP'],a['delta'])
    assert abs(float(vectors['matched-random delta'].norm()-a['delta'].norm()))<1e-6
    for mode,r in rows.items():
        n=r['n_tokens'];assert n==len(r['token_ids'])==len(r['coverage'])==32
        assert r['coverage'][0]['positions']==1
        assert all(c['sequence_length']==c['positions']==1 for c in r['coverage'][1:])
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),map_location='cpu',weights_only=True)
        delta=torch.zeros_like(a['delta']) if mode=='Base' else vectors[mode]
        requested=states[:,0]+delta;requested[1:]=states[1:,0]+.25*(requested[1:]-states[1:,0])
        assert torch.equal(requested,states[:,1]) and torch.equal(requested.to(torch.bfloat16).float(),states[:,2])
        assert math.isclose(r['answer_pair_mass'],r['p_answer0']+r['p_answer1'],abs_tol=1e-7)
        base=rows['Base']
        shift=math.log(r['p_answer1']/r['p_answer0'])-math.log(base['p_answer1']/base['p_answer0'])
        assert abs(shift-r['answer_log_odds_shift'])<1e-6
        assert all(math.isclose(t['p'],math.exp(t['log_p']),rel_tol=1e-6) for t in r['top10'])
        assert (out/mode.lower().replace(' ','-')/'run.md').is_file()
        all_rows.append(r)
    comparison.append({'relation':relation,'vjp_equals_base_ids':rows['offline naming VJP']['token_ids']==rows['Base']['token_ids'],
        'vjp_equals_random_ids':None if relation=='arithmetic_control' else rows['offline naming VJP']['token_ids']==rows['matched-random delta']['token_ids'],
        'vjp_prefill_requested_norm':rows['offline naming VJP']['coverage'][0]['requested_delta_norm'],
        'vjp_prefill_applied_norm':rows['offline naming VJP']['coverage'][0]['applied_delta_norm']})
assert len(all_rows)==8
result={'signature':'PI/OpenAI','scope':'saved gradient projection, exact F32/BF16 state equations, coverage and scalar metrics; not independent neural/backward/hardware/semantic certification',
        'naming_contexts':8,'trajectories':8,'generated_tokens':sum(r['n_tokens'] for r in all_rows),
        'float64_projection_max_error':max_error,'projection_fraction':float(coefficient/a['donor_difference'].double().norm()),'comparisons':comparison,'passed':True}
(root/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1))
