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

## Semantic outcomes (full continuations read)

- v25 imported: clean spider everywhere (name-N1-dog `蜘蛛 (Spider)…`; name-N2-dog
  `Spider…`); 2 capped (long coherent, r2 ≤ 0.04), 1 mild loop. NO donor answer, NO donor
  identity.
- v8 rescaled: clean spider everywhere; 3 capped, 3 mild loops (r2 ≤ 0.20) — slight
  degradation with size, no transfer.

## Verdict (registered branch (iii))

**Both non-replay conditions fail to transfer: these levels/constructions are insufficient.**
Importing the late-built donor component (14× larger, cos 0.26 different direction) does
not transfer; rescaling v8 to the late size does not transfer either (slight degradation).
The early idea is NOT declared impossible — this construction (Pd-projected donor states
under the joint operator at h8) is.

## Standing (tested settings)

The Pd-projected donor injection is behaviorally null at every tested depth (h8/h20),
norm (0.26–3.74), and selector; the template-label δ_ref′ injection remains the only
transferring direction (2×2 A/B; ablation injection-sufficiency). Magnitude was tested
directly here: 14× more donor-projection energy does not create transfer.
