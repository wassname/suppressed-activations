"""CPU artifact/ranking and selected-direction reconstruction; no inference. — PI/OpenAI"""
import ast
from collections import defaultdict
from functools import cache
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from safetensors import safe_open
from tokenizers import Tokenizer
import torch

root = Path(sys.argv[1]).resolve()
torch.set_num_threads(2)
source_sha = '5e31845bedb7df4a0fc9a924845ac1bb075f691142ba6cc63a95a7769653cb40'
launcher_sha = 'e2ddb1ba019b661469a82f413853bef9591b628c8ab789a74a832b0639c41c16'
assert hashlib.sha256((root / 'source.py').read_bytes()).hexdigest() == source_sha
assert hashlib.sha256((root / 'launcher.py').read_bytes()).hexdigest() == launcher_sha
launcher = ast.parse((root / 'launcher.py').read_text())
constants = {n.targets[0].id: ast.literal_eval(n.value) for n in launcher.body
             if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
             and n.targets[0].id in ('helpers', 'cache_hashes')}
for path, digest in constants['helpers'].items():
    assert hashlib.sha256((root / 'helpers' / path).read_bytes()).hexdigest() == digest
reference = Path('out/2026-09-30_185058_jlens-one-pass')
for path, digest in constants['cache_hashes'].items():
    assert hashlib.sha256((reference / path).read_bytes()).hexdigest() == digest
load = lambda name: json.loads((root / name).read_text())
selection = load('gradient_pursuit_selection.json')
assert selection['source_sha256'] == source_sha and selection['launcher_sha256'] == launcher_sha
assert not selection['advance_to_v5']
cases = load('cases.json')
traces = load('generation_traces.json')
assert traces == json.loads((reference / 'generation_traces.json').read_text())
states = torch.load(reference / 'prefill_positions.pt', map_location='cpu', weights_only=True)
last_states = torch.load(root / 'prefill.pt', map_location='cpu', weights_only=True)
spans = json.loads((reference / 'question_spans.json').read_text())
assert len(states) == len(last_states) == len(traces) == len(cases['cases']) == 8
assert all(torch.equal(last[r], full[r][-1]) for last, full in zip(last_states, states, strict=True) for r in last)
rows = load('readout.json')
by_key = {(r['case_index'], r['method']): r for r in rows}
assert len(rows) == len(by_key) == 384
old_root = Path('out/2026-10-01_032642_jlens-one-pass')
old = json.loads((old_root / 'readout.json').read_text())
assert cases == json.loads((old_root / 'cases.json').read_text())
assert len(old) == 288 and all(by_key[r['case_index'], r['method']] == r for r in old)
for name in ('pursuit_records.json', 'pursuit_diagnostics.json'):
    assert load(name) == json.loads((old_root / name).read_text())
records, diagnostics = load('gradient_pursuit_records.json'), load('gradient_pursuit_diagnostics.json')
assert len(records) == 24 and len(diagnostics) == 16
masks = load('pursuit_masks.json')
assert masks == json.loads((reference / 'pool_masks.json').read_text())
model_dir = Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
tok = Tokenizer.from_file(str(model_dir / 'tokenizer.json'))
config = json.loads((model_dir / 'config.json').read_text())
assert config['tie_word_embeddings'] and config['text_config']['tie_word_embeddings']
vocab = [tok.decode([i], skip_special_tokens=False) for i in range(config['text_config']['vocab_size'])]
vocab_norm = [v.strip().lower() for v in vocab]


def prompt_mask(text):
    words = set(re.findall(r'\w+', text.lower()))
    prefixes = {w[:j] for w in words for j in range(3, len(w) + 1)}
    return [i for i, v in enumerate(vocab_norm) if v and (v in words or v in prefixes)]


@cache
def labels(word):
    return frozenset(i for i, v in enumerate(vocab_norm) if len(v) >= min(3, len(word)) and word.lower().startswith(v))


def checked_labels(case, text):
    hidden = set().union(*(labels(a) for a in case['hidden_aliases']))
    said = set().union(*(labels(a) for a in case['answer_aliases']))
    words = set(re.findall(r'[^\W_]+', text.lower()))
    actual = set().union(*(labels(a) for a in words))
    hidden_is_said = any(a.casefold() in words for a in case['hidden_aliases'])
    positives, negatives = hidden - actual, actual - hidden
    actual_evaluable = hidden_is_said or bool(positives and negatives and all(labels(a) for a in words))
    if any(re.search(r'\b' + re.escape(a) + r'\b', text, re.I) for a in case['answer_aliases']):
        negatives |= said - hidden
    evaluable = hidden_is_said or bool(actual_evaluable and positives and negatives)
    return sorted(positives), sorted(negatives), evaluable, hidden_is_said


