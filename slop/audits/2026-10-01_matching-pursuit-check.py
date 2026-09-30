"""CPU algebra checks of production helpers; no model inference. — PI/OpenAI"""
import ast
import hashlib
import re
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

source = Path('scripts/english/08_jlens_one_pass.py')
names = {'unit_dictionary', 'nonnegative_matching_pursuit', 'pursuit_readout_scores', 'pursuit_diagnostic_positions'}
print('source_sha256=' + hashlib.sha256(source.read_bytes()).hexdigest(), flush=True)
module = ast.parse(source.read_text())
namespace = {'torch': torch}
exec(compile(ast.Module([n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names], []), str(source), 'exec'), namespace)
unit_dictionary = namespace['unit_dictionary']
pursuit = namespace['nonnegative_matching_pursuit']
torch.set_num_threads(2)


def independent(state, atoms, eligible, steps=32):
    residual = state.numpy().astype(np.float64).copy()
    dictionary = atoms.numpy().astype(np.float64)
    coefficients = np.zeros(len(dictionary))
    indices = []
    for _ in range(steps):
        values = np.array([np.dot(row, residual) if keep else -np.inf for row, keep in zip(dictionary, eligible.tolist(), strict=True)])
        token = int(np.argmax(values))
        if values[token] <= 0:
            break
        coefficients[token] += values[token]
        residual -= values[token] * dictionary[token]
        indices.append(token)
    return coefficients, residual, indices


def check(state, vectors, steps=32):
    atoms, norms, eligible = unit_dictionary(vectors)
    assert torch.equal(eligible, (vectors != 0).any(-1))
    assert torch.allclose(atoms[eligible].norm(dim=-1), torch.ones(int(eligible.sum())), atol=1e-6)
    assert torch.equal(atoms[~eligible], torch.zeros_like(atoms[~eligible]))
    original = state.clone()
    coefficients, residual, trace = pursuit(state, atoms, eligible, steps)
    expected, expected_residual, indices = independent(state, atoms, eligible, steps)
    assert trace['selected_ids'] == indices, (trace['selected_ids'], indices)
    assert np.allclose(coefficients.numpy(), expected, atol=2e-6, rtol=2e-5)
    assert np.allclose(residual.numpy(), expected_residual, atol=2e-6, rtol=2e-5)
    assert torch.equal(state, original)
    assert (coefficients >= 0).all() and not coefficients[~eligible].any()
    assert torch.allclose(coefficients @ atoms + residual, state, atol=2e-6, rtol=2e-5)
    energy = np.square(trace['residual_norms'])
    assert (np.diff(energy) <= 1e-6 * (1 + energy[:-1])).all()
    accumulated = torch.zeros_like(coefficients)
    for token, amount in zip(trace['selected_ids'], trace['increments'], strict=True):
        assert amount > 0
        accumulated[token] += amount
    assert torch.equal(accumulated, coefficients)
    assert len(trace['residual_norms']) == len(trace['selected_ids']) + 1
    return coefficients, trace


for seed in (0, 1):
    generator = torch.Generator().manual_seed(seed)
    vectors = torch.randn(24, 7, generator=generator)
    vectors[4] = 0
    state = torch.randn(7, generator=generator)
    check(state, vectors)
    atoms, _, eligible = unit_dictionary(vectors)
    scaled_atoms, _, scaled_eligible = unit_dictionary(vectors * torch.exp(torch.randn(24, 1, generator=generator)))
    assert torch.equal(eligible, scaled_eligible) and torch.allclose(atoms, scaled_atoms, atol=1e-6)
    print(f'PASS seed{seed}: independent float64 reference, reconstruction, monotone energy, accumulation, positive scale invariance', flush=True)

coefficients, trace = check(torch.tensor([1., 1.]), torch.tensor([[1., 0.], [0., 1.], [2., 0.], [0., 0.]]))
assert trace['selected_ids'] == [0, 1] and torch.equal(coefficients, torch.tensor([1., 1., 0., 0.]))
coefficients, trace = check(torch.tensor([-1., 1.]), torch.tensor([[1., 0.], [.6, .8], [-1., 0.]]), steps=7)
assert len(trace['selected_ids']) == 7 and len(set(trace['selected_ids'])) < 7
for state, vectors in ((torch.tensor([-1., -2.]), torch.eye(2)),
                       (torch.zeros(2), torch.eye(2)),
                       (torch.ones(2), torch.zeros(3, 2))):
    coefficients, trace = check(state, vectors)
    assert not coefficients.any() and not trace['selected_ids']
