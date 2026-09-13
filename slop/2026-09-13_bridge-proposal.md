# Bridge proposal v2: corrected historical formula + code-change map (CPU only)

Author: PI/glm-5p3-flash, 2026-09-13. Supersedes the v1 feasibility errors (fixed_deltas
is NOT None; the delta is NOT a raw donor residual). No GPU; tiny tests with NONZERO C.

## The ACTUAL historical formula (traced end-to-end, current code lines cited)

1. `template_deltas` (scripts/oat_sweep.py:2632-2655): for each template in
   CONCEPT_TEMPLATES, render spider vs donor template pairs (generate=False,
   extraction_instruction); take the last-3-position suffix residuals
   `(donor − spider)` at every layer; **average over the 3 positions** (`.mean(1)`)
   then **average over templates** (`torch.stack(differences).mean(0)`) →
   `template_deltas[layer] = (hidden,)` per layer. Template provenance (the exact
   rendered pairs) is recorded in persistence ("matched_template_mean_difference",
   "rendered_template_pairs"). The legs-donor PROMPT is not an input to this delta.
2. `shared` (U): the attenuation basis (persistent_rank=4) from the template
   contrasts at detector_layers peak=20/output=32 (oat_sweep.py:2741-2768),
   orthonormal.
3. `projected = component(delta, shared)` per layer; **norm matching SCALAR per
   layer**: `projected * delta.norm() / projected.norm()` +
   `assert_close(projected.norm(), delta.norm())` (oat_sweep.py:2849-2852).
4. `span_correction=True` → `source_basis = target_basis = shared`
   (oat_sweep.py:2858-2861); edit `h' = h + C(Δ̃ − U Uᵀh)` with Δ̃ = the norm-matched
   projected template delta at the edit layer; `applied_delta_sha256`/norm recorded
   (oat_sweep.py:2865-2872) for exact cross-arm equality.

Norm axes: the delta and its norm are PER-LAYER SCALARS over the hidden dim
(position-averaged); no per-position axis in the historical delta.

## The 2×2×2 = 8-row matrix (dog, ant × selector × site)

- U ∈ {attenuation-4 (historical), increment-selected joint (trajectory-selected,
  multi-token union/SVD — same orthonormal-U interface)}
- edit site ∈ {20, 8}; delta = `template_deltas[20]` FIXED (explicit anchor; norm
  matching computed at layer 20) in all rows — reads template_deltas[20], keyed by
  edit site
- donor ∈ {dog, ant} — via the template pairs (the template machinery already takes
  the donor concept); the reused legs pairs are development data
- All rows: C1.5, 3 positions, continuous decode policy, same replacement hook.

## Code-change map (IMPLEMENTED; tiny tests passing)

1. `delta_anchor_layer: int = -1` cfg field (-1 = site-tied historical default):
   `fixed_deltas = {site: template_deltas[anchor]}` when >= 0 (oat_sweep.py:2722-2728).
2. `basis_selector: str = "attenuation"` (historical) | `"increment"`: a branch at the
   HEAD of the shared-basis chain (BEFORE projection/norm-matching): per-position
   `subspace_from_scores` bases at the READOUT positions (content_end-anchored,
   independent of intervention_positions) for BOTH source and donor trajectories,
   CONCATENATED before orthonormalization, SVD, support = tolerance count (asserted
   >= persistent_rank), truncated to persistent_rank. Union kept before the SVD.
3. Downstream (projection, SCALAR per-layer norm matching, span_correction hook,
   applied-delta hash) unchanged; an in-run assert requires the injected delta inside
   the active basis.

## Tiny tests (historical replay with NONZERO C — C0 cannot validate the intervention)

a. historical replay (tiny, C1.5): the applied delta hash == the norm-matched
   projected template delta hash; `assert_close(projected.norm(), delta.norm())`.
b. projector independence: the template U identical across edit sites (site does not
   enter the basis).
c. anchor consumption: with delta_anchor=20 at site 8, the applied delta hash equals
   the layer-20 delta hash (not the layer-8 one).
d. C0 inert (already covered elsewhere; kept as the cheap sanity row).
