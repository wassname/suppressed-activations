"""One cached polar-factor experiment; no representation reselection. -- PI/OpenAI"""
import hashlib
import json
import math
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
reference=Path('out/2026-09-30_185058_jlens-one-pass')
out=main(cases_json=Path(sys.argv[2]),end_pass_readout=True,output_mask_max_n=1,
         erase_output=True,erase_strength=.5,polar_readout=True,replay_readout_run=reference)
assert all(Path(path).read_bytes()==data for path,data in helper_bytes.items())
(out/'helper_sha256.json').write_text(json.dumps(helpers,indent=1))
for path,data in helper_bytes.items():
    destination=out/'helpers'/path
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(data)
rows=json.loads((out/'readout.json').read_text())
by_key={(r['case_index'],r['method']):r for r in rows}
old=json.loads(Path('out/2026-09-30_151032_jlens-one-pass/readout.json').read_text())
assert len(old)==168 and len(rows)==224 and len(by_key)==224
assert all(by_key[(r['case_index'],r['method'])]==r for r in old), 'Existing readout row changed'
assert json.loads((out/'generation_traces.json').read_text())==json.loads((reference/'generation_traces.json').read_text())
summary={r['method']:r for r in json.loads((out/'summary.json').read_text())}
assert all(r['n']==8 for r in summary.values())
assert summary['end-pass erased0.5 plain27']['alias_checked_joint_pass']==6
names=['Q excess','original-J excess','plain24 excess','plain27 excess','mismatched excess','unsubtracted','early-prefix excess']
counts={name:summary['end-pass polar '+name]['alias_checked_joint_pass'] for name in names}
components={(c['case_index'],c['method']):c for c in json.loads((out/'polar_components.json').read_text())}
assert len(components)==56

def maximum(record,ids,field='score'):
    tokens={t['id']:t for t in record['tokens']}
    return max((tokens[t][field] for t in ids if tokens[t][field] is not None),default=-math.inf)

def finite_or_none(value):
    return value if math.isfinite(value) else None

margins=[]
for i in range(8):
    name='end-pass polar Q excess'
    row=by_key[i,name]; last=components[i,name]; prior=components[i,'end-pass polar early-prefix excess']
    assert last['hidden_label_ids']==prior['hidden_label_ids']
    ids=last['hidden_label_ids']; full_max=maximum(last,ids); early_max=maximum(prior,ids)
    wrong=[]
    for other,labels in last['other_hidden_labels'].items():
        score=maximum(last,labels['ids'])
        wrong.append({'case_index':int(other),'concept':labels['concept'],'full_max':finite_or_none(score),
                      'early_max':finite_or_none(maximum(prior,labels['ids'])),
                      'token_rank':labels['rank'],'beats_current_hidden':score>full_max,'ties_current_hidden':score==full_max})
    margins.append({'case_index':i,'concept':row['concept'],'alias_checked_pass':row['alias_checked_pass'],
        'full_max':finite_or_none(full_max),'early_max':finite_or_none(early_max),
        'eligible_margin':finite_or_none(full_max-early_max),'strictly_increased':full_max>early_max,
        'raw_signed_full_max':finite_or_none(maximum(last,ids,'signed_excess')),
        'raw_signed_early_max':finite_or_none(maximum(prior,ids,'signed_excess')),
        'wrong_label_comparisons':wrong})
selection={'author':'PI/OpenAI','role':'v4 development only; Q fixed as sole candidate',
    'counts':counts,'n':8,'exact_prior_rows':168,'incumbent_half_plain27':6,'prefix_comparisons':margins,
    'numeric_screen_passed':counts['Q excess']>=7 and all(counts['Q excess']>counts[k] for k in
        ('original-J excess','plain24 excess','plain27 excess','mismatched excess')) and
        all(m['strictly_increased'] for m in margins if m['alias_checked_pass']),
    'semantic_review':'required before new examples; no definite input/said leaks among counted passes',
    'limits':'No posthoc spectrum/layer/window tuning. Early prefix misses later topic priors. Other-label sets are not topic-matched. Unsubtracted parity prevents a subtraction-benefit claim. Nonfinite eligible maxima/margins are null, with the comparison boolean preserved.'}
(out/'polar_selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=1,allow_nan=False))
print(json.dumps(selection,ensure_ascii=False,indent=1,allow_nan=False),flush=True)
print(out/'run.md',flush=True)