check(torch.ones(2), torch.tensor([[1e-40, 1e-40], [0., 0.]]), steps=1)
for bad in (float('nan'), float('inf')):
    try:
        unit_dictionary(torch.tensor([[bad, 1.]]))
    except AssertionError:
        pass
    else:
        raise AssertionError('Nonfinite dictionary accepted')
    atoms, _, eligible = unit_dictionary(torch.eye(2))
    try:
        pursuit(torch.tensor([bad, 1.]), atoms, eligible)
    except AssertionError:
        pass
    else:
        raise AssertionError('Nonfinite state accepted')
print('PASS ties, repeated atoms, exact-zero exclusion without tiny-norm cutoff, no-positive stop, zero state/dictionary, nonfinite rejection', flush=True)
score_pursuit = namespace['pursuit_readout_scores']
vectors = torch.tensor([[1., 0.], [.6, .8], [-1., 0.], [0., 0.]])
dictionary = unit_dictionary(vectors)
state = torch.tensor([-1., 1.])
no_mask = torch.zeros(4, dtype=torch.bool)
values, limits, record, residual = score_pursuit(state, dictionary, no_mask)
assert record['postmask_cardinality'] == 2
assert limits == {'pursuit': 2, 'raw-dot matched': 2, 'unit-dot matched': 2, 'raw-dot full32': 32, 'unit-dot full32': 32}
assert torch.isneginf(values['pursuit'][[0, 3]]).all()
assert ((values['pursuit'][0] == values['pursuit'][3]).float() * .5).item() == .5
for mask in (torch.tensor([False, True, False, False]), torch.ones(4, dtype=torch.bool)):
    masked_values, masked_limits, masked_record, masked_residual = score_pursuit(state, dictionary, mask)
    assert masked_record['steps_selected_ids'] == record['steps_selected_ids']
    assert masked_record['increments'] == record['increments'] and torch.equal(masked_residual, residual)
    n = masked_record['postmask_cardinality']
    assert masked_limits['raw-dot matched'] == masked_limits['unit-dot matched'] == n
    for key in ('pursuit', 'raw-dot matched', 'unit-dot matched'):
        top = masked_values[key].argsort(descending=True, stable=True)[:n]
        assert len(top) == n and not mask[top].any()
    if mask.all():
        assert n == 0 and not masked_record['selected_ids']
zero_values, _, zero_record, _ = score_pursuit(torch.zeros(2), dictionary, no_mask)
assert torch.isneginf(zero_values['pursuit']).all() and zero_record['normalized_coefficients'] == []
positions = namespace['pursuit_diagnostic_positions']('Fact: The Thor clue',
    {'positions': [0, 1, 2, 3, 4], 'offsets': [[0,4], [4,5], [5,9], [9,14], [14,19]]}, 'Thor')
assert positions == {'early-prefix': 2, 'pre-clue': 2}
for prompt, clue in (('Fact: The Thor Thor clue', 'Thor'), ('Fact: The clue', 'Thor')):
    try:
        namespace['pursuit_diagnostic_positions'](prompt, {'positions': [], 'offsets': []}, clue)
    except AssertionError:
        pass
    else:
        raise AssertionError('Ambiguous/missing clue accepted')
print('PASS post-decomposition masking, active-only ranks, inactive AUROC ties, matched cardinalities including zero, zero-state normalization, clue uniqueness/boundary', flush=True)
for scale in (1e-30, 1e20):
    tiny_or_large = torch.full((2,), scale)
    legacy_norm = float(tiny_or_large.norm())
    values, _, record, _ = score_pursuit(tiny_or_large, unit_dictionary(torch.eye(2)), torch.zeros(2, dtype=torch.bool))
    assert np.isfinite(record['original_state_norm']) and record['original_state_norm'] > 0
    assert np.allclose(values['pursuit'].numpy(), np.full(2, 1 / np.sqrt(2)), atol=1e-12)
    print(f'PASS state scale{scale:g}: float32 norm={legacy_norm!r}, float64 norm={record["original_state_norm"]!r}; finite normalized coefficients', flush=True)

