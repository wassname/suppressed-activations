# Common-basis batch report (task 1072, 96 cells)

Written 2026-09-11 by PI[claude]. Run: pueue task 1072, `slop/common_basis_batch.json`,
one model load, 918 s. Model Qwen/Qwen3.5-4B rev 851bf6e8. 12 dev questions (the exposed
fresh cells) × 8 conditions, full 128-token continuations, continuous last-3-prefill + decode
coverage (asserted per cell), C=1.5, L20, window 4, positions 3. Equation under test:
`h' = h + C (P_d d_p − P_s h_p)`; recovered reference keeps its own equation
`h + C(δ − P_ref h)` (template-attenuation common rank-4). Randoms are rank-matched
seeded Gaussian projectors with real donor states — DESCRIPTIVE controls, NOT
applied-norm matched. Raw rows: `analysis.json` (this dir), per-cell `result.json`.

## Cross-condition means

| condition | swap log-odds ↑ | p(target) ↑ | p_valid ↑ | r2 ↓ | tokens | total norm | prefill | decode |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| recovered-ref C1.5 | **+10.01** | 0.327 | 0.328 | 0.122 | 86.1 | 778.5 | 19.8 | 758.8 |
| per_token C1.5 | +0.20 | 0.008 | 0.338 | 0.017 | 66.0 | 128.4 | 2.7 | 125.6 |
| full_union C1.5 | +0.60 | 0.009 | 0.334 | 0.025 | 74.1 | 443.1 | 8.8 | 434.2 |
| top8_union C1.5 | +0.25 | 0.011 | 0.334 | 0.015 | 73.3 | 152.1 | 3.1 | 149.0 |
| random_shared8 | +0.06 | 0.007 | 0.338 | 0.011 | 61.4 | 105.0 | 3.0 | 102.0 |
| random_shared32 | −0.03 | 0.005 | 0.337 | 0.029 | 72.9 | 277.5 | 5.9 | 271.6 |
| random_perpos8 | −0.06 | 0.005 | 0.342 | 0.013 | 66.3 | 120.5 | 2.9 | 117.7 |
| C0 | 0.00 | 0.007 | 0.339 | 0.009 | 62.7 | 0.0 | 0.0 | 0.0 |

Per-cell swap table and per-call norms: `analysis.json` (fields `swap`, `total_norm`,
`prefill_norm`, `decode_norm`, `n_calls`, `decode_steps`). Per-cell `first_answer` saved.

## Why the replacement barely edits: component scale

| condition | donor-proj norm mean | donor-state norm mean | proj/state |
|---|---:|---:|---:|
| per_token | 0.95 | 15.35 | 0.062 |
| full_union | 3.18 | 15.35 | 0.207 |
| top8_union | 1.14 | 15.35 | 0.074 |
| random_shared8 | 0.78 | 15.35 | 0.051 |
| random_shared32 | 1.65 | 15.35 | 0.108 |

The recovered reference's selected component norm at C=1.5 is 9.39 per token — 3–10× the
entire donor-proj vector of the replacement constructions, applied against a residual whose
L20 norm is ~17. The suppressed subspaces hold only 5–20% of the donor state, so
`P_d d_p` is small by construction; the reference's effect lives in its large additive
template delta, not in a projector replacement.

## Continuations (observed)

All three common-basis constructions leave the generation at the clean-source answer and
identity (e.g. per_token legs-L1-dog: `8

The spider is an arachnid that typically has
eight legs…`; full_union name-N1-dog: `蜘蛛 (Spider)

The spider is an arachnid…`).
No repetition loops (r2 ≤ 0.12), EOS terminations, coverage asserted (decode_steps =
tokens−1, trace = prefill+decode). The only cells with any notable movement are
full_union name-N1/N2-dog (+2.41/+1.52) — still no answer change.

## Union support / effective rank (numerical-null audit)

44 flags, all in `full_union`: 1–8 numerical-null columns per cell (s_min ~1e-7 vs s1 ~1.4),
support 24–31/32, effective rank 18.9–31.3 of 32. `top8_union` is within support everywhere
(min support 24 > 8). No cell is severely rank-deficient; the flagged columns are arbitrary
directions included by the unfiltered thin SVD in THIS run. Fixed for future runs: the
runner now support-filters the union basis (tolerance `max(shape)·eps·s1`), records
`union_support` in persistence, and never conceals a changed rank (smoke re-passed,
`out/b13_smoke_common/`).

## Interpretation (labelled inference)

At matched C=1.5/L20/window-4, the projector-replacement equation is an order of magnitude
too weak to move behavior: the suppressed subspaces carry only 5–20% of the donor state, so
the additive term `C·P_d d_p` (norm ~1–5) cannot compete with the reference delta (norm ~9.4
selected component, total applied ~778 over the trajectory). This does NOT show the union
constructions are causally inert at all strengths — it shows C=1.5 is the wrong scale for
this equation, and that the recovered reference's transfer rides its large template delta.
The natural one-at-a-time next axis (not run, not authorized yet): per-call applied-norm
matching to the reference (strength rescale), holding layer/window/positions fixed.

## Provenance

- Spec: `slop/common_basis_batch.json` (96 entries, condition indices 0–7).
- Per-cell: `out/2026-09-11_cb-batch/{cond}-{cell}/result.json` (+ `run.md`, condition logs).
- Analysis: `scripts/analyze_cb_batch.py` → `analysis.json`.
- Guard commit: support-filtered `union_basis` in `scripts/oat_sweep.py`.
