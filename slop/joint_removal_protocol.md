# Resolved protocol: same-injection comparison — original vs joint-span removal vs restricted

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12, "authorize SAME injection
comparison"). Tests the predicted removal of outside-source accumulation and its behavioral
consequence; NOT isolated semantic cause.

- Frozen: common_replace equation, C=1.5, interval h25..h30 (six sites per call, blocks
  24..29), bank selector (23/25/32) with expected_detector_layers asserted per spec cell,
  top8 TEMPORAL source/donor bases first, then the JOINT support over [U_s8 | U_d8]
  (support-filtered, rank 16 = 8+8 typically), window 4, positions last-3 + all decode,
  FROZEN donor (final prefill state; no sync change).
- Conditions (4 × 12 = 48 cells):
  1. original_C1.5: removal = Ps (rank 8), injection = Pd d — replay of the interval arm
     (accumulates ~80% of the injection outside Ps, coherent direction, per algebra.json).
  2. joint_removal_C1.5: removal = P_union (rank ~16), SAME injection v = Pd d — v lies in
     the joint span (containment asserted per layer/position at runtime, <1e-5); toy: no
     accumulation, stable for 0<C<2, C=1 idempotent (CPU-verified, saved).
  3. restricted_inject_C1.5: removal = Ps, injection = Ps(Pd d) — accumulation control that
     drops the outside-donor part (~70% energy).
  4. joint_C0: identity control on the joint-removal path.
- CONFOUNDS EXPLICIT: joint removes ~16 dims not 8 (more removal rank); restricted injects
  ~36% of the injection energy (reduced injection). Neither is a pure accumulation test;
  the pair brackets the mechanism.
- Measures: full 128/EOS continuations; full semantic verdicts with quotes (first answer
  alone not success); per-site per-call edit/residual norms; original outside-source
  injection vs joint containment recorded per cell; loop/repetition incidence.
- Registered prediction (supervisor): joint removes the toy accumulation; if transformer
  loops also drop, that supports utility — but only coherent donor identities improve the
  goal. If less looping but spider unchanged: stability improvement distinguished from
  transfer.
- No C1 GPU (CPU identity diagnostic only, already saved in algebra.json).