special = set(load('tokenizer_special_ids.json')['r2_excluded_ids'])
clues = ('Christmas Day', 'Thor', 'deciduous trees shed their leaves', 'poisoned in the story of Snow White',
         'played by Sherlock Holmes', "Danish prince asks 'To be, or not to be'", 'lightest chemical element',
         'formed by joining three non-collinear points')
for i, case in enumerate(cases['cases']):
    prompt = cases['prefix'] + case['prompt']
    encoded = tok.encode(prompt, add_special_tokens=False)
    span = spans[i]
    assert encoded.ids == span['input_ids'] and [list(x) for x in encoded.offsets] == span['offsets']
    positions = [p for p, (start, end) in enumerate(encoded.offsets)
                 if len(cases['prefix']) <= start < end <= len(prompt)
                 and not encoded.special_tokens_mask[p] and encoded.ids[p] not in special]
    assert positions == span['positions'] and prompt == traces[i]['prompt']
    assert prompt_mask(prompt) == masks[i]['prompt_mask_ids']
    for record in (r for r in diagnostics if r['case_index'] == i):
        assert prompt.count(clues[i]) == 1 and record['clue'] == clues[i]
        expected = positions[2] if record['kind'] == 'early-prefix' else max(p for p in positions if encoded.offsets[p][1] <= prompt.index(clues[i]))
        assert record['position'] == expected
        assert record['consumed_prefix'] == prompt[:encoded.offsets[expected][1]]
        assert encoded.offsets[expected][1] <= prompt.index(clues[i])
        assert prompt_mask(record['consumed_prefix']) == record['prompt_mask_ids']

index = json.loads((model_dir / 'model.safetensors.index.json').read_text())['weight_map']
key = 'model.language_model.norm.weight'
with safe_open(model_dir / index[key], framework='pt', device='cpu') as f:
    gain = 1. + f.get_tensor(key).float()
all_ids = sorted({t for record in records + diagnostics for update in record['updates'] for t in update['support_ids']} |
                 {t for row in rows if 'selected_ids' in row for t in row['selected_ids']})
key = 'model.language_model.embed_tokens.weight'
with safe_open(model_dir / index[key], framework='pt', device='cpu') as f:
    weight_rows = torch.cat([f.get_slice(key)[i:i+1] for i in all_ids])
lens_path = Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt')
with lens_path.open('rb') as stream:
    assert hashlib.file_digest(stream, 'sha256').hexdigest() == '1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e'
