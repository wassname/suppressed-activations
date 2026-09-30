"""Independent coefficient-update checks; no model inference. — PI/OpenAI"""
import ast
import hashlib
import math
from pathlib import Path

import numpy as np
import torch

torch.set_num_threads(2)
source = Path('scripts/english/08_jlens_one_pass.py')
text = source.read_text()
names = {'unit_dictionary', 'nonnegative_matching_pursuit', 'nonnegative_gradient_pursuit', 'pursuit_readout_scores'}
module = ast.Module(body=[x for x in ast.parse(text).body if isinstance(x, ast.FunctionDef) and x.name in names], type_ignores=[])
ns = {'torch': torch, 'math': math}
exec(compile(module, str(source), 'exec'), ns)
unit, mp, gp, score = [ns[k] for k in ('unit_dictionary', 'nonnegative_matching_pursuit', 'nonnegative_gradient_pursuit', 'pursuit_readout_scores')]
print('source_sha256=' + hashlib.sha256(source.read_bytes()).hexdigest(), flush=True)


def reference(h, dictionary, eligible, steps=32):
    h, dictionary = h.numpy().astype('float64'), dictionary.numpy().astype('float64')
    a = np.zeros(len(dictionary))
    support = set()
    residual = h.copy()
    selections = []
    for _ in range(steps):
        g = dictionary @ residual
        available = [i for i in range(len(g)) if eligible[i] and i not in support and g[i] > 0]
        new = max(available, key=lambda i: (g[i], -i)) if available else None
        if new is not None:
            support.add(new)
        q = np.array([g[i] if a[i] > 0 else max(g[i], 0) if i in support else 0 for i in range(len(a))])
        assert all(q[i] == 0 for i in range(len(a)) if i not in support)
        if np.all(q == 0):
            break
        p = q @ dictionary
        step = (residual @ p) / (p @ p)
        bounds = np.full(len(a), np.inf)
        bounds[q < 0] = -a[q < 0] / q[q < 0]
        step = min(step, min(bounds))
        previous = a.copy()
        a = a + step * q
        a[bounds == step] = 0
        assert min(a) >= -1e-12
        a = np.maximum(a, 0)
        residual = h - a @ dictionary
        selections.append(new)
        if np.array_equal(a, previous):
            break
    return a, residual, selections


def validate(h, dictionary, eligible):
    a, residual, trace = gp(h, dictionary, eligible)
    expected_a, expected_r, expected_selected = reference(h, dictionary, eligible)
    assert np.allclose(a.numpy(), expected_a, atol=3e-5, rtol=3e-5), (a, expected_a)
    assert np.allclose(residual.numpy(), expected_r, atol=3e-5, rtol=3e-5)
    assert trace['selected_ids'] == expected_selected, (trace['selected_ids'], expected_selected)
    assert torch.allclose(h, a @ dictionary + residual, atol=2e-6, rtol=2e-6)
    assert all(y*y <= x*x + trace['energy_tolerance'] for x, y in zip(trace['residual_norms'], trace['residual_norms'][1:]))
    assert (a >= 0).all() and (a[~eligible] == 0).all()
    for step in trace['updates']:
        before, after, direction = [np.array(step[k]) for k in ('before', 'after', 'direction')]
        assert np.all(direction[before == 0] >= 0)
        assert np.all(after >= 0)
        if step['max_feasible_step'] is not None:
            assert step['step_size'] <= step['max_feasible_step']
    return a, residual, trace


for seed in (0, 1):
    torch.manual_seed(seed)
    dictionary, _, eligible = unit(torch.randn(9, 13))
    h = (torch.rand(9) + .2) @ dictionary
    a, residual, trace = validate(h, dictionary, eligible)
    assert any(any(y < x for x, y in zip(u['before'], u['after'])) for u in trace['updates'])
    scaled_a, scaled_r, _ = gp(h * 3, dictionary, eligible)
    assert torch.allclose(scaled_a, a * 3, atol=1e-4, rtol=1e-4)
    assert torch.allclose(scaled_r, residual * 3, atol=1e-4, rtol=1e-4)
    print(f'PASS seed{seed}: independent float64 updates, coefficient decreases, reconstruction, energy and scale', flush=True)

D, norms, eligible = unit(torch.tensor([[1., 0.], [.8, .6]]))
h = torch.tensor([.7, .9]) @ D
a, residual, trace = validate(h, D, eligible)
mp_a, mp_r, _ = mp(h, D, eligible)
assert residual.norm() < mp_r.norm() / 100
assert torch.allclose(a, torch.tensor([.7, .9]), atol=.002)
first_atom = trace['selected_ids'][0]
revised = trace['updates'][2]
index = revised['support_ids'].index(first_atom)
assert revised['after'][index] < revised['before'][index]
print(f'PASS correlated dictionary: residual GP={residual.norm():.6g}, MP={mp_r.norm():.6g}; active coefficients revised', flush=True)

boundary_D, _, boundary_eligible = unit(torch.tensor([[.6, .6, math.sqrt(.28)], [1., 0., 0.], [0., 1., 0.]]))
boundary_a, boundary_r, boundary_trace = gp(torch.tensor([1., 1., -.2]), boundary_D, boundary_eligible)
assert torch.equal(boundary_a, torch.tensor([0., 1., 1.]))
assert torch.equal(boundary_r, torch.tensor([0., 0., -.2]))
assert any(u['max_feasible_step'] is not None and u['step_size'] == u['max_feasible_step']
           and any(x > 0 and y == 0 for x, y in zip(u['before'], u['after'])) for u in boundary_trace['updates'])
print('PASS feasibility boundary: initially chosen out-of-plane atom reaches exact zero; support retained', flush=True)

D, norms, eligible = unit(torch.tensor([[1., 0.], [1., 0.], [0., 1.], [0., 0.]]))
a, residual, trace = validate(torch.tensor([1., .5]), D, eligible)
assert trace['selected_ids'][0] == 0 and a[3] == 0
for h in (torch.zeros(2), torch.tensor([-1., -1.])):
    a, residual, trace = validate(h, D, eligible)
    assert not bool((a > 0).any()) and torch.equal(residual, h)
for h in (torch.tensor([float('nan'), 1.]), torch.tensor([float('inf'), 1.])):
    try:
        gp(h, D, eligible)
    except AssertionError:
        pass
    else:
        raise AssertionError('Nonfinite state accepted')
print('PASS lowest-ID ties, zero atom/state, no-positive direction, nonfinite rejection', flush=True)

mask = torch.tensor([True, False, False, False])
h = torch.tensor([1., .5])
values, limits, record, residual = score(h, (D, norms, eligible), mask, solver=gp)
assert record['steps_selected_ids'][0] == 0 and 0 not in record['selected_ids']
assert record['postmask_cardinality'] == limits['pursuit'] == limits['unit-dot matched']
assert all(torch.isfinite(values['pursuit'][i]) for i in record['selected_ids'])
base = score(h, (D, norms, eligible), mask)
explicit = score(h, (D, norms, eligible), mask, solver=mp)
assert all(torch.equal(base[0][k], explicit[0][k]) for k in base[0]) and base[1:3] == explicit[1:3]
print('PASS masks applied after solver, positive-only output, matched limits and unchanged default matching pursuit', flush=True)
print('LIMIT: helper-only validation; production integration, GPU parity and semantic recovery remain untested', flush=True)
