# Resolved protocol: full-temporal vs top8 joint removal (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12): returns to the user's
full-union vs top8 question under the accumulation-safe equation.

- Frozen: interval h25..h30 (six sites per call, blocks 24..29), C=1.5, FROZEN donor,
  bank selector (23,25,32) asserted per spec cell, window 4, positions last-3 + all decode,
  injection v = Pd d unchanged everywhere; joint removal = support-filtered span of
  [U_s | U_d] (shared numerical support helper everywhere; v containment asserted <1e-5
  per layer/position at runtime).
- ONE VARIED AXIS: TEMPORAL TRUNCATION —
  1. fulljoint_C1.5: U_s/U_d at FULL temporal support (rank ≤32 each; joint support over
     [U_s|U_d]); PRIOR full-union tests used a DIFFERENT removal operator (Ps-only) —
     comparison labeled accordingly.
  2. top8joint_C1.5: replay of 1138's joint arm (temporal top8 then joint).
  3. fulljoint_random: rank-matched random full-joint same operator (seeded random U_s/U_d
     at rank 32, joint support; DESCRIPTIVE — not norm-matched).
  4. fulljoint_C0: identity control.
- Cells: 4 × 12 = 48; one model load. No source+donor joint truncation mixed (support
  computed on the concatenated FULL bases).
- CONFOUNDS EXPLICIT: temporal truncation co-varies with removal rank, donor content, and
  applied norms — not a pure rank axis; do not assume energy is semantics.
- Registered prediction (supervisor): top8 may discard useful donor directions (descriptive
  basis capture ~30%); full support may improve persistent identity, or cause unrelated
  changes / leave spider unchanged.
- Measures: full 128/EOS continuations; full semantic verdicts with quotes; per-site
  per-call normalized edits; loop vs length-cap recorded separately.
