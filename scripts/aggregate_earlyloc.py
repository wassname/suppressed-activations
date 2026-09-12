# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Aggregation for the earlyloc batch (summary.json): swap/capped/loops/edit_frac.
The definitions: capped = >=128 tokens with no <|im_end|>; loops = r2 > 0.5;
edit_frac = the mean over cells of the JOINT 3-position Frobenius ratio
(||edit||_F/||h||_F - NOT a per-position quantity; per-position ratios in the
audit-calc). -- PI[glm-5p3-flash]"""
import json, statistics as st
from pathlib import Path
B = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-earlyloc"
CONDS = ["v25imported_h1_C1.5","v25imported_h2_C1.5","v25imported_h3_C1.5","v25imported_h8_C1.5",
         "siterescaled_h1_C1.5","siterescaled_h2_C1.5","siterescaled_h3_C1.5","v8replay_h8_C1.5",
         "C0_h1","C0_h2","C0_h3","C0_h8"]

def main():
    out = {}
    for cond in CONDS:
        rs = [json.loads(p.read_text())["rows"][0]
              for p in sorted(B.glob(f"{cond}-*/result.json"))]
        ids = [p.parent.name[len(cond)+1:] for p in sorted(B.glob(f"{cond}-*/result.json"))]
        qtype = lambda i: i.split("-")[0]
        capped = sum(1 for r in rs if r["generation_tokens"] >= 128
                     and not r["generation"]["text"].endswith("<|im_end|>"))
        loops = sum(1 for r in rs if r["repeated_bigram_fraction"] > 0.5)
        ef = st.mean([list(r["intervention_record"].values())[0]["perturbation_norm"] /
                      list(r["intervention_record"].values())[0]["residual_norm"] for r in rs])
        out[cond] = {"swap": round(st.mean([r["swap_log_odds_shift"] for r in rs]), 3),
                     "legs": round(st.mean([r["swap_log_odds_shift"] for r, i in zip(rs, ids)
                                            if qtype(i) == "legs"]), 2),
                     "name": round(st.mean([r["swap_log_odds_shift"] for r, i in zip(rs, ids)
                                            if qtype(i) == "name"]), 2),
                     "prop": round(st.mean([r["swap_log_odds_shift"] for r, i in zip(rs, ids)
                                            if qtype(i) == "prop"]), 2),
                     "capped": capped, "loops": loops, "edit_frac": round(ef, 4)}
    (B / "summary.json").write_text(json.dumps(out, indent=1))
    print("summary.json written")

if __name__ == "__main__":
    main()