J = torch.load(lens_path, map_location='cpu', weights_only=True)['J'][23].double()
raw_plain = (weight_rows.float() * gain).double()
raw_j = raw_plain @ J
raw_directions = {'J24': raw_j, 'plain24': raw_plain, 'plain27': raw_plain}
directions = {'J24': raw_j / raw_j.norm(dim=-1, keepdim=True), 'plain24': raw_plain / raw_plain.norm(dim=-1, keepdim=True)}
directions['plain27'] = directions['plain24']
id_to_row = {token: i for i, token in enumerate(all_ids)}
max_gradient_error = max_step_error = max_coefficient_error = max_residual_error = max_dot_error = max_auc_error = 0.
decreasing_updates = boundary_hits = 0
for record in records + diagnostics:
    i = record['case_index']
    diagnostic = 'kind' in record
    representation = 'J24' if diagnostic else record['representation']
    position = record['position'] if diagnostic else -1
    state = states[i][27 if representation == 'plain27' else 24][position].double()
    residual = state.clone()
    atoms = directions[representation]
    coefficients = defaultdict(lambda: torch.tensor(0., dtype=torch.float32))
    assert math.isclose(record['original_state_norm'], float(state.norm()), rel_tol=1e-10, abs_tol=1e-10)
    assert len(record['steps_selected_ids']) == len(record['updates']) <= 32
    assert len(record['residual_norms']) == len(record['updates']) + 1
    support = set()
    tolerance = 32 * torch.finfo(torch.float32).eps * max(1., float(state.norm()) ** 2)
    assert math.isclose(tolerance, record['energy_tolerance'], rel_tol=1e-12, abs_tol=1e-14)
    for step, (token, update) in enumerate(zip(record['steps_selected_ids'], record['updates'], strict=True)):
        assert update['added_id'] == token
        if token is not None:
            assert token not in support
            support.add(token)
        ids = sorted(support)
        assert ids == update['support_ids']
        before = torch.tensor([float(coefficients[t]) for t in ids], dtype=torch.float32)
        assert before.tolist() == update['before']
        local_atoms = atoms[[id_to_row[t] for t in ids]]
        expected_q = local_atoms @ residual
        expected_q[(before == 0) & (expected_q < 0)] = 0
        q = torch.tensor(update['direction'], dtype=torch.float32)
        error = float((q.double() - expected_q).abs().max())
        max_gradient_error = max(max_gradient_error, error)
        assert error <= 2e-5 * (1 + float(expected_q.abs().max())), (i, representation, step, 'gradient', error)
        if token is not None:
            assert q[ids.index(token)] > 0
        p = q.double() @ local_atoms
        numerator, denominator = float(residual @ p), float(p @ p)
        assert numerator > 0 and denominator > 0
        bounds = torch.full_like(before, torch.inf, dtype=torch.float64)
        negative = q < 0
        bounds[negative] = -before[negative].double() / q[negative].double()
        bound = float(bounds.min())
        reported_bound = update['max_feasible_step']
        if math.isfinite(bound):
            assert math.isclose(reported_bound, bound, rel_tol=1e-12, abs_tol=1e-12)
        else:
            assert reported_bound is None
        alpha = update['step_size']
        expected_alpha = min(numerator / denominator, bound)
        error = abs(alpha - expected_alpha)
        max_step_error = max(max_step_error, error)
        assert alpha > 0 and error <= 2e-5 * (1 + abs(expected_alpha)), (i, representation, step, 'step', error)
        expected_after = before + alpha * q
        if reported_bound == alpha:
            expected_after[int(bounds.argmin())] = 0
        expected_after.clamp_min_(0)
        after = torch.tensor(update['after'], dtype=torch.float32)
        assert bool((after >= 0).all())
        error = float((after - expected_after).abs().max())
        max_coefficient_error = max(max_coefficient_error, error)
        assert error <= 2e-6 * (1 + float(after.abs().max())), (i, representation, step, 'coefficients', error)
        if reported_bound == alpha:
            assert after[int(bounds.argmin())] == 0
        decreasing_updates += int(bool((after < before).any()))
        boundary_hits += int(((before > 0) & (after == 0)).sum())
        for t, amount in zip(ids, after, strict=True):
            coefficients[t] = amount
        residual = state - after.double() @ local_atoms
        assert math.isclose(float(residual.norm()), record['residual_norms'][step + 1], rel_tol=2e-5, abs_tol=2e-5)
        assert record['residual_norms'][step+1] ** 2 <= record['residual_norms'][step] ** 2 + tolerance
    coefficients = {t: a for t, a in coefficients.items() if a > 0}
    assert sorted(coefficients) == record['active_ids']
    assert [float(coefficients[t]) for t in sorted(coefficients)] == record['coefficients']
    assert [vocab[t] for t in record['active_ids']] == record['active_tokens']
    normalized = [float(coefficients[t].double() / state.norm()) for t in sorted(coefficients)]
    assert torch.allclose(torch.tensor(normalized), torch.tensor(record['normalized_coefficients']), atol=1e-10, rtol=1e-7)
    masked = set(record['prompt_mask_ids'] + record['output_mask_ids']) if diagnostic else set(masks[i]['prompt_mask_ids'] + masks[i]['output_mask_ids'])
    selected = sorted((t for t in coefficients if t not in masked), key=lambda t: (-float(coefficients[t]), t))
    assert selected == record['selected_ids'] and len(selected) == record['postmask_cardinality']
    assert [vocab[t] for t in selected] == record['selected_tokens']
    if diagnostic:
        saved_residual = torch.tensor(record['residual'], dtype=torch.float64)
    else:
        tensors = torch.load(root / 'gradient_pursuit_tensors' / f'{i:03d}-{representation}.pt', map_location='cpu', weights_only=True)
        saved_residual = tensors['residual'].double()
        sparse = tensors['scores']['pursuit']
        expected = torch.full_like(sparse, -torch.inf)
        for t in selected:
            expected[t] = coefficients[t].double() / state.norm()
        assert torch.allclose(sparse, expected, atol=1e-10, rtol=1e-7)
        text = tok.decode(traces[i]['token_ids'], skip_special_tokens=False)
        positives, negatives, evaluable, spoken = checked_labels(cases['cases'][i], text)
        old_tensors = torch.load(root / 'pursuit_tensors' / f'{i:03d}-{representation}.pt', map_location='cpu', weights_only=True)
        assert all(torch.equal(tensors['scores'][k], old_tensors['scores'][k]) for k in ('raw-dot full32', 'unit-dot full32'))
        for variant, score_key in (('pursuit', 'pursuit'), ('raw-dot matched', 'raw-dot full32'),
                ('unit-dot matched', 'unit-dot full32'), ('budget matching pursuit', 'pursuit')):
            budget = variant == 'budget matching pursuit'
            score = (old_tensors if budget else tensors)['scores'][score_key]
            method = f'end-pass gradient-budget matching pursuit {representation}' if budget else f'end-pass gradient {variant} {representation}'
            row = by_key[i, method]
            n = len(selected)
            top = [t for t in score.argsort(descending=True, stable=True)[:n].tolist() if torch.isfinite(score[t])]
            assert top == row['selected_ids'] and [vocab[t] for t in top] == row['top32']
            assert row['return_limit'] == n and row['returned_cardinality'] == len(top)
            assert row['baseline_generation'] == text
            if variant in ('raw-dot matched', 'unit-dot matched'):
                expected_directions = raw_directions[representation] if variant.startswith('raw-dot') else atoms
                for token in top:
                    expected_dot = float(expected_directions[id_to_row[token]] @ state)
                    dot_error = abs(expected_dot - float(score[token]))
                    max_dot_error = max(max_dot_error, dot_error)
                    assert dot_error <= 2e-5 * (1 + abs(expected_dot)), (i, representation, variant, token, dot_error)
            passed = evaluable and not spoken and bool(set(top) & set(positives)) and not bool(set(top) & set(negatives))
            assert bool(passed) == row['alias_checked_pass']
            auc = None
            if evaluable and not spoken:
                x, y = score[positives, None], score[negatives][None, :]
                auc = (2 * int((x > y).sum()) + int((x == y).sum())) / (2 * x.numel() * y.numel())
            if auc is None:
                assert row['alias_checked_auroc'] is None
            else:
                auc_error = abs(auc - row['alias_checked_auroc'])
                max_auc_error = max(max_auc_error, auc_error)
                assert auc_error <= 1e-7, (i, representation, variant, auc, row['alias_checked_auroc'])
    error = float((residual - saved_residual).abs().max())
    max_residual_error = max(max_residual_error, error)
    assert error <= 5e-5 * (1 + float(state.abs().max())), (i, representation, error)
