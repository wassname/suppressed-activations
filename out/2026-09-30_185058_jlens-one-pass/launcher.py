"""One position-pooling comparison; a passing screen is not semantic certification. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import sys

helpers={
    'scripts/demo.py':'3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
    'scripts/english/01_detector_baselines_and_pair_transfer.py':'812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
    'scripts/english/03_selector_search.py':'51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
    'scripts/english/04_erase_and_language_pairs.py':'734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
    'suppressed_activation_subspace.py':'415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
helper_bytes={path:Path(path).read_bytes() for path in helpers}
assert all(hashlib.sha256(helper_bytes[path]).hexdigest()==digest for path,digest in helpers.items())
main=runpy.run_path(sys.argv[1])['main']
out=main(cases_json=Path(sys.argv[2]),end_pass_readout=True,output_mask_max_n=1,
         erase_output=True,erase_strength=.5,pool_question=True,
         verify_readout_run=Path('out/2026-09-30_142814_jlens-one-pass'))
assert all(Path(path).read_bytes()==data for path,data in helper_bytes.items())
(out/'helper_sha256.json').write_text(json.dumps(helpers,indent=1))
for path,data in helper_bytes.items():
    destination=out/'helpers'/path
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(data)
rows=json.loads((out/'readout.json').read_text())
by_key={(r['case_index'],r['method']):r for r in rows}
old=json.loads(Path('out/2026-09-30_151032_jlens-one-pass/readout.json').read_text())
assert len(old)==168 and len(rows)==264 and len(by_key)==264
assert all(by_key[(r['case_index'],r['method'])]==r for r in old), 'Existing readout row changed'
summary={r['method']:r for r in json.loads((out/'summary.json').read_text())}
order=['plain27','J-lens','plain24']
counts={name:summary['end-pass pooled '+name]['alias_checked_joint_pass'] for name in order}
assert all(r['n']==8 for r in summary.values())
assert summary['end-pass erased0.5 plain27']['alias_checked_joint_pass']==6
winner=max(order,key=counts.__getitem__)
last=summary['end-pass pooling last '+winner]['alias_checked_joint_pass']
mismatch=summary['end-pass pooled mismatched '+winner]['alias_checked_joint_pass']
unsubtracted=summary['end-pass pooled probability '+winner]['alias_checked_joint_pass']
selection={'author':'PI/OpenAI','role':'v4 development screening only','tie_order':order,
           'pooled_counts':counts,'selected_representation':winner,'selected_last_count':last,
           'selected_mismatched_count':mismatch,'selected_unsubtracted_count':unsubtracted,
           'n':8,'numeric_screen_passed':counts[winner]>=7 and counts[winner]>last and counts[winner]>mismatch,
           'exact_prior_rows':168,'semantic_review':'not performed; required before new examples; no switching winner after failure',
           'limits':'Comparable unsubtracted results do not establish subtraction benefit. Hidden-only gains are insufficient. No window selection after failure.'}
(out/'pool_selection.json').write_text(json.dumps(selection,indent=1))
print(json.dumps(selection,indent=1),flush=True)
print(out/'run.md',flush=True)