rank_tree = ast.parse(Path('scripts/english/03_selector_search.py').read_text())
rank_function = next(n for n in rank_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'ranks_of_best')
rank_scope = {'torch': torch, 'Tensor': torch.Tensor}
exec(compile(ast.Module([rank_function], []), 'production-rank', 'exec'), rank_scope)
main_node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
scoring_loop = next(n for n in ast.walk(main_node) if isinstance(n, ast.For) and ast.unparse(n.target) == '(name, score)')
scorer = compile(ast.Module([scoring_loop], []), 'production-scoring-loop', 'exec')

def score_fixture(values, expected_pass, expected_auc, limit=32, evaluable=True, hidden_is_said=False):
    scope = dict(torch=torch, re=re, s4=SimpleNamespace(ranks_of_best=rank_scope['ranks_of_best']),
        scores={'fixture': torch.tensor(values)}, pursuit_limits={'fixture': limit}, mask=torch.zeros(4, dtype=torch.bool),
        hidden=[0], said=[1], actual_hidden_ids=[0], actual_said_ids=[1], checked_hidden=[0], checked_said=[1],
        hidden_alias_ids=[0], said_alias_ids=[1], input_label_ids={2}, components={}, kl_names=set(),
        pool_data={}, polar_data={}, readouts=[], case_index=0, generated_ids=[1],
        vocab=[' hidden', ' said', ' input', ' unused'], case={'prompt': 'input', 'said_text': 'said'},
        concept='hidden', answer='said', actual_evaluable=evaluable, checked_evaluable=evaluable,
        hidden_is_said=hidden_is_said, canonical_evaluable=True, hidden_aliases=['hidden'], answer_aliases=['said'],
        actual_words=['said'], expected_observed=True, unscorable_actual_words=[], ambiguous_intended=[], ambiguous_actual=[])
    exec(scorer, scope)
    row = scope['readouts'][0]
    assert row['alias_checked_pass'] == expected_pass and row['actual_pass'] == expected_pass, row
    assert row['alias_checked_auroc'] == expected_auc and row['token_pair_auroc'] == expected_auc, row
    return row

inf = -float('inf')
assert score_fixture([2., inf, inf, inf], True, 1.)['alias_checked_hidden_found']
score_fixture([2., 1., inf, inf], False, 1.)
score_fixture([2., inf, 1., inf], False, 1.)
score_fixture([inf, inf, inf, inf], False, .5)
score_fixture([2., 2., inf, inf], False, .5)
score_fixture([2., inf, inf, inf], False, None, evaluable=False)
score_fixture([2., inf, inf, inf], False, None, hidden_is_said=True)
row = score_fixture([2., inf, inf, inf], False, 1., limit=0)
assert row['r_hidden'] == 0 and row['returned_cardinality'] == 0 and not row['alias_checked_hidden_found']
print('PASS actual production scorer: genuine recovery, said/input leaks, tied inactive/active AUROC, undefined/spoken-hidden rejection, zero-return control despite rank0', flush=True)
for seed in (0, 1):
    generator = torch.Generator().manual_seed(seed)
    vectors = torch.randn(8197, 17, generator=generator)
    vectors[[0, 4095, 4096, 8192]] = 0
    vectors[8196] *= 1e-40
    expected_norms = torch.linalg.vector_norm(vectors, dim=-1, dtype=torch.float64)
    expected_atoms = (vectors / expected_norms.masked_fill(expected_norms == 0, 1)[:, None]).float()
    atoms, norms, eligible = unit_dictionary(vectors)
    assert torch.equal(norms, expected_norms) and torch.equal(atoms, expected_atoms)
    assert torch.equal(eligible, expected_norms > 0)
    print(f'PASS seed{seed}:8197-row batch-boundary/last-slice/zero/tiny normalization exactly equals dense float64 formula', flush=True)
print('Allocation calculation:248320*2560*8=5085593600 bytes (observed OOM);4096*2560*8=83886080 bytes per float64 tile; total GPU peak still untested', flush=True)
print('LIMIT: helper/scorer fixtures; semantic performance and production4B parity remain untested.', flush=True)
