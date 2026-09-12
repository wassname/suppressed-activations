# Bounded 2×2 results: injection × removal at L20 (task 1149, 72 cells)

2026-09-12, PI[claude]. Run: pueue 1149, `slop/common_basis_2x2_batch.json`, one model load,
1027 s; protocol `slop/2x2_protocol.md`. Injection {δ_ref′ (the successful branch's runtime
norm-matched projection), v = Pd d} × removal {P_ref (rank 4), Ps (top8 union, bank
criterion 23/25/32)} at the SAME L20 single site, C=1.5, frozen donor, 12 dev questions.
A = the EXISTING reference path. Raw: `out/2026-09-12_cb-2x2/{condition}-{cell}/result.json`.

## Construction checks (verified, saved)

- Baseline drift: arm A vs the historical 2026-09-10 reference continuations: **12/12
  text-identical, 12/12 steered-logit-hash identical** (same runtime; no byte drift at all).
- A/B injected delta vector equality: B's `delta_ref_prime.sha256` — exactly 2 hashes (dog/
  ant, as expected: the delta depends only on the target concept); B's delta construction
  uses the same runtime code as A's applied delta; the earlier norms reconcile
  (‖δ‖ 6.81/5.70 raw, ×1.5 at C).
- C/D injected vectors: per-layer/per-position SHA256 equality **12/12** (identical donor
  vectors; only the removal differs).
- Provenance recorded per cell: bank layers [23,25,32] (per-token bases), reference path
  [18,20,32], removal span/rank per condition.

## Swap means (nats; construction-identical where noted)

| condition | injection | removal | swap ↑ |
|---|---|---|---:|
| A (baseline, existing path) | δ_ref′ | P_ref (rank 4) | **+10.01** |
| B | δ_ref′ (same vector) | **Ps (top8)** | **+9.85** |
| C | v = Pd d | P_ref | +0.43 |
| D | v = Pd d | Ps | +0.43 |

## Semantic outcomes (first lines; full texts in raw files; first answer alone not success)

| cell | A | B |
|---|---|---|
| legs-L1/L2-dog | `4` + dog identity, coherent ✔ | `2`/`4` + dog identity — digit wrong/partial |
| legs-L1/L2-ant | `6` + ant identity ✔ | `3` + red-ant identity — digit wrong, identity moved |
| name-N1/N2-dog | `狗 (Dog)` + dog identity ✔ | `狗 (Dog)` / `A dog.` + dog identity ✔ |
| name-N1/N2-ant | Ant/Bee/Honeybee list loops ✘ | honey bee identity (N1) / `**Ant**` list loop (N2) ✘ |
| property | source-bound/degenerate ✘ | spider-bound ✘ |

## Reading (labeled)

**The injection direction is the discriminating factor; the removal span is not.** With the
SAME δ_ref′ injection, swapping the removal span P_ref → Ps barely moves the outcome
(+10.01 → +9.85; naming-dog still transfers persistently). With the v injection, NEITHER
removal does anything (+0.43 both). The 2×2 locates the successful construction's active
ingredient in the injection direction (the template-label delta), not in the reference's
removal span. CAUTION (per protocol): direction and norm co-vary (‖δ_ref′‖ = 6.81/5.70 vs
‖v‖ = 1.92/1.77); removal rank/content differ (4 vs 8 dims); this locates a promising
combination, not isolated direction causality.

**New, unplanned observation**: B's profile DIFFERS from A's — A transfers legs+digit
(4/4) but loops on ant-naming; B transfers naming-dog identity AND moves legs identity
(dog/red ant) but not digits. The removal span interacts with WHICH content survives
(digit vs identity) — one comparison, hypothesis-grade.

## Status

Baseline preserved exactly (12/12 byte-identical). The 2×2 closes the first comparison
cycle with a located active ingredient. Open next candidates: δ_ref′ + Ps at matched-norm
controls (H9), digit-vs-identity site interaction, per-decode donor policies on top of the
δ_ref′ injection. Not queued — supervisor's call.
