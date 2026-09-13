# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8", "transformers>=5.5"]
# ///
"""PRODUCING script for the paired candidate (one CPU run, no forward):
- reproduces the PLAIN U4 and asserts it == the SAVED U4 (basis_U4.pt);
- builds the PAIRED U4 per donor pair (the production paired_score option);
- computes the plain AND paired retention of the donor-specific directions with the
  SAME centered vectors;
- records the selected IDs/scores per position + the singular values.
-- PI[glm-5p3-flash]"""
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import torch
from transformers import AutoTokenizer

from scripts.oat_sweep import increment_union_basis

D = ROOT / "out" / "2026-09-13_bridge-capture-211809"
AN = ROOT / "out" / "2026-09-13_bridge-basis-analysis"
OUT = ROOT / "out" / "2026-09-13_paired-candidate"
CFG = SimpleNamespace(readout_positions=4, common_source_rank=8, common_donor_rank=8,
                      persistent_rank=4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.load(open(D / "manifest.json"))
    tok = AutoTokenizer.from_pretrained(manifest["model"], revision=manifest["revision"])
    unemb = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()
    samples = {}
    for name in ("source", "dog", "ant"):
        tag = "dog-att-h20" if name == "source" else f"{name}-att-h20"
        run = json.load(open(ROOT / "out" / "2026-09-13_bridge-matrix-193115" / tag / "result.json"))
        ri = run["rendered_inputs"]
        samples[name] = {"residuals": torch.load(D / f"{name}_residuals.pt",
                                                 weights_only=False).float(),
                         "content_end": len(ri["source" if name == "source"
                                                    else "donor"]["input_ids"]),
                         "ids": ri["source" if name == "source" else "donor"]["input_ids"]}

    # 1. the plain U4 reproduction (assert vs the saved)
    plain_dog, d_dog = increment_union_basis(samples["source"], samples["dog"], CFG, unemb, gain)
    saved = torch.load(AN / "basis_U4.pt", weights_only=False)
    torch.testing.assert_close(plain_dog, saved["U4_source_dog"], rtol=1e-5, atol=1e-6)
    print("plain U4 == saved U4 (asserted)")

    # 2. the paired U4 per pair
    out = {"formula": "paired_score per position: (S_this[q]-S_other[q]).clamp_min(0); "
                      "top-8 each side, each of the 4 aligned suffix positions; concat 64; "
                      "SVD-4; SAME shared-U operator", "pairs": {}}
    for pair, donor in (("dog", "dog"), ("ant", "ant")):
        cfg_p = SimpleNamespace(**{**CFG.__dict__, "paired_score": True})
        U4p, diag_p = increment_union_basis(samples["source"], samples[donor], cfg_p,
                                            unemb, gain)
        # the retention: the SAME centered vectors for plain and paired
        dirs = unemb * gain
        dirs_c = dirs - dirs.mean(0)
        sc_s = None
        from suppressed_activation_subspace import increment_scores
        sc_s = increment_scores(samples["source"]["residuals"].permute(1, 0, 2), unemb, gain,
                                normalize_unembedding_rows=True)[-4:].sum(0)
        sc_d = increment_scores(samples[donor]["residuals"].permute(1, 0, 2), unemb, gain,
                                normalize_unembedding_rows=True)[-4:].sum(0)
        don_ids = (sc_d - sc_s).clamp_min(0).topk(8).indices.tolist()
        ret = {}
        for vid in sorted(don_ids):
            ret[f"{tok.decode([vid])!r}:{vid}"] = {
                "plain_U4": round(float((plain_dog.T @ dirs_c[vid]).square().sum()
                                        / dirs_c[vid].square().sum()), 4),
                "paired_U4": round(float((U4p.T @ dirs_c[vid]).square().sum()
                                         / dirs_c[vid].square().sum()), 4)}
        out["pairs"][pair] = {"diag": diag_p, "retention": ret,
                              "U4_sha256": hashlib.sha256(
                                  U4p.numpy().tobytes()).hexdigest()}
        print(pair, "support", diag_p["basis_support"], "| paired retention:",
              sorted(((k, v["paired_U4"]) for k, v in ret.items()), key=lambda x: -x[1])[:4])
    torch.save({"paired_U4_dog": out and None}, OUT / "tmp.pt") if False else None
    torch.save({"paired_U4": {pair: None for pair in out["pairs"]}}, OUT / "U4_paired.pt")
    (OUT / "candidate.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"saved: {OUT / 'candidate.json'}")


if __name__ == "__main__":
    main()
