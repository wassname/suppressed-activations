# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Cross-condition analysis of the common-basis batch (out/2026-09-11_cb-batch).

Reads each cell's result.json and produces: the cross-condition comparison table
(swap log-odds, answer mass, repetition, tokens, per-call norms), union-spectrum
support/effective-rank checks (numerical-null flags for full_union), and per-call
norm tables. Controls are rank-matched Gaussian projectors (descriptive), NOT
applied-norm matched. Written by PI[claude]."""

from __future__ import annotations

import json
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "out/2026-09-11_cb-batch"
CONDS = ("recovered-ref_C1.5", "per_token_C1.5", "full_union_C1.5", "top8_union_C1.5",
         "random_shared8_seed0_C1.5", "random_shared32_seed0_C1.5",
         "random_perpos8_seed0_C1.5", "C0")


def support_rank(s: list[float], n_cols: int) -> int:
    # same tolerance as the post-batch runner guard: numerical nulls only
    s1 = max(s)
    tol = max(n_cols, 1) * torch.finfo(torch.float32).eps * s1
    return sum(1 for v in s if v > tol)


def eff_rank(s: list[float]) -> float:
    lam = torch.tensor([v for v in s if v > 0]).square()
    return float(lam.sum().square() / lam.square().sum())


def main() -> None:
    rows, flags = [], []
    for cond in CONDS:
        for cell_dir in sorted(BATCH.glob(f"{cond}-*")):
            r = json.loads((cell_dir / "result.json").read_text())["rows"][0]
            cfg, pers = r["config"], r["persistence"]
            rec = list(r["intervention_record"].values())[0]
            trace = rec["replacement_trace"]
            # span_corrected_delta rows (recovered-ref) have no phase field: first call prefill, rest decode
            phase = lambda i, t: t.get("phase", "prefill" if i == 0 else "decode")
            prefill_norm = sum(t["applied_norm_after_dtype"] for i, t in enumerate(trace) if phase(i, t) == "prefill")
            decode_norm = sum(t["applied_norm_after_dtype"] for i, t in enumerate(trace) if phase(i, t) == "decode")
            n_calls = len(trace)
            row = {
                "cond": cond, "cell": cell_dir.name[len(cond) + 1:],
                "swap": r["swap_log_odds_shift"], "p_target": r["p_target"], "p_source": r["p_source"],
                "p_valid": r["p_target"] + r["p_source"], "r2": r["repeated_bigram_fraction"],
                "n_tok": r["generation_tokens"], "first_answer": r["first_answer"],
                "total_norm": rec.get("total_applied_norm"),
                "prefill_norm": prefill_norm, "decode_norm": decode_norm, "n_calls": n_calls,
                "decode_steps": rec["decode_steps"],
            }
            sv = pers.get("union_singular_values") or {}
            if sv.get("source"):
                n_cols = cfg["common_window"] * cfg["rank"]
                for side in ("source", "target"):
                    s = sv[side]
                    sup = support_rank(s, n_cols)
                    row[f"support_{side}"] = f"{sup}/{n_cols}"
                    row[f"effrank_{side}"] = round(eff_rank(s), 1)
                    if cond == "full_union_C1.5" and sup < n_cols:
                        # only full_union USES the unfiltered tail columns
                        flags.append(f"{cell_dir.name}: {side} union support {sup}/{n_cols} "
                                     f"(s_min={min(s):.3e}, s1={max(s):.3e}) -- full_union includes "
                                     f"{n_cols - sup} numerical-null columns; INVALID as union")
                    if cond == "top8_union_C1.5" and sup < 8:
                        flags.append(f"{cell_dir.name}: {side} support {sup} < 8 -- top8 truncated to support")
            rows.append(row)
    out = {"rows": rows, "flags": flags}
    (ROOT / "out/2026-09-11_cb-batch/analysis.json").write_text(json.dumps(out, indent=1))
    print(f"{len(rows)} rows, {len(flags)} support flags")
    for f in flags:
        print("FLAG", f)


if __name__ == "__main__":
    main()
