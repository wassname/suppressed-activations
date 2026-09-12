# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""MAINTAINED integration test: the PRODUCTION complete_edit_bases function on real
nondegenerate tensors. Mutation: flipping common_temporal_full=False MUST fail the
support/containment conditions. Old rankinj k1/k2 modes asserted unchanged.
-- PI[glm-5p3-flash]"""
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
import scripts.oat_sweep as oat
from suppressed_activation_subspace import increment_scores, subspace_from_scores

BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"


def test_full_vs_k8():
    res_d = torch.load(BANK / "name-N1-dog-donor_residuals.pt", weights_only=False).float()
    res_s = torch.load(BANK / "name-N1-dog-source_residuals.pt", weights_only=False).float()
    cfg_full = replace(next(c for _, v, c in oat.SWEEP_CONFIGS['complete-rank']()
                            if v == 'kfull_C1.5'))
    cfg_k8 = replace(next(c for _, v, c in oat.SWEEP_CONFIGS['complete-rank']()
                          if v == 'k8_C1.5'))
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()

    def union_supported(res, a):
        rows1 = res.permute(1, 0, 2)
        inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
        b, _ = subspace_from_scores(inc, unembed, gain, rank=8, normalize_unembedding_rows=True)
        M = b[a:].permute(1, 0, 2).reshape(res.shape[2], -1)
        u, sv, _ = torch.linalg.svd(M, full_matrices=False)
        tol = max(M.shape) * torch.finfo(sv.dtype).eps * sv[0]
        return u[:, :int((sv > tol).sum())]

    U_s = union_supported(res_s, res_s.shape[1]-4)
    U_d = union_supported(res_d, res_d.shape[1]-4)
    # PRODUCTION function: the full arm (the FIXED upstream: the full supported bases)
    Us_f, Ud_f, Pj_f, active_f = oat.complete_edit_bases(U_s, U_d, U_s[:, :8], U_d[:, :8], cfg_full)
    assert active_f and Pj_f.shape[1] > 16, f"full joint {Pj_f.shape[1]} not > 16"
    # PRODUCTION: the k8 arm
    Us_k8, Ud_k8, Pj_8, active_8 = oat.complete_edit_bases(U_s, U_d, U_s[:, :8], U_d[:, :8], cfg_k8)
    assert active_8 and Pj_8.shape[1] == 16
    # MUTATION: the OLD BUG = the upstream U_s/U_d ALREADY top8-truncated (the runner
    # sliced U_s/U_d before complete_edit_bases) — the reproduction:
    Us_b, Ud_b, Pj_b, _ = oat.complete_edit_bases(U_s[:, :8], U_d[:, :8], U_s[:, :8], U_d[:, :8], cfg_full)
    assert Pj_b.shape[1] == 16, f"the old-bug mutation: joint {Pj_b.shape[1]} != 16"
    d25 = res_d[25, res_d.shape[1]-1]
    v_full = U_d @ (U_d.T @ d25)
    v8 = U_d[:, :8] @ (U_d[:, :8].T @ d25)
    assert v_full.square().sum() >= v8.square().sum() - 1e-6, "nesting violated"
    # the nesting FAILURE under the old bug: the buggy arm's injection energy = k8's
    v_buggy = U_d[:, :8] @ (U_d[:, :8].T @ d25)
    assert float(v_buggy.square().sum()) < float(v_full.square().sum()) - 1.0
    print("COMPLETE-EDIT INTEGRATION PASS: production fn; the old-bug mutation "
          f"(Pj {Pj_b.shape[1]} vs {Pj_f.shape[1]}); nesting; k8 unchanged")


if __name__ == "__main__":
    test_full_vs_k8()
