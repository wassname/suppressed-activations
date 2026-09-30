"""Check production donor reflection algebra, not model semantics. — PI/OpenAI"""
import ast
from pathlib import Path
import torch

source = ast.parse(Path('scripts/english/08_jlens_one_pass.py').read_text())
function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'reflect_donor_side')
namespace = {'torch':torch}
exec(compile(ast.Module(body=[function], type_ignores=[]), '<production reflection>', 'exec'), namespace)
reflect = namespace['reflect_donor_side']
for seed in (0,1):
    torch.manual_seed(seed)
    source, target = torch.randn(2,2560)
    center = (source+target)/2
    direction = (target-source)/(target-source).norm()
    h = torch.randn(1,17,2560).to(torch.bfloat16).float()
    changed = reflect(h,center,direction)
    before, after = (h-center)@direction, (changed-center)@direction
    assert torch.allclose(after, before.abs(), atol=1e-5, rtol=1e-5)
    delta = changed-h
    assert torch.allclose(delta, (delta@direction).unsqueeze(-1)*direction, atol=1e-6, rtol=1e-5)
    assert torch.allclose(reflect(changed,center,direction), changed, atol=1e-6, rtol=1e-5)
    assert torch.equal(changed[before>=0],h[before>=0])
    assert torch.allclose(reflect(source,center,direction),target,atol=1e-6,rtol=1e-5)
    assert torch.equal(reflect(target,center,direction),target)
    assert torch.equal(reflect(center,center,direction),center)
    assert torch.allclose(reflect(target,center,-direction),source,atol=1e-6,rtol=1e-5)
    cast = changed.to(torch.bfloat16).float()
    error = ((cast-center)@direction-after).abs()
    assert (error <= (cast-changed).norm(dim=-1)+1e-5).all()
    noise = torch.randn(2560);noise/=noise.norm()
    random_delta = delta.norm(dim=-1,keepdim=True)*noise
    assert torch.allclose(random_delta.norm(dim=-1),delta.norm(dim=-1),atol=1e-6,rtol=1e-5)
    print(f'PASS seed={seed}: source->target, target unchanged, fold, idempotence, perpendicular preservation, BF16 bound, random norms')
donor=torch.load('out/2026-09-30_133218_jlens-one-pass/donors.pt',weights_only=True)
s,t=donor['means']['dog'],donor['means']['spider'];c=(s+t)/2;u=(t-s)/(t-s).norm()
assert torch.allclose(reflect(s,c,u),t,atol=1e-6,rtol=1e-5)
assert torch.equal(reflect(t,c,u),t)
print('PASS real generic donor endpoints; norm=',float((t-s).norm()),'margins=',float((s-c)@u),float((t-c)@u))
