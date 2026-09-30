"""Saved-score arithmetic, old-row parity and fixed-selection audit. -- PI/OpenAI"""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
assert (root/'source.py').read_bytes() == subprocess.check_output(['git','show','091de02:scripts/english/08_jlens_one_pass.py'])
load = lambda path: json.loads(path.read_text())
replay = load(root/'replay_source.json')
assert replay['model_forward_calls'] == 0
cache = Path(replay['run'])
for name,digest in replay['sha256'].items():
    assert hashlib.sha256((cache/name).read_bytes()).hexdigest() == digest
assert load(root/'generation_traces.json') == load(cache/'generation_traces.json')
key = lambda row: (row['case_index'],row['method'])
rows = {key(row):row for row in load(root/'readout.json')}
assert len(rows) == 216
old = load(Path('out/2026-09-30_151032_jlens-one-pass/readout.json'))
assert len(old) == 168
for row in old:
    assert row == rows[key(row)], key(row)
components = load(root/'token_kl_components.json')
masks = {r['case_index']:set(r['prompt_mask_ids'])|set(r['output_mask_ids']) for r in load(root/'token_kl_masks.json')}
assert len(components) == 48 and len({key(r) for r in components}) == 48 and len(masks) == 8
rare = []
for trace in components:
    row = rows[key(trace)]
    tokens = {t['id']:t for t in trace['tokens']}
    selected = trace['selected_ids']
    assert len(selected) == len(set(selected)) <= 32
    assert row['top32'] == [tokens[t]['token'] for t in selected]
    for token in tokens.values():
        delta = token['log_p']-token['log_q']
        assert math.isclose(delta,token['difference'],rel_tol=1e-5,abs_tol=1e-5)
        assert token['eligible'] == (token['difference']>0 and token['id'] not in masks[trace['case_index']])
        if token['eligible']:
            assert math.isclose(token['log_score'],token['log_p']+math.log(token['difference']),rel_tol=1e-5,abs_tol=1e-5)
        else:
            assert token['log_score'] is None
    assert all(tokens[t]['eligible'] for t in selected)
    assert sorted(selected,key=lambda t:(-tokens[t]['log_score'],t)) == selected
    assert trace['eligible_n'] >= len(selected)
    for token in tokens.values():
        if token['eligible'] and token['id'] not in selected and selected:
            assert (-token['log_score'],token['id']) >= (-tokens[selected[-1]]['log_score'],selected[-1])
    hidden,said = set(trace['hidden_label_ids']),set(trace['said_label_ids'])
    assert row['alias_checked_hidden_found'] == bool(hidden.intersection(selected))
    assert row['alias_checked_said_excluded'] == (not said.intersection(selected))
    passed = row['alias_checked_evaluable'] and not row['hidden_is_said'] and bool(hidden.intersection(selected)) and not said.intersection(selected) and not row['input_hits']
    assert row['alias_checked_pass'] == passed
    if row['alias_checked_evaluable'] and not row['hidden_is_said']:
        value = lambda t: tokens[t]['log_score'] if tokens[t]['eligible'] else -math.inf
        auc = sum(float(value(h)>value(s))+.5*float(value(h)==value(s)) for h in hidden for s in said)/(len(hidden)*len(said))
        assert math.isclose(auc,row['alias_checked_auroc'],rel_tol=1e-6,abs_tol=1e-6)
    rare.append({'case_index':trace['case_index'],'concept':row['concept'],'method':trace['method'],
                 'selected_n':len(selected),'p_R_below_1e-5':sum(tokens[t]['log_p']<math.log(1e-5) for t in selected)})
summary = load(root/'summary.json')
for item in summary:
    matching = [r for r in rows.values() if r['method']==item['method']]
    assert len(matching) == item['n'] == 8
    assert sum(r['alias_checked_pass'] for r in matching) == item['alias_checked_joint_pass']
selection = load(root/'token_kl_selection.json')
counts = {name:sum(r['alias_checked_pass'] for r in rows.values() if r['method']=='end-pass positive token-KL '+name) for name in ('plain27','J-lens','plain24')}
winner = max(counts,key=counts.__getitem__)
mismatch = sum(r['alias_checked_pass'] for r in rows.values() if r['method']=='end-pass mismatched positive token-KL '+winner)
assert selection['matched_counts']==counts and selection['selected_representation']==winner
assert selection['selected_mismatched_count']==mismatch
assert selection['numeric_screen_passed']==(counts[winner]>=7 and counts[winner]>mismatch)
report = {'author':'PI/OpenAI','status':'PASS recorded-score reconstruction and168 exact old-row matches',
          'n_new_rows':48,'selection':selection,'rare_token_counts':rare,
          'limits':'Selected/scored-token components verify arithmetic, masks and scored comparisons, not full-vocabulary top32 optimality or semantic exclusion. Zero-forward claim also relies on executed guarded source, not an independent hardware trace.'}
(root/'verification.json').write_text(json.dumps(report,indent=1))
print(json.dumps(report,indent=1))
