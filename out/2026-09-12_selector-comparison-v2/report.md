# Selector comparison v2 (canonical readout; corrected)

2026-09-12, PI[glm-5p3-flash]. CORRECTION of the invalid first attempt (preserved at
`../selector-comparison-invalid-readout/`): its readout applied the norm gain TWICE (h-side
and row-side); this version uses the canonical once-gain convention and an EXECUTED
regression asserts, per prompt, that the snapshot scores equal
`suppressed_activation_scores(normalize_unembedding_rows=True)` on the same saved tensors.
Script: `scripts/selector_comparison.py` → `selector_comparison.json`. Exact-input bank
(task 1174: pinned revision, exact wrapper, 24/24 ID equality vs actual runs).

## What was computed (actual statistic)

Per prompt: the top-8 vocabulary sets over the last-4 window positions under (1) the
existing 3-snapshot selector (rise ϕ25−ϕ23, fall ϕ25−ϕ32, centered, rectified, min) and
(2) the positive-increment candidate (Σrelu(Δϕ) over build b13..b23 vs Σrelu(−Δϕ) over
writes b29/b30/b31, centered before rectification). Reported: VOCABULARY-SET Jaccard
between the two selections. NO basis geometry (QR/SVD/principal angles) is computed here —
that would be a separate calculation if needed.

## Result

**Jaccard = 0.020** (min 0.000, max 0.158, 24 prompts) — the two selectors pick largely
different vocabulary sets on exact inputs. (The invalid first attempt gave 0.026 — the
conclusion of large divergence survives the readout correction.)

## Selected-token per-layer traces (numerator + RMS; the buildup evidence)

`selector_comparison.json` now saves, per prompt, the per-layer RAW gain-weighted numerator
and the RMS denominator for the candidate-selected tokens (8 tokens × 33 layers + RMS) —
the trace-level evidence for WHERE the selected tokens build and fall, separating readout
numerator loss from RMS growth. Example (legs-L1-dog source): the candidate selects
leg-topic vocabulary (` legs`, ` leg`, `_leg`, `-legged`); its numerator trace shows the
build/fall shape over depth (numbers in the JSON). Sample decoded labels suffice; no
debris-semantics generalization is made from them.

## Scope

Vocabulary-set agreement only; no basis geometry, no behavior, no specificity battery.
Score-scale comparisons between the selectors are omitted (summed scores are not
comparable units). Next smallest CPU step if wanted: build-window edge sweep for set
stability; then donor-answer-presence/cross-prompt overlap descriptions.
