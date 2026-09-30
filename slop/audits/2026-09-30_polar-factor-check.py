"""Production polar-factor algebra only, not semantic evidence. -- PI/OpenAI"""
import ast
from pathlib import Path

import torch

torch.set_num_threads(1)
source=Path('scripts/english/08_jlens_one_pass.py')
node=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='orthogonal_polar_factor')
exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'))
for seed in (0,1):
    torch.manual_seed(seed)
    u=torch.linalg.qr(torch.randn(32,32,dtype=torch.float64)).Q
    v=torch.linalg.qr(torch.randn(32,32,dtype=torch.float64)).Q
    singular=torch.tensor([.1]*8+[1.]*16+[3.]*8,dtype=torch.float64)
    matrix=(u*singular)@v.T
    q,info=orthogonal_polar_factor(matrix)
    assert torch.allclose(q.double(),u@v.T,atol=1e-7,rtol=1e-7)
    x=torch.randn(7,32)
    assert torch.allclose((x@q.T).norm(dim=-1),x.norm(dim=-1),atol=1e-6,rtol=1e-6)
    q_scaled,_=orthogonal_polar_factor(matrix*8)
    assert torch.equal(q,q_scaled)
    assert torch.allclose(orthogonal_polar_factor(torch.eye(32))[0],torch.eye(32))
    reflection=torch.eye(32); reflection[0,0]=-1
    assert torch.equal(orthogonal_polar_factor(reflection)[0],reflection)
    for bad in (torch.zeros(32,32),torch.diag(torch.tensor([1.]*31+[0.]))):
        try:
            orthogonal_polar_factor(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('rank-deficient map accepted')
    print(f'PASS seed{seed}: known polar factor, repeated positive singular values, scale invariance, norm preservation, reflection retained, rank-deficient/zero rejected',flush=True)
print('PASS algebra only; readout integration and full-size decomposition are not yet tested',flush=True)