primary, control = 'end-pass gradient pursuit J24', 'end-pass gradient unit-dot matched J24'
gains = [i for i in range(8) if by_key[i, primary]['alias_checked_pass'] and not by_key[i, control]['alias_checked_pass']]
losses = [i for i in range(8) if by_key[i, control]['alias_checked_pass'] and not by_key[i, primary]['alias_checked_pass']]
new_vs_matching = [i for i in range(8) if by_key[i, primary]['alias_checked_pass'] and not by_key[i, 'end-pass pursuit J24']['alias_checked_pass']]
assert new_vs_matching == selection['new_vs_native_matching_pursuit']
candidates = [i for i in new_vs_matching if not any(set(r['active_ids']) & set().union(*(labels(a) for a in cases['cases'][i]['hidden_aliases']))
    for r in diagnostics if r['case_index'] == i)]
assert gains == selection['paired_gains'] and losses == selection['paired_losses']
assert candidates == selection['new_alias_gain_candidates_absent_from_unmasked_priors']
assert selection['net_paired_gain'] == len(gains) - len(losses)
assert selection['numeric_prerequisite_passed'] == (len(gains) > len(losses) and bool(candidates))
report = {'status': 'PASS source/cache/tokenization, selected-direction reconstruction, masks, full-vocabulary saved-score rankings and alias scoring',
          'checked_old_rows': 288, 'checked_new_rows': 96, 'checked_decompositions': 40,
          'max_gradient_error': max_gradient_error, 'max_step_error': max_step_error, 'max_coefficient_error': max_coefficient_error,
          'updates_with_decreasing_coefficients': decreasing_updates, 'positive_coefficients_reaching_zero': boundary_hits, 'max_residual_error': max_residual_error, 'max_selected_dot_error': max_dot_error, 'max_auc_error_vs_exact_pair_count': max_auc_error,
          'limits': 'No transformer inference, independent full-vocabulary dictionary/greedy-step optimality, raw/unit-dot derivation for unselected atoms, diagnostic greedy-mask derivation, hardware trace or semantic certification. Final ranks reconstruct saved scores, not independently derived logits.'}
(root / 'verification.json').write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))
