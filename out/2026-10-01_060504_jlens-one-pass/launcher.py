"""Run four preregistered native-chat readouts with frozen inputs. -- PI/OpenAI"""
import faulthandler
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import sys
import time

ROOT = Path.cwd()
SOURCE_SHA = '8703a56f4313e673eb19f891b97eb3cbb247818187aa321e9f75130b3fc3b868'
DATA_SHA = 'ced9ce88e658b20c9088ff51039736abc6bf40402032bf8eb0fd36279869eabe'
HELPERS = {
 'scripts/demo.py': '3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
 'scripts/english/01_detector_baselines_and_pair_transfer.py': '812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
 'scripts/english/03_selector_search.py': '51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
 'scripts/english/04_erase_and_language_pairs.py': '734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
 'suppressed_activation_subspace.py': '415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
METHODS = ['end-pass erased0.5 J-lens', 'end-pass erased0.5 plain24',
           'end-pass erased0.5 plain27', 'end-pass J-lens']
started = time.monotonic()
faulthandler.dump_traceback_later(120, repeat=True)
source, data = map(Path, sys.argv[1:])
assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA
assert hashlib.sha256(data.read_bytes()).hexdigest() == DATA_SHA
for name, expected in HELPERS.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
preflight_path = ROOT/'slop/audits/2026-10-01_chat-preflight.json'
preflight = json.loads(preflight_path.read_text())
assert preflight['data_sha256'] == DATA_SHA and preflight['model_forward_calls'] == 0
print(json.dumps({'stage':'preflight-done','elapsed_seconds':time.monotonic()-started}), flush=True)
g = runpy.run_path(str(source))['main'].__globals__
import torch

torch.set_num_threads(4)
print(json.dumps({'stage':'imports-done','elapsed_seconds':time.monotonic()-started}), flush=True)
out = g['main'](cases_json=data, end_pass_readout=True, output_mask_max_n=1,
                erase_output=True, erase_strength=.5, chat_readout=True, readout_max_new_tokens=32)
shutil.copyfile(__file__, out/'launcher.py')
shutil.copyfile(preflight_path, out/'preflight.json')
shutil.copyfile(ROOT/'slop/audits/2026-10-01_geography-chat-preregistration.md', out/'preregistration.md')
for name, expected in HELPERS.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
    target=out/'helpers'/name; target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/name, target)
traces=json.loads((out/'generation_traces.json').read_text())
rows=json.loads((out/'readout.json').read_text())
rendering=json.loads((out/'chat_rendering.json').read_text())
assert rendering['chat_template_sha256']==preflight['chat_template_sha256']
assert len(traces)==len(rendering['cases'])==4 and len(rows)==72
assert len({(r['case_index'],r['method']) for r in rows})==72
for trace, rendered, reference in zip(traces, rendering['cases'], preflight['renderings'], strict=True):
    assert rendered['rendered_repr']==reference['rendered_repr']==repr(trace['prompt'])
    assert rendered['input_ids']==reference['input_ids']
    n=len(trace['token_ids'])
    assert 1<=n<=32 and trace['n_tokens']==n
    assert trace['generation_overrides']=={'max_new_tokens':32,'do_sample':False,'use_cache':True,'eos_token_id':[248044,248046]}
    assert all(c==[len(rendered['input_ids'])]+[1]*(n-1) for c in trace['coverage'].values())
    assert trace['stopped_on_eos']==(trace['token_ids'][-1] in (248044,248046))
    assert n==32 or trace['stopped_on_eos']
    assert not any(t in (248044,248046) for t in trace['token_ids'][:-1])
results=[]
for method in METHODS:
    subset=[r for r in rows if r['method']==method]
    assert len(subset)==4
    ranks=[r['pair_hidden_rank']<r['pair_partner_rank'] for r in subset]
    lexical_pairs={pair: all(r['intended_answer_observed'] and r['alias_checked_pass'] and
                            r['pair_hidden_rank']<r['pair_partner_rank'] for r in subset if r['pair']==pair)
                   for pair in ('Asia','Africa')}
    aucs=[r['alias_checked_auroc'] for r in subset if r['alias_checked_auroc'] is not None]
    results.append({'method':method,'joint_alias_passes':sum(r['alias_checked_pass'] for r in subset),'n':4,
                    'expected_answer_alias_matches':sum(r['intended_answer_observed'] for r in subset),
                    'mean_alias_auroc':sum(aucs)/len(aucs) if aucs else None,'auroc_n':len(aucs),
                    'pair_rank_wins':ranks,'lexically_discriminating_pairs':lexical_pairs,
                    'reviewed_semantic_passes':None,'reviewed_discriminating_pairs':None})
(out/'paired_summary.json').write_text(json.dumps(results, indent=1))
report='# Four native-chat geography probes\n\nWritten by PI/OpenAI. Fixed method, selected geography task; these counts are lexical, not semantic certification.4 prompts/2 dependent pairs.\n\n'
for trace, case in zip(traces, json.loads(data.read_text())['cases'], strict=True):
    report+=f"## {case['concept']} (expected output {case['answer']})\n\nInput repr:\n```text\n{trace['prompt']!r}\n```\n\nContinuation ({trace['n_tokens']} tokens; EOS={trace['stopped_on_eos']}), verbatim:\n```text\n{trace['decoded_verbatim']}\n```\n\n"
    for method in METHODS:
        r=next(r for r in rows if r['case_index']==trace['case_index'] and r['method']==method)
        report+=f"{method}: lexical joint={r['alias_checked_pass']}; own/partner ranks={r['pair_hidden_rank']}/{r['pair_partner_rank']}.\n\n{r['top32']!r}\n\n"
(out/'case_comparison.md').write_text(report)
metadata={'source_sha256':SOURCE_SHA,'data_sha256':DATA_SHA,'helper_sha256':HELPERS,
          'generation_trajectories':4,'generated_tokens':sum(len(t['token_ids']) for t in traces),
          'declared_maximum_new_tokens':128,'elapsed_seconds':time.monotonic()-started,
          'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,
          'peak_reserved_gib':torch.cuda.max_memory_reserved()/2**30,
          'semantic_review_pending':True,'research_goals_completed':False}
(out/'pipeline.json').write_text(json.dumps(metadata, indent=1))
print(json.dumps({'run':str(out),'results':results,'pipeline':metadata}, indent=1), flush=True)
faulthandler.cancel_dump_traceback_later()
