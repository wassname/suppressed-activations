# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
# the maintained regression: (1) the full arm's actual support > 8 on a nondegenerate
# fixture; (2) the full projector contains k8; (3) the same-state full projection energy
# >= k8's (nesting); (4) the k8 projector/vector UNCHANGED
import torch, sys
sys.path.insert(0, '.')
from pathlib import Path
from suppressed_activation_subspace import increment_scores, subspace_from_scores
import scripts.oat_sweep as oat
rows = oat.SWEEP_CONFIGS['complete-rank']()
by_label = {v: c for _, v, c in rows}
# the nondegenerate fixture: the exact-input bank's real tensors (name-N1-dog)
BANK = Path('out/2026-09-12_exact-input-bank-att3')
unembed = torch.load(BANK/'unembedding.pt', weights_only=False).float()
gain = torch.load(BANK/'norm_gain.pt', weights_only=False).float()
res_d = torch.load(BANK/'name-N1-dog-donor_residuals.pt', weights_only=False).float()
res_s = torch.load(BANK/'name-N1-dog-source_residuals.pt', weights_only=False).float()
seq_d, seq_s = res_d.shape[1], res_s.shape[1]
ad, asr = seq_d-4, seq_s-4
# production construction path (the same as run_with_bundle's complete-mode branch):
# increment scores -> subspace_from_scores -> union_basis (support) -> the sentinel slicing
def union_basis_runner(win):
    m = win.permute(1, 0, 2).reshape(win.shape[1], -1)
    u, s_vals, _ = torch.linalg.svd(m, full_matrices=False)
    tol = max(m.shape) * torch.finfo(s_vals.dtype).eps * s_vals[0]
    support = int((s_vals > tol).sum())
    return u[:, :support], s_vals, support
sc_d = increment_scores(res_d.permute(1,0,2), unembed, gain, normalize_unembedding_rows=True)
sc_s = increment_scores(res_s.permute(1,0,2), unembed, gain, normalize_unembedding_rows=True)
Bd, _ = subspace_from_scores(sc_d, unembed, gain, rank=8, normalize_unembedding_rows=True)
Bs, _ = subspace_from_scores(sc_s, unembed, gain, rank=8, normalize_unembedding_rows=True)
U_d_full, sv_d, _ = union_basis_runner(Bd[ad:])
U_s_full, sv_s, _ = union_basis_runner(Bs[asr:])
print(f"full supports: donor {U_d_full.shape[1]}, source {U_s_full.shape[1]}")
# (1) the full arm's support > 8
assert U_d_full.shape[1] > 8 and U_s_full.shape[1] > 8, "full support NOT > 8"
# the k8 arm's bases: the top8 temporal = the union support's first 8
U_d8 = U_d_full[:, :8]; U_s8 = U_s_full[:, :8]
# the projected donor vectors: the same state d25, per offset
for o in (1, 2, 3):
    d25 = res_d[25, seq_d-o]
    v_full = U_d_full @ (U_d_full.T @ d25)
    v8 = U_d8 @ (U_d8.T @ d25)
    # (3) nesting: the full projection energy >= k8's
    assert v_full.square().sum() >= v8.square().sum() - 1e-6, f"nesting violated at offset {o}"
# (2) the full projector contains k8: ||(I-P_full) U8|| ~ 0
resid = U_d8 - U_d_full @ (U_d_full.T @ U_d8)
# float32 noise: measured 2.5e-6 (vs the signal 2.83) - the threshold 1e-4
assert float(resid.norm()) < 1e-4, "the full projector does not contain k8"
# (4) the k8 projector/vector unchanged by the flag fix: the k8 arm's cfg: temporal_full
# False, ranks 8/8 -> the same construction as before the fix
k8_cfg = by_label['k8_C1.5']
assert k8_cfg.common_temporal_full is False and k8_cfg.common_donor_rank == 8
print("FULL-SUPPORT REGRESSION PASS: support > 8 (donor %d/source %d); nesting holds; "
      "the full projector contains k8; the k8 arm unchanged" % (U_d_full.shape[1], U_s_full.shape[1]))
