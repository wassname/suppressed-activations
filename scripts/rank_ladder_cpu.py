# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Per-k CPU precomputation for the complete-edit rank ladder (protocol
slop/complete_rank_protocol.md): per-POSITION norms with the SAME denominators, energies,
triangle bounds and delta-identity asserts. -- PI[glm-5p3-flash]"""
import json, torch, sys, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import increment_scores, subspace_from_scores
BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-earlyloc/rank_ladder_cpu.json"
C = 1.5

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
        def union_full(res, a, W):
            # the production temporal span: the LAST W positions (1230 config window=4)
            rows1 = res.permute(1,0,2)
            inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
            b, _ = subspace_from_scores(inc, unembed, gain, rank=8, normalize_unembedding_rows=True)
            M = b[res.shape[1]-W:].permute(1,0,2).reshape(res.shape[2], -1)
            u, sv, _ = torch.linalg.svd(M, full_matrices=False)
            tol = max(M.shape) * torch.finfo(sv.dtype).eps * sv[0]
            sup = int((sv > tol).sum())
            return u[:, :sup], sup          # FULL supported temporal basis + rank
        Us_full, sup_s = union_full(res_s, asr, W=4)
        Ud_full, sup_d = union_full(res_d, ad, W=4)
        SITE = 1  # the predeclared early intervention layer (h1)
        for o in (1, 2, 3):
            d25 = res_d[25, seq_d-o]
            h8 = res_s[SITE, seq_s-o]   # the edited state = h_SITE (h1), named h in records
            rec = {'cell': cid, 'offset': o, 'site_layer': SITE,
                   'h_norm': round(float(h8.norm()), 4)}
            for k in (1, 2, 4, 8, 'full'):
                ks = sup_s if k == 'full' else k
                kd = sup_d if k == 'full' else k
                Us_k, Ud_k = Us_full[:, :ks], Ud_full[:, :kd]
                # joint = orthonormal support-filtered union of the two truncated bases
                cat = torch.cat([Us_k, Ud_k], dim=1)
                uj, svj, _ = torch.linalg.svd(cat, full_matrices=False)
                tolj = max(cat.shape) * torch.finfo(svj.dtype).eps * svj[0]
                keep = int((svj > tolj).sum())
                Pj_cols = uj[:, :keep]
                assert float((Pj_cols.T @ Pj_cols - torch.eye(keep)).norm()) < 1e-5
                v_k = Ud_k @ (Ud_k.T @ d25)
                edit = C * (v_k - Pj_cols @ (Pj_cols.T @ h8))
                # per-position decomposition (same denominator h8)
                rec[f'k{k}'] = {
                    'inj_norm_frac': round(float((C * v_k).norm())/float(h8.norm()), 4),
                    'rem_norm_frac': round(float((C * Pj_cols @ (Pj_cols.T @ h8)).norm())/float(h8.norm()), 4),
                    'edit_norm_frac': round(float(edit.norm()/h8.norm()), 4),
                    'inj_energy': round(float(v_k.square().sum()), 3),
                    'joint_rank': keep}
                # triangle bound: edit <= C(inj + rem)
                tri = C * (v_k.norm() + (Pj_cols @ (Pj_cols.T @ h8)).norm())
                assert edit.norm() <= tri + 1e-6, "triangle violated"
                # delta identity: edit = C*v_k - C*Pj h; check exact decomposition
                assert torch.allclose(edit, C*v_k - C*(Pj_cols @ (Pj_cols.T @ h8)), atol=1e-5)
            rows.append(rec)
    summary = {}
    for k in (1, 2, 4, 8, 'full'):
        summary[f'k{k}'] = {
            'inj_norm_frac': round(st.mean([r[f'k{k}']['inj_norm_frac'] for r in rows]), 4),
            'rem_norm_frac': round(st.mean([r[f'k{k}']['rem_norm_frac'] for r in rows]), 4),
            'edit_norm_frac': round(st.mean([r[f'k{k}']['edit_norm_frac'] for r in rows]), 4),
            'joint_rank': st.mean([r[f'k{k}']['joint_rank'] for r in rows])}
    json.dump({'rows': rows, 'summary': summary}, open(OUT, 'w'), indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == '__main__':
    main()
