# Resolved protocol: current-reference ablation — injection-only / removal-only (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12). At L20 C1.5, same 12
questions, the SAME applied delta'/P_ref constructed ONCE by the runtime sweep code
(template corpus forwards -> attenuation_basis -> projection + match_component_norm
rescale); no reprojection/renorm after condition selection.

- Conditions (4 × 12 = 48 cells, one model load):
  1. injection-only: h + C·δ_ref′ (existing fixed_delta op; no span removal).
  2. removal-only: h − C·P_ref h (new remove_scaled op — same C, no norm restore, matching
     A's removal component in magnitude and form).
  3. A replay: both (existing span-correction path).
  4. C0: identity.
- Historical job-500 ablation (different operator/basis era) is motivational only; no
  general alignment structure inferred from it.
- Registered predictions (supervisor): injection-only retaining A's naming/legs successes
  supports sufficiency at these inputs; removal-only digit change WITHOUT donor identity
  indicates answer bias, not transfer; neither alone but both coherent → combination
  needed at this setting. Removal can still affect identity/digits despite aggregate-shift
  similarity.
- Measures: full 128/EOS continuations; exact per-row verdicts/quotes; semantic/format
  separate (no first-answer proxy); per-call norms; applied_delta_sha256 equality
  (injection-only == A) asserted in-run and re-checked at analysis.
