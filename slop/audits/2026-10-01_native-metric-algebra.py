"""Held-scale projection algebra, including nonidentity J; no model inference. — PI/OpenAI"""
import ast
from pathlib import Path
import torch

torch.set_num_threads(4)
module=ast.parse(Path('scripts/english/08_jlens_one_pass.py').read_text())
node=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='native_metric_directions')
exec(compile(ast.Module(body=[node],type_ignores=[]),'production-direction','exec'))
for seed in (0,1):
    torch.manual_seed(seed);n=17
    w=torch.randn(n,dtype=torch.float64);gain=torch.linspace(.3,2,n,dtype=torch.float64)
    J=torch.randn(n,n,dtype=torch.float64)+torch.eye(n,dtype=torch.float64)
    y=torch.randn(n,dtype=torch.float64);c=.5*(y@w)
    d=native_metric_directions(w,gain,J)
    B=gain[:,None]*J;a=B.T@w
    native_delta=c*a/a.square().sum()
    assert torch.allclose(B@native_delta,c*d['J-lens'],atol=1e-12,rtol=1e-12)
    nuisance=torch.randn(n,dtype=torch.float64);nuisance-=a*(nuisance@a)/(a@a)
    assert (native_delta+nuisance).norm()>=native_delta.norm()
    for name,v in d.items():
        assert torch.allclose(v@w,torch.tensor(1.,dtype=w.dtype),atol=1e-12,rtol=1e-12),name
        assert torch.allclose((y-c*v)@w,.5*(y@w),atol=1e-12,rtol=1e-12)
    assert torch.allclose(d['plain24'],gain.square()*w/((gain*w).square().sum()),atol=1e-12,rtol=1e-12)
    assert torch.allclose(d['random0 J-lens'].norm(),d['J-lens'].norm(),atol=1e-12,rtol=1e-12)
    assert torch.allclose(native_metric_directions(w,gain,3.7*J)['J-lens'],d['J-lens'],atol=1e-12,rtol=1e-12)
    unit=native_metric_directions(w,torch.ones_like(gain),torch.eye(n,dtype=w.dtype))
    assert all(torch.equal(v,w/(w@w)) for v in unit.values())
    for bad_w,bad_gain,bad_J in [(w,gain,J*0),(w*0,gain,J),(w,gain*0,J)]:
        try:native_metric_directions(bad_w,bad_gain,bad_J);raise RuntimeError('zero sensitivity accepted')
        except AssertionError:pass
    print(f'PASS seed{seed}: nonidentity-J minimum-native-norm solution, coordinate equality, requested random norm, scale invariance, identity/zero-extra equivalence and explicit zero-sensitivity rejection.',flush=True)
