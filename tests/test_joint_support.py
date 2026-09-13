# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""MAINTAINED regression: the non-complete joint-removal span (oat_sweep.joint_support)
must exist, be orthonormal at rank 8+8, and contain both injections. The cc25c2b
refactor deleted this path and every joint arm crashed on a dangling `Pu`; this test
would have caught it. Also pins the rem_cols selection in run_with_bundle's branch.
-- PI[glm-5p3-flash]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
import scripts.oat_sweep as oat


def test_joint_support_rank_and_orthonormality():
    torch.manual_seed(0)
    H = 2560  # real 4B hidden size
    Us8 = torch.linalg.qr(torch.randn(H, 8))[0].float()
    Ud8 = torch.linalg.qr(torch.randn(H, 8))[0].float()
    Pu = oat.joint_support(Us8, Ud8)
    assert Pu.shape == (H, 16), f"joint rank of two disjoint rank-8 bases should be 16, got {Pu.shape}"
    torch.testing.assert_close(Pu.T @ Pu, torch.eye(16), rtol=1e-4, atol=1e-4)


def test_joint_support_contains_injection():
    torch.manual_seed(1)
    H = 2560
    Us8 = torch.linalg.qr(torch.randn(H, 8))[0].float()
    Ud8 = torch.linalg.qr(torch.randn(H, 8))[0].float()
    Pu = oat.joint_support(Us8, Ud8)
    d = torch.randn(H)
    v = Ud8 @ (Ud8.T @ d)  # the injected direction v = Pd d
    cont = float((v - Pu @ (Pu.T @ v)).norm() / v.norm())
    assert cont < 1e-6, f"injection not contained in joint span: {cont}"


def test_complete_mode_uses_complete_edit_bases_not_joint_support():
    # the complete-rank arms keep the Pj branch: joint_support must not shadow it
    from dataclasses import replace
    torch.manual_seed(2)
    H = 2560
    U_s = torch.linalg.qr(torch.randn(H, 8))[0].float()
    U_d = torch.linalg.qr(torch.randn(H, 8))[0].float()
    cfg = replace(next(c for _, v, c in oat.SWEEP_CONFIGS["complete-rank"]() if v == "k8_C1.5"))
    Us_k, Ud_k, Pj, active = oat.complete_edit_bases(U_s, U_d, U_s, U_d, cfg)
    assert active, "complete-rank k8 arm must be active"
    # Pj is the support of the TRUNCATED pair, identical to joint_support(Us_k, Ud_k)
    torch.testing.assert_close(Pj, oat.joint_support(Us_k, Ud_k), rtol=1e-4, atol=1e-4)
