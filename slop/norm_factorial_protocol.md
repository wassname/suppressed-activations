# Resolved protocol: injection direction × injection norm factorial (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12). Isolates injection NORM
vs DIRECTION with the SAME L20 site and P_ref removal held fixed.

- Frozen: L20 single site, P_ref removal (rank 4), C=1.5, last-3 prefill + all decode,
  frozen donor, selector assertion (detector [18,20,32] reference path; bank [23,25,32]
  per-token bases — recorded per cell), same 12 dev questions.
- Factorial (per matched prefill position; decode = offset-1 policy):
  1. A replay: δ_ref′ at OWN norm (existing span-correction path) — ‖δ‖ = 6.81/5.70.
  2. δ_ref′ direction scaled per-position to ‖v_o‖ (≈1.9/1.8) — rescale preserves direction
     (asserted: cos = 1.0 exactly, target norm exact; recorded per cell).
  3. C replay: v at OWN norm (existing 2x2 C path).
  4. v direction scaled per-position to ‖δ_ref′‖ (≈6.8/5.7).
  5. C0 (identity).
- 60 cells = 12 × 5; one model load. NO reprojection of either vector; total edits still
  depend on direction+source state — this equalizes injection magnitude at the matched
  site/position ONLY, not total edit or semantic strength.
- Registered prediction (supervisor): (a) template direction retains coherent transfer at
  low norm → direction-specific advantage; (b) high-norm v improves → magnitude
  contributed; (c) only high-norm delta works → direction and sufficient magnitude jointly
  needed. Judge full identity/answer/coherence separately.
- Vector hashes recorded per cell (unscaled delta_ref, injected vectors) — A-vs-1149 hash
  continuity + A/B equality verifiable exactly.
