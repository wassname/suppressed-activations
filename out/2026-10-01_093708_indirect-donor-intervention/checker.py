"""Check saved donor means, actual call trace and edits; no neural replay. -- PI/OpenAI"""
import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import torch

torch.set_num_threads(4)
root=Path(sys.argv[1]);pipeline=json.loads((root/'pipeline.json').read_text())
assert pipeline['stage']=='completed'
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==pipeline['source_sha256']
assert hashlib.sha256((root/'config.json').read_bytes()).hexdigest()==pipeline['config_sha256']
assert hashlib.sha256((root/'preregistration.md').read_bytes()).hexdigest()==pipeline['contract_sha256']
for path,sha in pipeline['helper_sha256'].items():assert hashlib.sha256((root/'helpers'/path).read_bytes()).hexdigest()==sha
prepared=Path(pipeline['runs']['preparation'])
a=torch.load(prepared/'donors.pt',map_location='cpu',weights_only=True)
assert hashlib.sha256((prepared/'donors.pt').read_bytes()).hexdigest()==pipeline['donor_sha256']
config=json.loads((root/'config.json').read_text());assert a['provenance']['config']==config
literal_path=Path(config['literal_control_path'])
assert hashlib.sha256(literal_path.read_bytes()).hexdigest()==pipeline['literal_donor_sha256']==config['literal_control_sha256']
literal=torch.load(literal_path,map_location='cpu',weights_only=True)
contexts=[torch.load(p,map_location='cpu',weights_only=True) for p in sorted((prepared/'donor-contexts').glob('*.pt'))]
assert len(contexts)==8 and [c['record'] for c in contexts]==a['provenance']['samples']
assert [ast.literal_eval(c['record']['input_repr']) for c in contexts]==sum((config['prompts'][c] for c in config['concepts']),[])
assert {c['record']['token_ids'][-1] for c in contexts}=={1049}
max_mean_error=0.0
for concept in config['concepts']:
    states=torch.stack([c['state'] for c in contexts if c['record']['concept']==concept])
    assert states.shape[0]==4 and torch.equal(states,a['sample_states'][concept])
    expected=states.double().mean(0);error=(expected-a['means'][concept].double()).abs()
    bound=8*torch.finfo(torch.float32).eps*states.double().abs().mean(0)
    assert (error<=bound).all()
    max_mean_error=max(max_mean_error,float(error.max()))
delta=a['means']['spider']-a['means']['dog']
literal_delta=literal['means']['spider']-literal['means']['dog']
trace=[json.loads(line) for line in (root/'forward_trace.jsonl').read_text().splitlines()]
assert not any(r['grad_enabled'] for r in trace)
prep_trace=[r for r in trace if r['phase']=='preparation']
assert len(prep_trace)==8 and [r['sequence_length'] for r in prep_trace]==[len(c['record']['token_ids']) for c in contexts]
old_pipeline=json.loads(Path('out/2026-10-01_063917_vjp-intervention/pipeline.json').read_text())
all_rows=[];reference_vectors=None;comparisons=[]
for relation,count in (('legs',4),('skeleton_body',4),('arithmetic_control',2)):
    out=Path(pipeline['runs'][relation]);rows=json.loads((out/'interventions.json').read_text());assert len(rows)==count
    vectors=torch.load(out/'applied_vectors.pt',map_location='cpu',weights_only=True)
    if reference_vectors is None:reference_vectors=vectors
    assert all(torch.equal(v,reference_vectors[k]) for k,v in vectors.items())
    assert torch.equal(vectors['indirect-description donor'],delta)
    assert torch.equal(vectors['literal-name donor control'],literal_delta)
    assert torch.allclose(vectors['matched-random delta'].norm(),delta.norm(),rtol=1e-6,atol=1e-6)
    calls=[r for r in trace if r['phase']==relation]
    assert [r['sequence_length'] for r in calls]==[c['sequence_length'] for r in rows.values() for c in r['coverage']]
    special=set(json.loads((out/'tokenizer_special_ids.json').read_text())['r2_excluded_ids'])
    for mode,r in rows.items():
        n=r['n_tokens'];assert 1<=n<=32 and n==len(r['token_ids'])==len(r['coverage'])
        assert r['coverage'][0]['positions']==1 and r['coverage'][0]['scale']==1
        assert all(c['positions']==c['sequence_length']==1 and c['scale']==.25 for c in r['coverage'][1:])
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),map_location='cpu',weights_only=True)
        update=torch.zeros_like(delta) if mode=='Base' else vectors[mode]
        requested=states[:,0]+update;requested[1:]=states[1:,0]+.25*(requested[1:]-states[1:,0])
        assert torch.equal(requested,states[:,1]) and torch.equal(requested.to(torch.bfloat16).float(),states[:,2])
        assert math.isclose(r['answer_pair_mass'],r['p_answer0']+r['p_answer1'],abs_tol=1e-7)
        base=rows['Base']
        shift=math.log(r['p_answer1']/r['p_answer0'])-math.log(base['p_answer1']/base['p_answer0'])
        assert abs(shift-r['answer_log_odds_shift'])<1e-6
        assert all(math.isclose(t['p'],math.exp(t['log_p']),rel_tol=1e-6) for t in r['top10'])
        ids=[t for t in r['token_ids'] if t not in special];bigrams=list(zip(ids,ids[1:]))
        repetition=1-len(set(bigrams))/len(bigrams) if bigrams else 0
        assert abs(repetition-r['r2'])<1e-12
        assert (out/mode.lower().replace(' ','-')/'run.md').is_file()
        all_rows.append(r)
    previous=json.loads((Path(old_pipeline['runs'][relation])/'interventions.json').read_text())
    comparisons.append({'relation':relation,'base_matches_job2681_ids':rows['Base']['token_ids']==previous['Base']['token_ids'],
        'indirect_equals_base_ids':rows['indirect-description donor']['token_ids']==rows['Base']['token_ids'],
        'indirect_equals_random_ids':None if relation=='arithmetic_control' else rows['indirect-description donor']['token_ids']==rows['matched-random delta']['token_ids'],
        'indirect_equals_literal_ids':None if relation=='arithmetic_control' else rows['indirect-description donor']['token_ids']==rows['literal-name donor control']['token_ids']})
assert len(all_rows)==10 and len(trace)==8+sum(r['n_tokens'] for r in all_rows)==pipeline['actual_forward_calls']
result={'signature':'PI/OpenAI','scope':'float64 donor-mean reconstruction, exact F32/BF16 edits, forward trace/coverage, scalar probabilities and non-special-token repetition; not independent neural/hardware/semantic certification',
    'preparation_contexts':8,'trajectories':10,'actual_forward_calls':len(trace),'generated_tokens':sum(r['n_tokens'] for r in all_rows),
    'float64_mean_max_error':max_mean_error,'natural_delta_norm':float(delta.norm()),'literal_delta_norm':float(literal_delta.norm()),
    'comparisons':comparisons,'passed':True}
(root/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1))
