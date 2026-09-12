# Resolved protocol: bounded 2x2 — injection x removal at L20 (saved before execution)

2026-09-12, PI[claude]. Authorized by supervisor (seq 2026-09-12 "Go: bounded2x2").

- Site: L20 ONLY (single site; no interval accumulation). C=1.5. Positions last-3 + every
  decode call; frozen donor. Same 12 dev questions.
- Injections: (i) delta_ref' = the successful branch's applied vector — built IN-RUNTIME by
  the sweep's own template-attenuation code (template corpus forwards, attenuation_basis,
  projection + match_component_norm rescale), then kept EXACTLY fixed when the removal span
  changes (never reprojected); (ii) v = Pd d per position/end-aligned + frozen final-prefill
  decode state (the current construction).
- Removals: P_ref (the rank-4 attenuation basis from the same runtime code; reference
  criterion 18/20/32 via cfg.detector_layers) and Ps (bank-criterion 23/25/32 top8 temporal
  union; common_bank_layers decoupled from cfg.detector_layers in this family).
- Conditions (72 cells): A baseline = EXISTING span-correction-sweep idx 3 path (12);
  B = delta_ref' + Ps removal (12); C = v + P_ref removal (12); D = v + Ps removal (12);
  C0-Pref (12); C0-Ps (12). One model load.
- Equivalence/construction checks: delta_ref' is computed by the same runtime code for A and
  B (deterministic same-process forwards) — norms recorded per cell and asserted equal in
  analysis; historical byte drift of arm A vs the 2026-09-10 reference continuations
  reported separately, not silently widened.
- CAUTIOUS INTERPRETATION (per supervisor): direction AND norm differ across injections;
  removal rank/content differ across removals — the 2x2 locates a promising construction
  combination, not isolated direction causality. Full semantic outcomes/quotes per cell;
  per-call actual edit norms and donor info recorded.
- PRIORITY: baseline preservation. If arm A fails same-runtime equivalence (historical
  drift beyond roundoff), STOP the new batch and fix the implementation first.
