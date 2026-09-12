# Cross-depth donor results (task 1194, 48 cells)

2026-09-12, PI[glm-5p3-flash]. Run: pueue 1194, `slop/common_basis_xdepth_batch.json` (full
contracts validated pre-model), one model load, 499 s; protocol `slop/xdepth_spec.md`.
INCREMENT selector, h8 site, joint removal, C=1.5 — ONLY the donor vector construction
varies. Raw: `out/2026-09-12_cb-xdepth/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| condition | injected vector | inj. norm (mean) | swap ↑ | capped | loops |
|---|---|---:|---:|---:|---:|
| v8 replay | Pd d8 (same-depth) | 0.26 | +0.02 | 0/12 | 0/12 |
| v25 imported | Pd d25 (late-built, imported to h8) | 3.74 | +0.13 | 2/12 | 1/12 |
| v8 rescaled | v8 direction at ‖v25‖ | 3.74 | +0.46 | 3/12 | 3/12 |
| C0 | identity | 0 | 0.00 exact | 0/12 | |

Same-depth replay regression: **12/12 first-logit hashes identical to 1182's increment-h8**
(config/vectors/first-logits match; no drift).

## Semantic outcomes (EXACT per-row: 24 rows in `per_row_verdicts.json` with quotes;
answer/identity/factuality/repetition judged separately vs each output's own base)

- v25 imported: 4/12 rows give the DONOR-CORRECT answer (both spinneret rows + liveyoung-ant
  No) — always with SPIDER identity and FALSE factual claims ("Spiders do not possess
  spinnerets" — they do; "do not have lungs; they have book lungs" — they do; fabricated
  species "Latrodectus hassidii"); 1 loop; the rest clean spider.
- v8 rescaled: 2 rows repeat "No" to the cap (r2 0.72); 1 block-loop; the donor-correct
  liveyoung-ant No with spider identity; the rest clean spider.
- COHERENT DONOR TRANSFER ABSENT is the supported claim — the rows are NOT "clean spider
  everywhere": there are donor-correct answers, false-fact off-target effects,
  self-contradictions, fabricated species, and loops (4 off-target/false-fact rows,
  4 loops).

## Verdict (registered branch (iii), scoped)

Both non-replay conditions fail to produce COHERENT DONOR TRANSFER: these levels/
constructions are insufficient. Importing the late-built donor component (norm 14× paired;
see energy below) does not transfer; rescaling v8 to the late size does not either. The
early idea is NOT declared impossible — this construction (Pd-projected donor states under
the joint operator at h8) is.

## Standing (tested settings; withdrawals applied)

- WITHDRAWN: "the Pd-projected donor injection is behaviorally null at every depth/norm/
  selector" — the tested rows include donor-correct answers, off-target/false-fact effects
  and loops; "null" only described the earlier aggregate swaps, not the outputs.
- WITHDRAWN: "the template-label δ_ref′ direction remains the only transferring injection"
  (global) — B's 3/12 and the v@δ-norm 1/12 remain the observed counts at their tested
  settings; no general claim.
- Magnitude units: the 14× is the PAIRED NORM ratio (v25/v8 per offset); the ENERGY ratio
  is per-row squared (≈14² ≈ 196 only where the paired ratio is 14; per-row squared ratios
  in cross_depth_increment.json rows) — no squared aggregate.
