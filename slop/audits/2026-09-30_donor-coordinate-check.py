"""CPU algebra checks for the actual validation helper. — PI/OpenAI"""

import ast
from pathlib import Path

import torch

source = Path("scripts/english/08_jlens_one_pass.py")
node = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "donor_margins")
namespace = {"torch": torch}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
margins = namespace["donor_margins"]
for seed in (0, 1):
    torch.manual_seed(seed)
    u = torch.randn(2560)
    u /= u.norm()
    center, e_ref, e_current = torch.randn(3, 2560)
    h = torch.randn(7, 2560).to(torch.bfloat16)
    e = torch.randn(7, 2560).to(torch.bfloat16)
    raw, corrected = margins(h, e, center, u, e_ref)
    direct = ((h.float() - e.float()) - (center - e_ref)) @ u
    assert torch.allclose(corrected, direct, atol=2e-5, rtol=2e-5)
    raw, corrected = margins(h, e_ref.expand_as(h), center, u, e_ref)
    assert torch.equal(raw, corrected)
    residual_context = center - e_ref
    h_pair = torch.stack((residual_context - u + e_current, residual_context + u + e_current))
    raw, corrected = margins(h_pair, e_current.expand_as(h_pair), center, u, e_ref)
    assert torch.allclose(corrected, torch.tensor([-1., 1.]), atol=2e-5, rtol=2e-5)
    assert torch.allclose(raw[1] - raw[0], corrected[1] - corrected[0], atol=2e-5, rtol=2e-5)
    changed = h_pair - 2 * corrected.clamp_max(0).unsqueeze(-1) * u
    _, after = margins(changed, e_current.expand_as(h_pair), center, u, e_ref)
    assert torch.allclose(after, corrected.abs(), atol=2e-5, rtol=2e-5)
    assert torch.equal(changed[1], h_pair[1])
    assert torch.allclose(changed[0], h_pair[1], atol=2e-5, rtol=2e-5)
    print(f"PASS seed={seed}: direct formula, It identity, embedding-origin toy, paired ordering and fold")
