# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Fixed-removal rank design (CPU): P_joint8 = span(Us8, Ud8) removal in EVERY condition;
vary ONLY the injection v_k = Ud_k Ud_k^T d25 for k in {1,2,4,8} (contained already).
Measures per cell/offset: ||Pd_k d25||^2 / ||Pd8 d25||^2 (donor-signal retention) and the
resulting planned edit ||C(v_k - P_joint8 h8)|| / ||h8||. -- PI[glm-5p3-flash]"""
import json, torch, sys, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import increment_scores, subspace_from_scores
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-selsite/rank_design_cpu.json"
C = 1.5


def runner_union_basis_cols(m):
    """VERBATIM runner joint construction (scripts/oat_sweep.py union_basis body)."""
    u, s_vals, _ = torch.linalg.svd(m, full_matrices=False)
    tol = max(m.shape) * torch.finfo(s_vals.dtype).eps * s_vals[0]
    support = int((s_vals > tol).sum())
    u = u[:, :support]
    return u, s_vals, support

def main():
    unembed = torch.load(BANK/'unembedding.pt', weights_only=False).float()
    gain = torch.load(BANK/'norm_gain.pt', weights_only=False).float()
    manifest = json.load(open(BANK/'manifest.json'))
    rows = []
    for cid in sorted({n.rsplit('-',1)[0] for n in manifest['entries'] if n.endswith('-donor')}):
        res_d = torch.load(BANK/f'{cid}-donor_residuals.pt', weights_only=False).float()
        res_s = torch.load(BANK/f'{cid}-source_residuals.pt', weights_only=False).float()
        seq_d, seq_s = res_d.shape[1], res_s.shape[1]
        ad, asr = seq_d-4, seq_s-4
        def top8(res, a):
            rows1 = res.permute(1,0,2)
            inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
            b, _ = subspace_from_scores(inc, unembed, gain, rank=8, normalize_unembedding_rows=True)
            M = b[a:].permute(1,0,2).reshape(res.shape[2], -1)
            u, sv, _ = torch.linalg.svd(M, full_matrices=False)
            return u[:, :8]
        Ud8 = top8(res_d, ad)
        Us8 = top8(res_s, asr)
        # JOINT support exactly as the runner: SVD of the concatenation, support-filtered
        # (the raw cat columns are NOT jointly orthonormal - cat+apply sums two projectors)
        Pj, svj, supj = runner_union_basis_cols(torch.cat([Us8, Ud8], dim=1))
        ortho_err = float((Pj.T @ Pj - torch.eye(Pj.shape[1], dtype=Pj.dtype)).norm())
        assert ortho_err < 1e-5, f"joint not orthonormal: {ortho_err}"
        x = torch.randn(Pj.shape[0], dtype=Pj.dtype)
        idem = float((Pj @ (Pj.T @ (Pj @ (Pj.T @ x))) - Pj @ (Pj.T @ x)).norm())
        assert idem < 1e-5 * x.norm(), f"joint projector not idempotent: {idem}"
        for o in (1,2,3):
            d25 = res_d[25, seq_d-o]
            h8 = res_s[8, seq_s-o]
            v8 = Ud8 @ (Ud8.T @ d25)
            removal = Pj @ (Pj.T @ h8)
            rec = {'cell': cid, 'offset': o, 'h8_norm': round(float(h8.norm()), 3),
                   'removal_norm_frac': round(float(removal.norm()/h8.norm()), 4)}
            for k in (1,2,4,8):
                Uk = Ud8[:, :k]
                v_k = Uk @ (Uk.T @ d25)
                edit = C * (v_k - removal)   # the same joint removal for every k
                rec[f'k{k}'] = {'inj_energy_frac_vs_k8': round(float(v_k.square().sum()/v8.square().sum()), 4),
                                'edit_norm_frac_of_h8': round(float(edit.norm()/h8.norm()), 4)}
            rows.append(rec)
    summary = {}
    for k in (1,2,4,8):
        ks = [r[f'k{k}']['inj_energy_frac_vs_k8'] for r in rows]
        es = [r[f'k{k}']['edit_norm_frac_of_h8'] for r in rows]
        summary[f'k{k}'] = {'inj_energy_frac_vs_k8': round(st.mean(ks), 4),
                            'edit_norm_frac_of_h8': round(st.mean(es), 4)}
    json.dump({'rows': rows, 'summary': summary}, open(OUT, 'w'), indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == '__main__':
    main()
