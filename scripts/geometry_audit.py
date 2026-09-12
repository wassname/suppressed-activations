# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Geometry audit on the exact-input bank (task 1182 selectors).

Outputs (all SAVED with per-row labels):
1. snapshot-top8 vs increment-top8 union PRINCIPAL-ANGLE COSINES (singular values of
   U_s^T U_d — NOT angles; max cos = ONE shared direction, not near-identical spans),
   labeled per cell/side.
2. donor-projection energy retained in top8 vs full union, per LAYER (tagged: these are
   layers 20/25, NOT the 1182 intervention sites 8/20), per cell/position.
Generates out/2026-09-12_cb-selsite/geometry_audit.json. -- PI[glm-5p3-flash]"""

from __future__ import annotations

import json
import statistics as st
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import (
    suppressed_activation_scores, increment_scores, subspace_from_scores)

BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-selsite/geometry_audit.json"


def main() -> None:
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    manifest = json.load(open(BANK / "manifest.json"))
    out = {"note_principal": "singular values of U_snap^T U_inc = PRINCIPAL-ANGLE COSINES "
                             "(not angles); max cos ~1 = ONE shared direction",
           "note_retention_layers": "retention rows are LAYERS 20/25 (not the 1182 sites 8/20)",
           "per_cell": {}}
    flat = {"source": [], "donor": []}
    ret_rows = []
    for cid in sorted({n.rsplit('-', 1)[0] for n in manifest['entries']
                       if n.endswith(('-source', '-donor'))}):
        entry = {"sides": {}}
        for side in ('source', 'donor'):
            res = torch.load(BANK / f"{cid}-{side}_residuals.pt", weights_only=False).float()
            seq = res.shape[1]; a = seq - 4
            rows1 = res.permute(1, 0, 2)
            snap = suppressed_activation_scores(rows1, unembed, gain, early_layer=23,
                                                peak_layer=25, output_layer=32,
                                                normalize_unembedding_rows=True)
            inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
            def cols(score):
                b, _ = subspace_from_scores(score, unembed, gain, rank=8,
                                            normalize_unembedding_rows=True)
                M = b[a:].permute(1, 0, 2).reshape(res.shape[2], -1)
                u, sv, _ = torch.linalg.svd(M, full_matrices=False)
                tol = max(M.shape) * torch.finfo(sv.dtype).eps * sv[0]
                full = u[:, :int((sv > tol).sum())]
                return full[:, :8], full
            s8, sfull = cols(snap)
            d8, dfull = cols(inc)
            cos = [round(float(x), 4) for x in torch.linalg.svdvals(s8.T @ d8)]
            entry["sides"][side] = {"principal_angle_cosines_snapshot_vs_increment_top8": cos}
            flat[side].extend(cos)
            # donor-projection energy: top8 vs full (donor side only; layers 20/25 tagged)
            if side == 'donor':
                for L in (20, 25):
                    for o in (1, 2, 3):
                        d_l = res[L, seq - o]
                        v8 = d8 @ (d8.T @ d_l)
                        vf = dfull @ (dfull.T @ d_l)
                        ret_rows.append({"cell": cid, "layer": L, "offset": o,  # LAYER, not site
                                         "energy_top8": round(float(v8.square().sum()), 3),
                                         "energy_full": round(float(vf.square().sum()), 3),
                                         "retained_frac": round(float(v8.square().sum() /
                                                                      (vf.square().sum() + 1e-9)), 3)})
        out["per_cell"][cid] = entry
    out["summary"] = {
        "principal_cos_source": {"mean": round(st.mean(flat['source']), 4),
                                 "max": round(max(flat['source']), 4)},
        "principal_cos_donor": {"mean": round(st.mean(flat['donor']), 4),
                                "max": round(max(flat['donor']), 4)},
        "retained_energy_top8_vs_full": {
            "mean": round(st.mean([r['retained_frac'] for r in ret_rows]), 4),
            "per_row": ret_rows},
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
