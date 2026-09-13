# Bridge proposal: historical operator × selector × site (proposal, no GPU queued)

Author: PI/glm-5p3-flash, 2026-09-13. CPU preparation only; GPU waits for supervisor
review. Historical 6/12 stays frozen; the reused dog/ant pairs are development data.

## Source-level feasibility (read from current code, cited)

1. The historical successful operator EXISTS in current code:
   `span_correction_configs` (scripts/oat_sweep.py:245) = template-contrast +
   template_state_span="attenuation" + persistent_rank=4 + match_component_norm=True
   (ACTIVE) + span_correction=True (h' = h + C(Δ − UUᵀh)), detector (18,20,32),
   intervention (20,), 3 positions, continue_generation=True — the replay recipe.
2. The basis is built from the TEMPLATE-CONTRAST contrasts at detector_layers
   (oat_sweep.py:2760-2768: peak/output = contrasts[:, detector_layers[1/2]];
   attenuation_basis(peak, output, persistent_rank)) — the SELECTOR coordinates are
   the detector layers; with a single edit layer the shared basis is site-INDEPENDENT
   (oat_sweep.py:2764 runs once; the per-layer local selectors only activate for
   multiple intervention layers, oat_sweep.py:2923).
3. The DONOR STATE is SITE-TIED in this family: the injected delta is the donor's
   residual at the intervention layer (fixed_deltas=None path); there is NO explicit
   anchor parameter here (xdepth_anchor_layer belongs to the increment families).
   So "fixed donor anchor 20 across sites" is NOT expressible without a code change —
   the honest site move sets intervention_layer=(8,) and the donor state moves to
   layer 8 with it (faithful historical semantics; site and donor depth confounded
   BY THE OPERATOR, recorded as such).
4. Crossing the increment selector INTO this operator = a new framework (the
   operator's basis IS the template contrast) — NOT built. The selector axis is
   covered by existing runs instead (see overlap check).

## Existing-runs overlap check (no equivalent cells missing except one)

- selsite/complete-rank families: selector {snapshot?, increment} × site {h8, h20}
  with the CURRENT (top8_union/joint) operator — already run (1182/1230-era).
- span_correction replay: the HISTORICAL operator at h20 only (the success).
- MISSING and proposed: the historical operator at h8 (+ C0) — the one cell that
  tests whether the successful operator survives an earlier site.

## Proposed compact matrix (per donor: dog, ant — 2 reused development pairs)

| cell | operator | selector coords | edit site | donor state | C |
|---|---|---|---|---|---|
| replay-h20 | span_correction (template-contrast attenuation, rank 4, norm-matched) | detector 18/20/32 | 20 | layer 20 (site-tied) | 1.5 + C0 |
| early-h8 | SAME operator/coords | detector 18/20/32 (unchanged) | 8 | layer 8 (site-tied) | 1.5 + C0 |

6 rows total (2 cells × 2 donors × {C1.5, C0}) + the historical h20 snapshot replay
requirement: the replay-h20 cell must first reproduce the saved 2026-09-10
full continuations (byte/token comparison against the snapshot JSONs) before the
h8 cell is interpreted — if the current code does not replay the historical rows,
the drift is the first finding and the h8 cell is not comparable.

## Equation (both cells, the operator's own)

h' = h + C(Δ − U Uᵀ h) with Δ = the donor residual at the edit site, U = the
template-contrast attenuation basis (4-dim, persistent template retained),
component-norm matching ACTIVE (upstream), no residual renormalization.

## Tiny real-path tests (already runnable, CPU)

- smoke_span_correction family = the tiny real path for this exact operator
  (oat_sweep.py:250-260); a dispatch test running one tiny condition through
  run_with_bundle (same pattern as test_real_noncomplete_joint_smoke) — to add.
- Persist full replacement traces at source before asserts (done for future batches
  in anchor_control.py; apply the same to the runner when queued).
