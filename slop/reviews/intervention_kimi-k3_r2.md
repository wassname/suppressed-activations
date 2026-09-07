# Revised review

**Withdrawn.** (1) The reflection claim: with `w=(v_s−v_t)/‖v_s−v_t‖`, the swap is exactly a Householder reflection; C=1 is norm-preserving regardless of column nonorthogonality, and the pinv/QR critique was wrong. (2) The `B[t]` critique: orthonormal blocks make `mean(BB^T)` a genuine average of projectors and thin SVD exact; no hidden-covariance assumption is smuggled in. (3) C0 identity controls exist; I miscounted.

**Retained, with reasons.**

- *Success definition is still unsettled.* The digit flip is compatible with three hypotheses: concept replacement, logit-aligned bias along `v_target`, or generic disruption. Your own note (8) concedes global cosine can't arbitrate. The arbitrator must be **cross-task behavioral**: after the patched model says "4," does its *explanation* attribute 4 legs to the dog, does it volunteer dog-consistent properties (barking) unprompted, and is it self-consistent given the unchanged web clue? Define success as emitted digit = named animal = leg-count rationale, all agreeing with the target. Score this, not p(digit).
- *Random/wrong-animal norm-matched controls* remain the cheapest way to keep the candidate-selection honest; agreed they are filters, not verdicts.
- *Projection fractions logged* (ant raw cos .137 vs projected .667) is itself diagnostic: raw and projected directions encode different things; treat them as separate hypotheses in the grid, not variants.

## Cheapest compelling next test: matched template contrast

It reuses forward-only infrastructure (~2s/condition), needs no corpus, no backprop, no VJP variance analysis. VJPs are the better-motivated estimator (causal future effect) but cost an order of magnitude more and add estimator-noise questions; defer until contrast fails informatively.

**Exact protocol:**

1. **Extraction.** K≥6 templates differing only in the animal token, identical suffix. `d_L = normalize(mean_templates mean_last3suffix (h_target − h_source))` at L ∈ {4, 12, 20, 24}.
2. **Calibration.** Set α so `α·‖d_L‖` equals the measured source↔donor prompt displacement `‖h_donor − h_source‖` at that layer (α=1 = full donor distance). Sweep α ∈ {0.5, 1, 2} — this anchors dose to a natural scale instead of an arbitrary C.
3. **Application.** Additive, continuous through generation (per requirement 4), at all decode steps; compare full-residual vs suppressed-space-projected `d_L` as separate arms, with one-sided gating (only when source coordinate exceeds target) as a third.
4. **Controls in the same batch:** norm-matched random direction; mismatched-animal direction (extract dog, test ant prompt). Candidates that don't beat both are rejected regardless of digit output.
5. **Readout:** the self-consistency triple above, plus unprompted target-attribute rate in free continuation.

If the contrast direction at α=1 yields coherent target-consistent continuations where named swaps didn't, the named-unembedding estimator (not the swap operator) was the bottleneck — then VJPs become worth their cost as the refinement.