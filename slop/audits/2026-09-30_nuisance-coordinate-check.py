"""CPU checks of the production nuisance-coordinate fit; no model inference. — PI/OpenAI"""

import ast
import json
from pathlib import Path

import torch

torch.set_num_threads(1)
source = Path('scripts/english/08_jlens_one_pass.py')
node = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'nuisance_coordinate')
namespace = {'torch': torch}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
fit = namespace['nuisance_coordinate']
for seed in (0, 1):
    torch.manual_seed(seed)
    means = torch.randn(8, 32, dtype=torch.float64)
    direction = torch.randn(32, dtype=torch.float64)
    direction /= direction.norm()
    fitted = fit(means, direction)
    basis = fitted['nuisance_basis']
    assert torch.allclose(basis @ basis.T, torch.eye(7, dtype=torch.float64), atol=1e-12, rtol=1e-12)
    centered = means - means.mean(0)
    assert torch.allclose(centered, centered @ basis.T @ basis, atol=1e-12, rtol=1e-12)
    assert torch.allclose(basis @ fitted['direction'].double(), torch.zeros(7, dtype=torch.float64), atol=1e-7, rtol=0)
    margins = (means.float() - fitted['center']) @ fitted['direction']
    assert float(margins.abs().max()) < 2e-6
    assert abs(float(fitted['direction'].norm()) - 1) < 1e-6
    for bad_means, bad_direction in [(means[:1].expand_as(means), direction), (means, basis[0])]:
        try:
            fit(bad_means, bad_direction)
        except AssertionError:
            pass
        else:
            raise AssertionError('rank-deficient or vanishing-direction input was accepted')
    print(f'PASS seed={seed}: span reconstruction, orthogonality, unit norm, numerical aborts; zero training midpoint margins are algebraic', flush=True)

root = Path('out/2026-09-30_163330_jlens-one-pass')
states = torch.load(root / 'states.pt', weights_only=True, map_location='cpu')
coordinate = torch.load(root / 'coordinate.pt', weights_only=True, map_location='cpu')
keys = [p['key'] for p in json.loads((root / 'result.json').read_text())['pairs']]
dogs = torch.stack([states[k+'-dog']['hidden'][-1].double() for k in keys])
spiders = torch.stack([states[k+'-spider']['hidden'][-1].double() for k in keys])
fitted = fit((dogs+spiders)/2, coordinate['direction'])
dog_margins = (dogs.float()-fitted['center']) @ fitted['direction']
spider_margins = (spiders.float()-fitted['center']) @ fitted['direction']
print(json.dumps({'role':'development fit check, NOT validation or causal success',
                  'singular_values': fitted['singular_values'].tolist(),
                  'retained_direction_norm': fitted['retained_direction_norm'],
                  'rank_tolerance': fitted['rank_tolerance'], 'norm_tolerance': fitted['norm_tolerance'],
                  'training_brackets': int(((dog_margins<0)&(spider_margins>0)).sum()),
                  'max_training_midpoint_margin': float(((dog_margins+spider_margins)/2).abs().max()),
                  'dog_margins': dog_margins.tolist(), 'spider_margins': spider_margins.tolist()}, indent=1), flush=True)
