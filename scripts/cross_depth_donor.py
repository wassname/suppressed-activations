# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Cross-depth donor projection table: the donor residual projected on the trajectory-
selected (bank 23/25/32) top8 span at depths h8/h20/h25/h30 - normalized + absolute
magnitudes, labeled rows. Informs the cross-depth donor candidate (inject the LATE-BUILT
donor component at the EARLY h8 site; explicit cross-depth coordinate/scale caveat).
-- PI[glm-5p3-flash]"""
import json, torch, sys, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import suppressed_activation_scores, subspace_from_scores
BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-selsite/cross_depth_donor.json"

def main():
    unembed = torch.load(BANK/'unembedding.pt', weights_only=False).float()
    gain = torch.load(BANK/'norm_gain.pt', weights_only=False).float()
    manifest = json.load(open(BANK/'manifest.json'))
    rows = []
    for cid in sorted({n.rsplit('-',1)[0] for n in manifest['entries'] if n.endswith('-donor')}):
        res_d = torch.load(BANK/f'{cid}-donor_residuals.pt', weights_only=False).float()
        seq = res_d.shape[1]; a = seq-4
        rows1 = res_d.permute(1,0,2)
        snap = suppressed_activation_scores(rows1, unembed, gain, early_layer=23, peak_layer=25,
                                            output_layer=32, normalize_unembedding_rows=True)
        b, _ = subspace_from_scores(snap, unembed, gain, rank=8, normalize_unembedding_rows=True)
        M = b[a:].permute(1,0,2).reshape(res_d.shape[2], -1)
        u, sv, _ = torch.linalg.svd(M, full_matrices=False)
        Ud8 = u[:, :8]
        for L in (8, 20, 25, 30):
            for o in (1, 2, 3):
                d_l = res_d[L, seq-o]
                v = Ud8 @ (Ud8.T @ d_l)
                rows.append({'cell': cid, 'site_layer': L, 'offset': o,
                             'proj_norm': round(float(v.norm()), 3),
                             'h_norm': round(float(d_l.norm()), 3),
                             'proj_frac': round(float(v.norm()/d_l.norm()), 4)})
    agg = {}
    for r in rows: agg.setdefault(r['site_layer'], []).append(r['proj_norm'])
    summary = {str(L): {'mean_proj_norm': round(st.mean(agg[L]), 3),
                        'mean_proj_frac': round(st.mean([r['proj_frac'] for r in rows if r['site_layer']==L]), 4)}
               for L in sorted(agg)}
    json.dump({'rows': rows, 'summary': summary}, open(OUT, 'w'), indent=1)
    print('summary:', json.dumps(summary))

if __name__ == '__main__':
    main()
