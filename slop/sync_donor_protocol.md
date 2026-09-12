# Resolved protocol: donor-state updating vs frozen donor (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12): "Next bounded comparison
is donor-state updating". Changes ONLY donor-state evolution; everything else frozen.

- Construction: common_replace h' = h + 1.5(P_d d − P_s h); bases = per-token rank-8,
  bank selector (early,peak,output) = (23,25,32) [expected_detector_layers asserted in-spec];
  window last-4; top8_union arm only (U_s8/U_d8 = first 8 support-filtered SVD cols);
  site L25 (block 24); positions = last-3 prefill + every decode call.
- FROZEN arm: decode donor state = frozen final-prefill donor projection (as in 1130).
- SYNC arm: donor own prompt teacher-forced on EXACTLY the source-selected continuation
  tokens (separate KV caches; token-ID histories asserted equal per step; NO ground-truth
  answer fed); at each decode step d_t = donor's CURRENT h25 at its last position, projected
  with the FIXED U_d8; the source hook uses P_d d_t for that step. Step 0's donor state is
  the donor's final prefill state == the frozen arm's state, so step-0 (prefill) logits and
  the first token must be bitwise equal across arms — a construction check (asserted post
  hoc via saved first_logits_sha256), not outcome evidence.
- Controls: C0 identity for BOTH execution paths (C0_sync, C0_frozen). Random references:
  descriptive only, referenced from task 1130 L25-rand8 rows (identical selector/site/config
  family), not rerun. Old task 1007 was a different construction (shared_replace);
  distinction preserved.
- Measures: full 128/EOS continuations; per-task semantic answer/identity/coherence/format;
  self-correction incidence; per-call norms; synchronized_history token IDs.
- Cells: 48 = 12 questions × {sync_C1.5, C0_sync, frozen_C1.5, C0_frozen}; one model load.
- Prediction registered before execution (supervisor): if frozen-state staleness explains
  reversions, sync should preserve initially induced identity more often WITHOUT changing
  first logits; if both revert, this policy is insufficient (not all adaptive steering
  ruled out).
