"""One cached pursuit experiment; no alternate-winner selection. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import sys

from tabulate import tabulate

helpers = {'scripts/demo.py': '3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39', 'scripts/english/01_detector_baselines_and_pair_transfer.py': '812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b', 'scripts/english/03_selector_search.py': '51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb', 'scripts/english/04_erase_and_language_pairs.py': '734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0', 'suppressed_activation_subspace.py': '415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
cache_hashes = {'prefill.pt': '277b8ead3fae918f795a42bac7cfe4bb2c976a7aab5f7f661f045cbe92cd08b9', 'generation_traces.json': 'e5a480e4cfd35ff62fb3d3e6b09d34d4fc4c1348ed8df929b55863a50d7d9c26', 'source.py': '8a7be64c38106e52d693ec5ab41a4588854b3c79fed92c76a3a1bef6df4aa7df', 'prefill_positions.pt': '9f5a1d3f0740d67dd1d547431e110d2335c24a44ffa5f429d66b61c75cd3156e', 'question_spans.json': '90a774a2aafb766f3c295e51bad2fd06a4deb1a4bd042533d202e76caba0ea71'}
reference = Path('out/2026-09-30_185058_jlens-one-pass')
assert all(hashlib.sha256((reference / n).read_bytes()).hexdigest() == digest for n, digest in cache_hashes.items())
helper_bytes = {path: Path(path).read_bytes() for path in helpers}
assert all(hashlib.sha256(helper_bytes[path]).hexdigest() == digest for path, digest in helpers.items())
source_bytes, data_bytes, launcher_bytes = Path(sys.argv[1]).read_bytes(), Path(sys.argv[2]).read_bytes(), Path(__file__).read_bytes()
assert hashlib.sha256(data_bytes).hexdigest() == 'f7e253176a60ab43d99b019d2b84fbec97cde0ba4df6c08b172d7c7f8f3a2173'
ns = runpy.run_path(sys.argv[1])
out = ns['main'](cases_json=Path(sys.argv[2]), end_pass_readout=True, output_mask_max_n=1,
    erase_output=True, erase_strength=.5, matching_pursuit=True, replay_readout_run=reference)
assert all(Path(path).read_bytes() == data for path, data in helper_bytes.items())
assert (out / 'source.py').read_bytes() == source_bytes == Path(sys.argv[1]).read_bytes()
assert data_bytes == Path(sys.argv[2]).read_bytes() and launcher_bytes == Path(__file__).read_bytes()
assert all(hashlib.sha256((reference / n).read_bytes()).hexdigest() == digest for n, digest in cache_hashes.items())
(out / 'launcher.py').write_bytes(launcher_bytes)
(out / 'helper_sha256.json').write_text(json.dumps(helpers, indent=1))
for path, data in helper_bytes.items():
    destination = out / 'helpers' / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
rows = json.loads((out / 'readout.json').read_text())
by_key = {(r['case_index'], r['method']): r for r in rows}
old = json.loads(Path('out/2026-09-30_151032_jlens-one-pass/readout.json').read_text())
assert len(old) == 168 and len(rows) == len(by_key) == 288
assert all(by_key[r['case_index'], r['method']] == r for r in old), 'Existing readout row changed'
assert json.loads((out / 'generation_traces.json').read_text()) == json.loads((reference / 'generation_traces.json').read_text())
summary = {r['method']: r for r in json.loads((out / 'summary.json').read_text())}
assert all(r['n'] == 8 for r in summary.values())
assert summary['end-pass erased0.5 plain27']['alias_checked_joint_pass'] == 6
records = json.loads((out / 'pursuit_records.json').read_text())
diagnostics = json.loads((out / 'pursuit_diagnostics.json').read_text())
assert len(records) == 24 and len(diagnostics) == 16
for record in records:
    n, i, representation = record['postmask_cardinality'], record['case_index'], record['representation']
    for variant in ('pursuit', 'raw-dot matched', 'unit-dot matched'):
        row = by_key[i, f'end-pass {variant} {representation}']
        assert row['returned_cardinality'] == row['return_limit'] == n
primary, control = 'end-pass pursuit J24', 'end-pass unit-dot matched J24'
gains = [i for i in range(8) if by_key[i, primary]['alias_checked_pass'] and not by_key[i, control]['alias_checked_pass']]
losses = [i for i in range(8) if by_key[i, control]['alias_checked_pass'] and not by_key[i, primary]['alias_checked_pass']]
new_candidates = []
for i in gains:
    prior = [r for r in diagnostics if r['case_index'] == i]
    assert {r['kind'] for r in prior} == {'early-prefix', 'pre-clue'}
    aliases = by_key[i, primary]['hidden_aliases']
    if not any(ns['q'].is_prefix_hit(token, alias, 3) for r in prior for token in r['active_tokens'] for alias in aliases):
        new_candidates.append(i)
selection = {'author': 'PI/OpenAI', 'role': 'v4 development; J24 sole primary', 'n': 8,
    'primary_count': summary[primary]['alias_checked_joint_pass'],
    'cardinality_matched_unit_dot_count': summary[control]['alias_checked_joint_pass'],
    'paired_gains': gains, 'paired_losses': losses, 'net_paired_gain': len(gains) - len(losses),
    'new_alias_gain_candidates_absent_from_unmasked_priors': new_candidates,
    'numeric_prerequisite_passed': len(gains) > len(losses) and bool(new_candidates),
    'semantic_review': 'unreviewed; review all affected gains/losses and both raw diagnostic inventories',
    'advance_to_v5': False, 'exact_prior_rows': len(old),
    'peak_allocated_gib': ns['torch'].cuda.max_memory_allocated() / 2**30,
    'peak_reserved_gib': ns['torch'].cuda.max_memory_reserved() / 2**30,
    'source_sha256': hashlib.sha256(source_bytes).hexdigest(), 'data_sha256': hashlib.sha256(data_bytes).hexdigest(),
    'launcher_sha256': hashlib.sha256(launcher_bytes).hexdigest(),
    'limits': 'Aliases are incomplete; prior absence is not semantic certification or counterfactual necessity. No alternate-winner promotion or old-gate reopening.'}
assert selection['net_paired_gain'] == selection['primary_count'] - selection['cardinality_matched_unit_dot_count']
(out / 'pursuit_selection.json').write_text(json.dumps(selection, ensure_ascii=False, indent=1, allow_nan=False))
methods = [m for m in summary if any(m.startswith('end-pass ' + v + ' ') for v in
    ('pursuit', 'raw-dot matched', 'unit-dot matched', 'raw-dot full32', 'unit-dot full32'))]
methods += ['end-pass J-lens', 'end-pass plain24', 'end-pass plain27', 'end-pass erased0.5 plain27']
methods.sort(key=lambda m: (-summary[m]['alias_checked_joint_pass'], m))
table = tabulate([[('**' + m + '**') if m == primary else ('*' + m + '*'),
    f"{summary[m]['alias_checked_joint_pass']}/8",
    sum(len(by_key[i, m]['top32']) for i in range(8)) / 8] for m in methods],
    headers=['Method', 'Alias joint ↑', 'Mean returned'], tablefmt='pipe', floatfmt='.2f')
appendix = ('\n\n## Pursuit comparison\n\nDevelopment aliases, not certified semantic accuracy. J24 primary; all controls retained.\n\n'
    + table + '\n\n' + f"Paired gains={gains}; losses={losses}; temporally new alias candidates={new_candidates}. "
    + 'Semantic review is pending; neither research goal is complete.\n\n' + f"run.md: {out / 'run.md'}\n")
with (out / 'run.md').open('a') as stream:
    stream.write(appendix)
print(json.dumps(selection, ensure_ascii=False, indent=1, allow_nan=False), flush=True)
print(appendix, flush=True)

