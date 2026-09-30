"""Bounded offline VJP preparation and eight fixed causal conditions. -- PI/OpenAI"""
from datetime import datetime
import faulthandler
import gc
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import sys
import time

ROOT=Path.cwd()
SOURCE_SHA='8767a29aa90ce13624ee6a64802eea4a14014287b2b49164116600b4590048fd'
DATA_SHA='a1b1431045979b7490500b882662b8bb368bc368ea98b3291f89a763c08117f9'
DONOR=ROOT/'out/2026-09-30_133218_jlens-one-pass/donors.pt'
DONOR_SHA='572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5'
HELPERS={
 'scripts/demo.py':'3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
 'scripts/english/01_detector_baselines_and_pair_transfer.py':'812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
 'scripts/english/03_selector_search.py':'51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
 'scripts/english/04_erase_and_language_pairs.py':'734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
 'suppressed_activation_subspace.py':'415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
started=time.monotonic();faulthandler.dump_traceback_later(120,repeat=True)
source,config=map(Path,sys.argv[1:])
assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA
assert hashlib.sha256(config.read_bytes()).hexdigest()==DATA_SHA
assert hashlib.sha256(DONOR.read_bytes()).hexdigest()==DONOR_SHA
for name,sha in HELPERS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_vjp-intervention'
master.mkdir(parents=True)
for src,name in ((source,'source.py'),(config,'config.json'),(Path(__file__),'launcher.py'),
                 (ROOT/'slop/audits/2026-10-01_vjp-preregistration.md','preregistration.md')):
    shutil.copyfile(src,master/name)
for name in HELPERS:
    target=master/'helpers'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
metadata={'source_sha256':SOURCE_SHA,'config_sha256':DATA_SHA,'donor_sha256':DONOR_SHA,
          'helper_sha256':HELPERS,'stage':'preflight','runs':{},'goals_completed':False}
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
print(json.dumps({'master':str(master),'stage':'preflight','seconds':time.monotonic()-started}),flush=True)
g=runpy.run_path(str(source))['main'].__globals__
import torch

torch.set_num_threads(4)
prepared=g['main'](prepare_vjp_json=config,donor_checkpoint=DONOR)
metadata['runs']['preparation']=str(prepared)
metadata['stage']='prepared'
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
checkpoint=prepared/'vjp.pt'
artifact=torch.load(checkpoint,map_location='cpu',weights_only=True)
assert artifact['provenance']['passed'] and len(artifact['provenance']['records'])==8
checkpoint_sha=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
print(json.dumps({'stage':'prepared','seconds':time.monotonic()-started,'coefficient':artifact['provenance']['coefficient'],
                  'delta_norm':artifact['provenance']['delta_norm']}),flush=True)
gc.collect()
compact=[]
for relation,n in (('legs',3),('skeleton_body',3),('arithmetic_control',2)):
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()==checkpoint_sha
    out=g['main'](vjp_checkpoint=checkpoint,reverse=True,prompt_positions=1,decode_scale=.25,relation=relation)
    rows=json.loads((out/'interventions.json').read_text());assert len(rows)==n
    vectors=torch.load(out/'applied_vectors.pt',map_location='cpu',weights_only=True)
    assert torch.equal(vectors['offline naming VJP'],artifact['delta'])
    assert torch.allclose(vectors['offline naming VJP'].norm(),vectors['matched-random delta'].norm(),atol=1e-6,rtol=1e-6)
    for mode,row in rows.items():
        assert 1<=row['n_tokens']<=32 and len(row['coverage'])==row['n_tokens']
        assert row['coverage'][0]['positions']==1 and row['coverage'][0]['scale']==1
        assert all(c['positions']==c['sequence_length']==1 and c['scale']==.25 for c in row['coverage'][1:])
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),map_location='cpu',weights_only=True)
        delta=torch.zeros_like(artifact['delta']) if mode=='Base' else vectors[mode]
        requested=states[:,0]+delta
        requested[1:]=states[1:,0]+.25*(requested[1:]-states[1:,0])
        assert torch.equal(states[:,1],requested)
        assert torch.equal(states[:,2],states[:,1].to(torch.bfloat16).float())
        compact.append({'relation':relation,'condition':mode,'expected_answer':row['expected_answer'],
            'generation':row['generation'],'n_tokens':row['n_tokens'],'answer_log_odds_shift':row['answer_log_odds_shift'],
            'answer_pair_mass':row['answer_pair_mass'],'r2':row['r2'],'report':str((out/mode.lower().replace(' ','-')/'run.md').relative_to(ROOT))})
    metadata['runs'][relation]=str(out);metadata['stage']=relation
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    (master/'conditions.json').write_text(json.dumps(compact,ensure_ascii=False,indent=1))
    print(json.dumps({'stage':relation,'seconds':time.monotonic()-started}),flush=True)
    gc.collect()
assert len(compact)==8 and sum(r['n_tokens'] for r in compact)<=256
for name,sha in HELPERS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
metadata.update(stage='completed',elapsed_seconds=time.monotonic()-started,offline_forward_backward_calls=8,
    evaluation_generation_trajectories=8,generated_tokens=sum(r['n_tokens'] for r in compact),vjp_sha256=checkpoint_sha,
    peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,peak_reserved_gib=torch.cuda.max_memory_reserved()/2**30,
    semantic_review_pending=True)
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
report='---\npreparation_contexts: 8\ngeneration_trajectories: 8\nmax_new_tokens_per_condition: 32\n---\n# Fixed offline naming-VJP intervention\n\nWritten by PI/OpenAI. Natural projected pronoun scale; no current-input lookahead. Raw observations, not certified concept replacement.\n\n'
report+='| Property | Condition | Expected | Log-odds shift toward4/inside | Bare pair mass | Repeated-bigram rate |\n|---|---|---|---:|---:|---:|\n'
for r in compact:
    report+=f"| {r['relation']} | [{r['condition']}](../{Path(r['report']).relative_to('out')}) | {r['expected_answer']} | {r['answer_log_odds_shift']:.4f} | {r['answer_pair_mass']:.4f} | {r['r2']:.4f} |\n"
for r in compact:
    report+=f"\n## {r['relation']}: {r['condition']}\n\nExpected: {r['expected_answer']}. Exact{r['n_tokens']}-token continuation:\n\n```text\n{r['generation']}\n```\n"
report+='\nPositive shift favors4/inside; reverse animal targets8/outside favor negative shifts. Arithmetic should preserve4. Full condition logs contain exact input, prefilling/final readouts, top10 and coverage.\n'
(master/'run.md').write_text(report)
print(json.dumps(metadata,indent=1),flush=True)
print('run.md: '+str(master/'run.md'),flush=True)
faulthandler.cancel_dump_traceback_later()
