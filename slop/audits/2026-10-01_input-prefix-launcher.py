"""One cached complete-input-prefix comparison, without transformer calls. -- PI/OpenAI"""
import faulthandler
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import sys
import time

ROOT=Path.cwd()
SOURCE_SHA='9d8b8410675792a4dba7c7235d3672246c17d5690c463634dff0e2223a768b9e'
DATA_SHA='ced9ce88e658b20c9088ff51039736abc6bf40402032bf8eb0fd36279869eabe'
CONTRACT_SHA='4f3f27cfc3b92e033dc710ac877df67f459d8e974acfd979981207146b8f0fda'
CACHE=ROOT/'out/2026-10-01_060504_jlens-one-pass'
CACHE_SHA={'prefill.pt':'3e8e823d003b3b4f8cd33ad704a10cbbfbf2f177a5af998c443917603cd474be',
 'generation_traces.json':'eadec9aef6d5df7750937a0bbb4f022ec39ed9eb919c14f3f9814c69cc153756',
 'readout.json':'7822553fda78fd83fe63785f037de0568cf101527c8e888282a87d085263180c',
 'source.py':'8703a56f4313e673eb19f891b97eb3cbb247818187aa321e9f75130b3fc3b868'}
HELPERS={
 'scripts/demo.py':'3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
 'scripts/english/01_detector_baselines_and_pair_transfer.py':'812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
 'scripts/english/03_selector_search.py':'51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
 'scripts/english/04_erase_and_language_pairs.py':'734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
 'suppressed_activation_subspace.py':'415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
BASE_METHODS=['end-pass erased0.5 J-lens','end-pass erased0.5 plain24','end-pass erased0.5 plain27','end-pass J-lens']
METHODS=[m.replace('end-pass ','end-pass input-prefix ',1) for m in BASE_METHODS]
started=time.monotonic();faulthandler.dump_traceback_later(120,repeat=True)
source,data=map(Path,sys.argv[1:])
assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA
assert hashlib.sha256(data.read_bytes()).hexdigest()==DATA_SHA
contract=(ROOT/'slop/reviews/2026-10-01_after-vjp-next-test.md').read_bytes()
assert hashlib.sha256(contract).hexdigest()==CONTRACT_SHA
for name,sha in CACHE_SHA.items():assert hashlib.sha256((CACHE/name).read_bytes()).hexdigest()==sha
for name,sha in HELPERS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
print(json.dumps({'stage':'preflight','seconds':time.monotonic()-started}),flush=True)
g=runpy.run_path(str(source))['main'].__globals__
import torch

torch.set_num_threads(4)
out=g['main'](cases_json=data,end_pass_readout=True,output_mask_max_n=1,erase_output=True,
              erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,replay_readout_run=CACHE,expand_input_prefix=True)
shutil.copyfile(__file__,out/'launcher.py')
shutil.copyfile(data,out/'dataset.json')
(out/'preregistration.md').write_bytes(contract)
for name,sha in HELPERS.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
    target=out/'helpers'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
rows=json.loads((out/'readout.json').read_text())
index={(r['case_index'],r['method']):r for r in rows}
assert len(rows)==len(index)==88
previous=json.loads((CACHE/'readout.json').read_text());assert len(previous)==72
assert all(index[r['case_index'],r['method']]==r for r in previous)
assert (out/'generation_traces.json').read_bytes()==(CACHE/'generation_traces.json').read_bytes()
states=torch.load(out/'prefill.pt',weights_only=True,map_location='cpu')
original_states=torch.load(CACHE/'prefill.pt',weights_only=True,map_location='cpu')
assert all(torch.equal(a[k],b[k]) for a,b in zip(states,original_states,strict=True) for k in a)
exclusions=json.loads((out/'input_prefix_exclusions.json').read_text());assert len(exclusions)==4
for i,record in enumerate(exclusions):
    added={r['id'] for r in record['added_input_exclusions']}
    for method in METHODS:
        assert not added.intersection(index[i,method]['selected_ids'])
results=[]
for method in [*METHODS,*BASE_METHODS]:
    rs=[index[i,method] for i in range(4)]
    aucs=[r['alias_checked_auroc'] for r in rs if r['alias_checked_auroc'] is not None]
    results.append({'method':method,'n':4,'joint_alias_passes':sum(r['alias_checked_pass'] for r in rs),
        'mean_alias_auroc':sum(aucs)/len(aucs) if aucs else None,'auroc_n':len(aucs),
        'lexical_pairs':{pair:all(r['intended_answer_observed'] and r['alias_checked_pass'] and r['pair_hidden_rank']<r['pair_partner_rank'] for r in rs if r['pair']==pair) for pair in ('Asia','Africa')},
        'reviewed_joint':None,'reviewed_pairs':None})
(out/'paired_summary.json').write_text(json.dumps(results,indent=1))
report='# Complete-input-prefix mask, four development cases\n\nWritten by PI/OpenAI. Old72 rows exactly preserved;16 new candidate rows. No new transformer calls or generations. Lexical/AUROC results do not certify semantic exclusion.\n'
for i in range(4):
    r=index[i,METHODS[0]]
    report+=f"\n## {r['concept']}\n\nInput repr:\n```text\n{r['prompt']!r}\n```\n\nCached continuation:\n```text\n{r['baseline_generation']}\n```\n"
    for method in METHODS:
        r=index[i,method];base=index[i,method.replace('end-pass input-prefix ','end-pass ',1)]
        report+=f"\n### {method}\n\nCandidate lexical joint={r['alias_checked_pass']}; own/partner ranks={r['pair_hidden_rank']}/{r['pair_partner_rank']}.\n\n{r['top32']!r}\n\nOriginal {base['method']}:\n\n{base['top32']!r}\n"
(out/'case_comparison.md').write_text(report)
metadata={'source_sha256':SOURCE_SHA,'data_sha256':DATA_SHA,'contract_sha256':CONTRACT_SHA,'cache_sha256':CACHE_SHA,'helper_sha256':HELPERS,
 'original_rows_exact':72,'candidate_rows':16,'model_forward_calls':0,'new_generations':0,
 'elapsed_seconds':time.monotonic()-started,'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,
 'semantic_review_pending':True,'goals_completed':False}
(out/'pipeline.json').write_text(json.dumps(metadata,indent=1))
print(json.dumps({'run':str(out),'results':results,'pipeline':metadata},indent=1),flush=True)
faulthandler.cancel_dump_traceback_later()
