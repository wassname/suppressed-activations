# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Compact computed diagnostics for the late-blocks claims (CPU, dev bank).

Saves a single JSON with, per prompt and per block: the matched-row decomposition
E_union = E_top8 + E_complement (with per-row residual), write angles (parallel/orthogonal
components and cosines), and the selector token IDs under both the normalized and
unnormalized criteria. These are COMPUTED artifacts, not formulas to re-derive. -- PI[claude]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from suppressed_activation_subspace import (
    suppressed_activation_scores, subspace_from_scores)

BANK = ROOT / "out/2026-09-12_devbank"
OUT = ROOT / "out/2026-09-12_late-blocks-dev/diagnostics.json"


def main() -> None:
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    manifest = json.load(open(BANK / "manifest.json"))["entries"]
    out = {"per_prompt": {}, "selector_sensitivity": {}}
    for name in manifest:
        res = torch.load(BANK / f"{name}_residuals.pt", weights_only=False).float()
        seq = res.shape[1]; a = seq - 4
        rows1 = res.permute(1, 0, 2)
        sc = suppressed_activation_scores(rows1, unembed, gain, early_layer=29,
                                          peak_layer=30, output_layer=32,
                                          normalize_unembedding_rows=True)
        bases, _ = subspace_from_scores(sc, unembed, gain, rank=8,
                                        normalize_unembedding_rows=True)
        M = bases[a:].permute(1, 0, 2).reshape(res.shape[2], -1)
        u, s, _ = torch.linalg.svd(M, full_matrices=False)
        tol = max(M.shape) * torch.finfo(s.dtype).eps * s[0]
        sup = int((s > tol).sum())
        U8, Ucomp = u[:, :8], u[:, :sup][:, 8:]
        # selector ids per window position, both criteria
        h3 = rows1[:, [29, 30, 32]].float()
        hu = torch.einsum("plh,vh->plv", h3 * gain, unembed * gain)
        rise = hu[:, 1] - hu[:, 0]; fall = hu[:, 1] - hu[:, 2]
        rise = rise - rise.mean(-1, keepdim=True); fall = fall - fall.mean(-1, keepdim=True)
        sc2 = torch.minimum(rise.clamp_min(0), fall.clamp_min(0))
        entry = {
            "support": sup,
            "selector_ids_normalized": sc[a:].topk(8, dim=-1).indices.tolist(),
            "selector_ids_unnormalized": sc2[a:].topk(8, dim=-1).indices.tolist(),
            "rows": [],
        }
        for t in range(4):
            pos = a + t
            for l in (29, 30, 31):
                h, h1 = res[l, pos], res[l + 1, pos]
                dh = h1 - h
                Ph, Pdh8, PdhC = U8.T @ h, U8.T @ dh, Ucomp.T @ dh
                E_u = float((u[:, :sup].T @ dh).square().sum())  # matched row: ALL terms on Δh
                E_8 = float(Pdh8.square().sum())
                ph, pdh = U8.T @ h, U8.T @ dh
                par = float(ph @ pdh)
                cos = float(par / (ph.norm() * pdh.norm() + 1e-9))
                pdh_par = ph * ((ph @ pdh) / (ph @ ph))
                E_c = float(PdhC.square().sum())
                entry["rows"].append({
                    "position": pos, "block": l,
                    "E_union": E_u, "E_top8": E_8, "E_complement": E_c,
                    "decomposition_residual": E_u - (E_8 + E_c),
                    "write_parallel_signed": float(pdh_par.norm()) * (1 if par >= 0 else -1),
                    "write_orthogonal": float((pdh - pdh_par).norm()),
                    "cos_Ph_Pdh": cos,
                })
        out["per_prompt"][name] = entry
    out["selector_sensitivity"] = {
        "note": "both selectors are fall-conditioned (rise-then-fall forms); the comparison "
                "is a NORMALIZATION sensitivity check, not independent replication of the fall",
        "computed_in": "scripts/late_blocks_diagnostics.py run log",
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
