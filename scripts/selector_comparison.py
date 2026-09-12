# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Selector comparison on EXACT inputs: the 3-snapshot selector vs the positive-increment
sum candidate (whole-last-3), per the recovery report's unit tests. CPU only. -- PI[glm-5p3-flash]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from suppressed_activation_subspace import suppressed_activation_scores

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "out/2026-09-12_exact-input-bank-att3"
OUT = ROOT / "out/2026-09-12_selector-comparison-v2"
B_BUILD = range(13, 24)          # the hypothesis window (b13..b23)
LAST3_WRITES = (29, 30, 31)      # exactly the last-3 block writes


def readout(res: torch.Tensor, unembed: torch.Tensor, gain: torch.Tensor) -> torch.Tensor:
    """ϕ[b, pos, vocab]: RMS+gain readout, row-normalized. Gain applied ONCE (h-side) with
    the row normalization dividing by ||unembed*gain|| - EXACTLY the
    suppressed_activation_scores convention (the previous version applied gain twice)."""
    h = res.float()
    hn = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain
    row_norm = (unembed * gain).norm(dim=-1)
    return hn @ unembed.T / row_norm  # (33, seq, V)


def regression_check(phi: torch.Tensor, res: torch.Tensor, unembed: torch.Tensor,
                     gain: torch.Tensor) -> None:
    """Executed regression: my snapshot scores == canonical suppressed_activation_scores
    (normalize_unembedding_rows=True) on the same saved tensors."""
    canonical = suppressed_activation_scores(
        res.permute(1, 0, 2), unembed, gain, early_layer=23, peak_layer=25,
        output_layer=32, normalize_unembedding_rows=True)  # (seq, V)
    mine = selectors(phi)[0]  # snapshot scores (seq, V)
    torch.testing.assert_close(mine, canonical, rtol=1e-4, atol=1e-4,
                               msg="snapshot scores diverge from canonical scores")


def selectors(phi: torch.Tensor):
    """phi: (33, seq, V) -> per-position score vectors for both selectors."""
    c = lambda x: x - x.mean(-1, keepdim=True)
    relu = torch.relu
    # 3-snapshot (existing): rise = phi25 - phi23; fall = phi25 - phi32 (centered then rectified)
    rise3 = c(phi[25] - phi[23])
    fall3 = c(phi[25] - phi[32])
    snap = torch.minimum(rise3.clamp_min(0), fall3.clamp_min(0))
    # positive-increment candidate: dphi(b) = phi(b+1) - phi(b), centered BEFORE rectification
    dphi = c(phi[1:] - phi[:-1])                       # dphi[b] for b in 0..31
    build = relu(dphi[13:24]).sum(0)                   # sum over b13..b23
    cut3 = relu(-dphi[list(LAST3_WRITES)]).sum(0)      # exactly writes b29,b30,b31
    cut_post = relu(-dphi[30:32]).sum(0)               # post-peak variant (b30,b31 only)
    cand = torch.minimum(build, cut3)
    cand_post = torch.minimum(build, cut_post)
    return snap, cand, cand_post


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    manifest = json.load(open(BANK / "manifest.json"))
    result = {"per_cell": {}, "notes": {
        "bank": str(BANK), "wrapper": manifest["wrapper"], "revision": manifest["revision"],
        "build_window": "b13..b23 (hypothesis window)",
        "windows": {"snap3": "(23,25,32) endpoints",
                    "candidate": "build = sum relu(dphi b13..b23); cut = sum relu(-dphi) over b29,b30,b31",
                    "post-peak variant": "cut over b30,b31 only"}}}
    for name, entry in manifest["entries"].items():
        res = torch.load(BANK / f"{name}_residuals.pt", weights_only=False).float()
        seq = res.shape[1]
        phi = readout(res, unembed, gain)
        regression_check(phi, res, unembed, gain)
        snap, cand, cand_post = selectors(phi)
        a = seq - 4  # window = last-4 (as before)
        r = {}
        for sname, scores in (("snapshot3", snap), ("increment_cand", cand), ("increment_postpeak", cand_post)):
            top = scores[a:].topk(8, dim=-1).indices          # (4, 8) per window position
            r[f"{sname}_ids"] = top.tolist()
            r[f"{sname}_scores"] = [round(float(x), 4) for x in scores[a:].topk(8, dim=-1).values.flatten()]
        # agreement between selectors on the union of window top-8 sets
        set_s = {t for rowt in r["snapshot3_ids"] for t in rowt}
        set_c = {t for rowt in r["increment_cand_ids"] for t in rowt}
        r["jaccard_snapshot_vs_candidate"] = len(set_s & set_c) / len(set_s | set_c)
        result["per_cell"][name] = r
    # aggregate jaccard
    js = [v["jaccard_snapshot_vs_candidate"] for v in result["per_cell"].values()]
    result["jaccard_summary"] = {"mean": sum(js)/len(js), "min": min(js), "max": max(js)}
    json.dump(result, open(OUT / "selector_comparison.json", "w"), indent=1)
    print(f"wrote {OUT/'selector_comparison.json'}; Jaccard mean {result['jaccard_summary']['mean']:.3f} "
          f"min {result['jaccard_summary']['min']:.3f} max {result['jaccard_summary']['max']:.3f}")


if __name__ == "__main__":
    main()
