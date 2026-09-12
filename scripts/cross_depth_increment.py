# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Cross-depth donor table with the INCREMENT trajectory selector (1182's): the donor
residual at each depth projected on the increment-selected top8 span; cross-depth COSINES
(cos(v8, v25) etc. — the missing measurement). Labeled artifact. -- PI[glm-5p3-flash]"""
import json, torch, sys, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import increment_scores, subspace_from_scores
BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-selsite/cross_depth_increment.json"

def main():
    unembed = torch.load(BANK/'unembedding.pt', weights_only=False).float()
    gain = torch.load(BANK/'norm_gain.pt', weights_only=False).float()
    manifest = json.load(open(BANK/'manifest.json'))
    rows, cos_rows = [], []
    for cid in sorted({n.rsplit('-',1)[0] for n in manifest['entries'] if n.endswith('-donor')}):
        res_d = torch.load(BANK/f'{cid}-donor_residuals.pt', weights_only=False).float()
        seq = res_d.shape[1]; a = seq-4
        rows1 = res_d.permute(1,0,2)
        inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
        b, _ = subspace_from_scores(inc, unembed, gain, rank=8, normalize_unembedding_rows=True)
        M = b[a:].permute(1,0,2).reshape(res_d.shape[2], -1)
        u, sv, _ = torch.linalg.svd(M, full_matrices=False)
        Ud8 = u[:, :8]
        vs = {}
        for L in (8, 20, 25, 30):
            for o in (1, 2, 3):
                d_l = res_d[L, seq-o]
                v = Ud8 @ (Ud8.T @ d_l)
                vs[(L, o)] = v
                rows.append({'cell': cid, 'site_layer': L, 'offset': o,
                             'proj_norm': round(float(v.norm()), 3),
                             'proj_frac': round(float(v.norm()/d_l.norm()), 4)})
        for o in (1, 2, 3):
            for La, Lb in ((8, 25), (8, 30), (20, 25), (25, 30)):
                c = float(vs[(La,o)] @ vs[(Lb,o)] / (vs[(La,o)].norm()*vs[(Lb,o)].norm() + 1e-9))
                cos_rows.append({'cell': cid, 'offset': o, 'pair': f'h{La}-h{Lb}', 'cos': round(c, 4)})
    summary = {str(L): {'mean_proj_norm': round(st.mean([r['proj_norm'] for r in rows if r['site_layer']==L]), 3),
                        'mean_frac': round(st.mean([r['proj_frac'] for r in rows if r['site_layer']==L]), 4)}
               for L in (8, 20, 25, 30)}
    cos_summary = {}
    for r in cos_rows: cos_summary.setdefault(r['pair'], []).append(r['cos'])
    cos_means = {k: round(st.mean(v), 4) for k, v in cos_summary.items()}
    json.dump({'rows': rows, 'summary': summary, 'cross_depth_cosines': cos_rows,
               'cosine_means': cos_means}, open(OUT, 'w'), indent=1)
    print('summary:', json.dumps(summary))
    print('cross-depth cosines:', json.dumps(cos_means))

if __name__ == '__main__':
    main()
