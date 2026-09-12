# Resolved protocol: interval-wise re-correction (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12). Tests whether maintaining
the edit through intermediate computation prevents reversion.

- Construction frozen: common_replace h' = h + 1.5(P_d d − P_s h); bank selector (23,25,32);
  top8_union (U_s8/U_d8 = first 8 support-filtered SVD cols, FIXED and SHARED across the
  whole interval); window 4; positions = last-3 prefill + every decode call; frozen decode
  donor policy (final prefill state); C = 1.5.
- INTERVAL arm: the edit applied at EVERY residual boundary h25..h30 (layers 25,26,27,28,29,30
  = blocks 24..29; exactly six sites per call). Donor residual for EACH layer from that
  ACTUAL layer (end-aligned offsets), projected with the fixed U_d8.
- Endpoint replays: L25-only and L30-only (same config, single site).
- Controls: C0 interval (exact identity asserted); random-projector interval (seeded shared
  rank-8 Gaussian projectors at all six sites, real donor states) — DESCRIPTIVE, NOT
  dose-matched: more sites means more cumulative intervention, explicitly not a pure timing
  effect.
- Cells: 60 = 12 dev questions × 5 arms; one model load; expected_detector_layers=[23,25,32]
  asserted per cell.
- Measures: full 128/EOS continuations; full semantic verdicts with quotes (first answer
  alone is not success); per-layer per-call normalized edit norms; self-correction incidence.
- Registered prediction (supervisor): improved persistent identity if single-site overwrite
  is addressable this way; unchanged source or degradation ⇒ this interval/procedure
  insufficient.
