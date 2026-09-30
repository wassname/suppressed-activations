"""Eight indirect donor prefills and ten fixed one-pass conditions. -- PI/OpenAI"""
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
from types import SimpleNamespace

ROOT=Path.cwd()
SOURCE_SHA='69455b6a07824eb675d6f738c6178691d9ff31929267944aae1b9ddf4eac6f3d'
DATA_SHA='e3eb753f8d4d44b790dcb43e16bb6aa313e74749c0bac4df444dc4a0a02417e8'
CONTRACT_SHA='c60fefdfb479994b6204593554b89459c564ab06f79f96c92d796a6d2a493e96'
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
contract=ROOT/'slop/audits/2026-10-01_indirect-donor-preregistration.md'
contract_bytes=contract.read_bytes();assert hashlib.sha256(contract_bytes).hexdigest()==CONTRACT_SHA
master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_indirect-donor-intervention'
master.mkdir(parents=True)
for src,name in ((source,'source.py'),(config,'config.json'),(Path(__file__),'launcher.py')):
    shutil.copyfile(src,master/name)
(master/'preregistration.md').write_bytes(contract_bytes)
for name in HELPERS:
    target=master/'helpers'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
metadata={'source_sha256':SOURCE_SHA,'config_sha256':DATA_SHA,'literal_donor_sha256':DONOR_SHA,
          'contract_sha256':CONTRACT_SHA,'helper_sha256':HELPERS,'stage':'preflight','runs':{},'goals_completed':False}
settings={'indirect_donor':True,'reverse':True,'prompt_positions':1,'decode_scale':.25,'block_index':15,'readout_block_index':23}
metadata['evaluation_settings']=settings
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
print(json.dumps({'master':str(master),'stage':'preflight','seconds':time.monotonic()-started}),flush=True)
g=runpy.run_path(str(source))['main'].__globals__
import torch

torch.set_num_threads(4)
forward_records=[];phase='preparation';original_loader=g['AutoModelForCausalLM'].from_pretrained

def record_forward(module,args,kwargs):
    ids=args[0] if args else kwargs['input_ids']
    record={'phase':phase,'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()}
    forward_records.append(record)
    with (master/'forward_trace.jsonl').open('a') as stream:stream.write(json.dumps(record)+'\n')

def tracked_loader(*args,**kwargs):
    model=original_loader(*args,**kwargs)
    model.register_forward_pre_hook(record_forward,with_kwargs=True)
    return model

g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=tracked_loader)
prepared=g['main'](prepare_donors_json=config)
assert len(forward_records)==8 and not any(r['grad_enabled'] for r in forward_records)
metadata['runs']['preparation']=str(prepared)
metadata['stage']='prepared'
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
checkpoint=prepared/'donors.pt'
artifact=torch.load(checkpoint,map_location='cpu',weights_only=True)
assert len(artifact['provenance']['samples'])==8
assert len(list((prepared/'donor-contexts').glob('*.pt')))==8
expected_delta=artifact['means']['spider']-artifact['means']['dog']
literal=torch.load(DONOR,map_location='cpu',weights_only=True)
literal_delta=literal['means']['spider']-literal['means']['dog']
checkpoint_sha=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
print(json.dumps({'stage':'prepared','seconds':time.monotonic()-started,'natural_delta_norm':float(expected_delta.norm()),
                  'literal_delta_norm':float(literal_delta.norm())}),flush=True)
gc.collect()
compact=[];previous_vectors=None
for relation,n in (('legs',4),('skeleton_body',4),('arithmetic_control',2)):
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()==checkpoint_sha
    phase=relation
    out=g['main'](donor_checkpoint=checkpoint,relation=relation,**settings)
    rows=json.loads((out/'interventions.json').read_text());assert len(rows)==n
    vectors=torch.load(out/'applied_vectors.pt',map_location='cpu',weights_only=True)
    assert torch.equal(vectors['indirect-description donor'],expected_delta)
    assert torch.equal(vectors['literal-name donor control'],literal_delta)
    assert torch.allclose(expected_delta.norm(),vectors['matched-random delta'].norm(),atol=1e-6,rtol=1e-6)
    if previous_vectors is not None:assert all(torch.equal(v,previous_vectors[k]) for k,v in vectors.items())
    previous_vectors=vectors
    calls=[r for r in forward_records if r['phase']==relation]
    assert len(calls)==sum(r['n_tokens'] for r in rows.values()) and not any(r['grad_enabled'] for r in calls)
    assert [r['sequence_length'] for r in calls]==[c['sequence_length'] for r in rows.values() for c in r['coverage']]
    for mode,row in rows.items():
        assert 1<=row['n_tokens']<=32 and len(row['coverage'])==row['n_tokens']
        assert row['coverage'][0]['positions']==1 and row['coverage'][0]['scale']==1
        assert all(c['positions']==c['sequence_length']==1 and c['scale']==.25 for c in row['coverage'][1:])
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),map_location='cpu',weights_only=True)
        delta=torch.zeros_like(expected_delta) if mode=='Base' else vectors[mode]
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
assert len(compact)==10 and sum(r['n_tokens'] for r in compact)<=320
for name,sha in HELPERS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
metadata.update(stage='completed',elapsed_seconds=time.monotonic()-started,offline_prefill_calls=8,
    evaluation_generation_trajectories=10,actual_forward_calls=len(forward_records),
    generated_tokens=sum(r['n_tokens'] for r in compact),donor_sha256=checkpoint_sha,
    peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,peak_reserved_gib=torch.cuda.max_memory_reserved()/2**30,
    semantic_review_pending=True)
(master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
report='---\npreparation_contexts: 8\ngeneration_trajectories: 10\nmax_new_tokens_per_condition: 32\n---\n# Indirect-description donor addition\n\nWritten by PI/OpenAI. Natural unrescaled donor difference, ordinary addition, no current-input lookahead. Literal-name donor retains its own natural norm; random matches the new norm. Norm/length differences remain confounds. Raw observations, not certified concept replacement.\n\n'
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
