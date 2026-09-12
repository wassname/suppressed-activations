# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Exact minimal reproduction of the failed cell's containment residual, both precisions,
SAME input arrays (upstream bases computed once in float32 = the runner's dtype, then cast).
Uses the runner's union_basis helper VERBATIM (runner SHA + helper recorded in the output).
Diagnosis status: UNRESOLVED / likely numerical pending this check. -- PI[claude]"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from suppressed_activation_subspace import (
    suppressed_activation_scores, subspace_from_scores)

BANK = ROOT / "out/2026-09-12_devbank"
OUT = ROOT / "out/2026-09-12_cb-fulljoint-failed1140/exact_reproduction.json"
RUNNER = ROOT / "scripts/oat_sweep.py"
CELL = "name-N2-dog"
LAYERS = (25, 26, 27, 28, 29, 30)


def runner_union_basis_cols(m):
    """VERBATIM body of the nested union_basis in scripts/oat_sweep.py (run_with_bundle),
    with the (hidden, r*W) matrix as direct input (the nested one reshapes first).
    Supports dtype via m.dtype."""
    u, s_vals, _ = torch.linalg.svd(m, full_matrices=False)
    # support filter: drop numerical-null columns (arbitrary directions),
    # record support so a changed rank is visible, never silent. -- PI[claude]
    tol = max(m.shape) * torch.finfo(s_vals.dtype).eps * s_vals[0]
    support = int((s_vals > tol).sum())
    u = u[:, :support]
    # runner line compares against torch.eye without dtype (f32-only path); this copy adds
    # dtype=u.dtype so the f64 arm compares like-for-like
    torch.testing.assert_close(u.T @ u, torch.eye(u.shape[1], device=u.device, dtype=u.dtype),
                               rtol=1e-4, atol=1e-4, msg="union basis not orthonormal")
    return u, s_vals, support


def main() -> None:
    src = RUNNER.read_text()
    runner_sha = hashlib.sha256(RUNNER.read_bytes()).hexdigest()
    helper_start = src.index("                m = win.permute(1, 0, 2)")
    helper_end = src.index("return u, s_vals, support", helper_start) + len("return u, s_vals, support")
    helper_sha = hashlib.sha256(src[helper_start:helper_end].encode()).hexdigest()

    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    res_s = torch.load(BANK / f"{CELL}-source_residuals.pt", weights_only=False).float()
    res_d = torch.load(BANK / f"{CELL}-donor_residuals.pt", weights_only=False).float()
    seq_s, seq_d = res_s.shape[1], res_d.shape[1]

    # upstream per-token window bases ONCE in float32 (the runner's dtype path)
    def own_window_bases(res, a):
        rows1 = res.permute(1, 0, 2)
        sc = suppressed_activation_scores(rows1, unembed, gain, early_layer=23, peak_layer=25,
                                          output_layer=32, normalize_unembedding_rows=True)
        b, _ = subspace_from_scores(sc, unembed, gain, rank=8, normalize_unembedding_rows=True)
        return b[a:]  # (4, hidden, 8)

    bw_s = own_window_bases(res_s, seq_s - 4)
    bw_d = own_window_bases(res_d, seq_d - 4)

    out = {"runner_sha256": runner_sha, "helper_body_sha256": helper_sha,
           "helper_path": "scripts/oat_sweep.py run_with_bundle.union_basis (verbatim body above)",
           "status": "UNRESOLVED / likely numerical pending this check",
           "precisions": {}}

    # SAME input arrays in both precisions: the float32 SVD of the SAME float32 window bases,
    # then the resulting Us/Ud columns CAST to float64 for the f64 arm (identical subspaces).
    Us32, sv_s32, sup_s32 = runner_union_basis_cols(bw_s.permute(1, 0, 2).reshape(bw_s.shape[1], -1).float())
    Ud32, sv_d32, sup_d32 = runner_union_basis_cols(bw_d.permute(1, 0, 2).reshape(bw_d.shape[1], -1).float())

    for tag, dtype in (("float32", torch.float32), ("float64", torch.float64)):
        Us = Us32.to(dtype)
        Ud = Ud32.to(dtype)
        joint = torch.cat([Us, Ud], dim=1)
        Pu, sv_u, sup_u = runner_union_basis_cols(joint)
        I = torch.eye(Pu.shape[1], dtype=dtype)
        ortho = float((Pu.T @ Pu - I).norm())
        donor_res = float((Ud - Pu @ (Pu.T @ Ud)).norm()) / float(Ud.norm())  # ||(I-P)Ud||/||Ud||
        vs = []
        for L in LAYERS:
            for o in (1, 2, 3):
                d_l = res_d[L, seq_d - o].to(dtype)
                v = Ud @ (Ud.T @ d_l)
                abs_r = float((v - Pu @ (Pu.T @ v)).norm())
                vs.append({"layer": L, "offset": o, "v_norm": float(v.norm()),
                           "abs_residual": abs_r, "rel_residual": abs_r / float(v.norm())})
        out["precisions"][tag] = {
            "support_source": sup_s32, "support_donor": sup_d32, "joint_support": sup_u,
            "joint_tol": float(max(joint.shape) * torch.finfo(dtype).eps * sv_u[0]),
            "orthonormality_err_F": ortho,
            "donor_basis_residual_rel": donor_res,
            "max_v_rel": max(x["rel_residual"] for x in vs),
            "max_v_abs": max(x["abs_residual"] for x in vs),
            "all_v": vs,
        }
    # f64 arithmetic at FIXED chosen rank (the f32 support), same columns, no support varying
    r_fixed = out["precisions"]["float32"]["joint_support"]
    Pu_fixed = Puc32_fixed = None
    joint64 = torch.cat([Us32.to(torch.float64), Ud32.to(torch.float64)], dim=1)
    u64, s64, _ = torch.linalg.svd(joint64, full_matrices=False)
    Pu_f64_fixed = u64[:, :r_fixed]
    vs_fixed = []
    for L in LAYERS:
        for o in (1, 2, 3):
            d_l = res_d[L, seq_d - o].to(torch.float64)
            v = Ud32.to(torch.float64) @ (Ud32.to(torch.float64).T @ d_l)
            vs_fixed.append(float((v - Pu_f64_fixed @ (Pu_f64_fixed.T @ v)).norm() / v.norm()))
    out["f64_at_fixed_rank"] = {"rank": r_fixed, "max_v_rel": max(vs_fixed),
                                "mean_v_rel": sum(vs_fixed) / len(vs_fixed)}
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
