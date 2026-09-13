# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8", "transformers>=5.5"]
# ///
"""v2: the ACTUAL selected production directions (per-position top-8 IDs from the
capture) — their squared-projection fraction in U4 vs the FULL span (the support from
the SVD tolerance, not an arbitrary 48). Both dog and ant U4. Containment of ALL
selected production directions must be ~1 in the full span (else debug the convention).
-- PI[glm-5p3-flash]"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import torch

from suppressed_activation_subspace import increment_scores, subspace_from_scores

D = ROOT / "out" / "2026-09-13_bridge-capture-211809"
AN = ROOT / "out" / "2026-09-13_bridge-basis-analysis"
OUT = ROOT / "out" / "2026-09-13_svd4-fraction-v2"


def samples_for(pair):
    names = ("source", "dog") if pair == "source_dog" else ("source", "ant")
    out = []
    for name in names:
        res = torch.load(D / f"{name}_residuals.pt", weights_only=False).float()
        bridge = ROOT / "out" / "2026-09-13_bridge-matrix-193115"
        tag = "dog-att-h20" if name == "source" else f"{name}-att-h20"
        run = json.load(open(bridge / tag / "result.json"))
        ri = run["rendered_inputs"]
        ids = ri["source" if name == "source" else "donor"]["input_ids"]
        out.append({"residuals": res, "content_end": len(ids), "ids": ids})
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.load(open(D / "manifest.json"))
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(manifest["model"], revision=manifest["revision"])
    unemb = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()
    an = json.load(open(AN / "analysis.json"))
    U4s = torch.load(AN / "basis_U4.pt", weights_only=False)

    def frac(V, v):
        return float((V.T @ v).square().sum() / v.square().sum())

    table = {}
    for pair in ("source_dog", "source_ant"):
        sh4 = U4s[f"U4_{pair}"].float()
        # rebuild the concat with the ACTUAL support
        per_pos, sel_ids = [], []
        samples = samples_for(pair)
        for sample in samples:
            res, seq = sample["residuals"], sample["residuals"].shape[1]
            sc = increment_scores(res.permute(1, 0, 2), unemb, gain,
                                  normalize_unembedding_rows=True)
            for off in range(CFG_READOUT):
                q = sample["content_end"] - 1 - off
                ids8 = sc[q].topk(8).indices.tolist()
                sel_ids.extend(ids8)
                bases_q, _ = subspace_from_scores(sc[q:q + 1], unemb, gain, rank=8,
                                                  normalize_unembedding_rows=True)
                per_pos.append(bases_q[0])
        cols = torch.cat(per_pos, dim=1)
        vecs, vals, _ = torch.linalg.svd(cols, full_matrices=False)
        tol = max(cols.shape) * torch.finfo(cols.dtype).eps * vals[0]
        support = int((vals > tol).sum())
        full = vecs[:, :support]
        # the production convention: directions are VOCAB-MEAN-CENTERED before the QR
        dirs = unemb * gain
        dirs = dirs / dirs.norm(dim=-1, keepdim=True)
        dirs_c = dirs - dirs.mean(0)
        # containment of ALL selected production directions (centered) in the FULL span ~ 1
        worst = 1.0
        for vid in set(sel_ids):
            v = dirs_c[vid]
            worst = min(worst, frac(full, v))
        assert worst > 0.99, f"{pair}: selected direction {1-worst:.3f} outside the full span"
        # the fractions for the ACTUAL selected IDs (centered directions)
        rows = {}
        for vid in sorted(set(sel_ids)):
            v = dirs_c[vid]
            rows[f"{tok.decode([vid])!r}:{vid}"] = {"U4": round(frac(sh4, v), 4),
                                                    "full": round(frac(full, v), 4)}
        table[pair] = {"support": support, "worst_full_containment": round(worst, 6),
                       "rows": rows}
        n_kept = sum(1 for v in rows.values() if v["U4"] > 0.5)
        print(f"{pair}: support {support} | worst full containment {worst:.6f} | "
              f"U4 fraction > 0.5 for {n_kept}/{len(rows)} selected directions")
    (OUT / "svd4_fraction_v2.json").write_text(json.dumps(
        {"formula": "||V.T v||^2 / ||v||^2; v = (unemb[id]*gain)/rown; full span = SVD support",
         "table": table}, indent=1) + "\n")
    print(f"saved: {OUT / 'svd4_fraction_v2.json'}")


CFG_READOUT = 4

if __name__ == "__main__":
    main()
