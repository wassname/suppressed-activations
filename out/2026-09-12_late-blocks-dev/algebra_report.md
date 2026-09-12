# Algebra discriminator: why the interval degenerated, and the correction candidates

2026-09-12, PI[claude]. CPU only; measured on the saved dev-bank bases/states
(`scripts/algebra_discriminator.py` → `out/2026-09-12_late-blocks-dev/algebra.json`; 12
cells × 3 end-aligned positions). Toy simulations use IDENTITY between sites — toy algebra,
NOT transformer evidence; the real 1136 interval had blocks between sites.

## The operator and its exact algebra

T(h) = (I − C·Ps)h + C·v with v = Pd d, Ps ≠ Pd, C = 1.5. Left-multiply by (I − Ps):

    (I − Ps)T(h) = (I − Ps)h + C·(I − Ps)v

With a fixed donor the OUTSIDE-SOURCE component accumulates linearly; within Ps the
coefficient is 1 − C = −0.5. Not idempotent replacement.

## Measured (actual bases/states, means over 12 cells × 3 positions)

1. **Outside fraction of the injection** ‖(I−Ps)Pd d_l‖/‖Pd d_l‖: **0.78–0.80 at every
   layer** h25..h30 (v norms 4.6→6.1). ~80% of each injection lands OUTSIDE the removal
   span.
2. **Signed cross-layer agreement of those outside components**: cosines **+0.90 to
   +0.98** (all 15 pairs) — the accumulated vector points in nearly the SAME direction at
   every layer. No alignment was assumed; it is measured.
3. **Toy simulations** (start = actual clean source h25; per-position means):

| operator (6 steps) | outside: k1→k6 | source-span: k1→k6 | behavior |
|---|---|---|---|
| current, frozen v | 27.9 → 42.9 | 2.90 → 2.29 (→ \|1−C\| fixed point) | linear outside accumulation |
| current, actual per-layer v_l | 27.9 → 45.3 | 2.90 → 3.15 | ≈ frozen (cross-layer cos ≈ 0.95) |
| **shared P_union removal, C=1.5** | **27.04 constant** | 2.90 → 3.15 oscillating-converging (\|1−C\|<1) | stable fixed point |
| **shared P_union removal, C=1** | 27.04 constant | k2 ≈ k1 (2.28 → 2.25) | **exact idempotence** |
| restricted injection Ps·Pd d, C=1.5 | 27.12 constant | 2.90 → 3.15 | no accumulation, drops the outside 80% of v |

The toy matches the algebra exactly. Union support is 16 = 8+8 at every cell: the source
and donor top8 spans are DISJOINT, yet 20% of v lies along source-span directions.

## Interpretation (labeled)

The interval degeneration is CONSISTENT with the measured accumulation: six sites each
added C·(I−Ps)v_l ≈ 0.8·C·‖v‖ in a nearly fixed direction (cos ≥ 0.90) — a large coherent
injection nothing removes. This is a mechanism hypothesis consistent with the toy + the
real degeneration, not a proof (the real interval also had blocks between sites and
unmatched cumulative dose).

## Recovery: this correction is NOT novel structure

The recovered frozen candidate h + C(δ − P_ref h) already has δ ∈ span(P_ref) (its
template-attenuation delta is projected onto the shared basis before injection, sweep-side:
`projected = {layer: component(delta, shared)}`). So the reference NEVER had the
accumulation failure mode — its injection lives in its removal span. Earlier joint-span
constructions also exist: `persistent_shared_basis` (joins source+donor spans, used by the
shared_replacement families, task 1007 era) and the synchronized-donor variants. The
candidate below re-derives the candidate's structure on the per-token union bases; the
unifying reading (reference works BECAUSE δ ∈ removal span; the new operator failed
BECAUSE v ⊄ span(Ps)) is a hypothesis consistent with all measured evidence so far.

## Candidate evaluation (supervisor's proposal; math checked, NOT auto-approved)

- **Shared P_union removal**: h' = h + C(v − P_union h), P_union = support-filtered span of
  [U_s8 | U_d8] (rank 16). v ∈ span(P_union) exactly ⇒ (I − P_union)v = 0 ⇒ no outside
  accumulation; within-span iteration matrix I − C·P_union has eigenvalue 1−C ⇒ stable for
  0 < C < 2; C=1 idempotent (verified numerically above). Same injection vector as the
  current operator (v = Pd d, unchanged). CONFOUND (explicit): removal expands from 8 to 16
  dims — dose/removal-rank changes with it.
- **Restricted injection** Ps·Pd d: no accumulation by the same algebra, but discards ~80%
  of the injection (the donor's outside-Ps directions) — likely neuters the edit; useful as
  a CONTROL (accumulation removed, donor injection weakened), less promising as the main fix.

## Recommendation

If a GPU comparison is authorized next: three conditions at L25..L30 interval and/or single
sites, same 12 questions — (1) current operator (have), (2) shared P_union removal at C=1.5
(+ C=1 for the idempotence point), (3) restricted injection as the accumulation control —
with the rank/removal confound explicit (a matched-removal control can be added later if
the effect survives). Toy evidence supports stability; behavioral transfer is NOT
guaranteed by stability (the fixed point is donor-set components, and prior single-site
results were transient anyway).

## Report corrections applied (same commit family)

"Any site/selector/policy" → tested-settings only; H8 → mechanism question (audited 6/12
exists); no bases-alone-caused-loops conclusion (dose unmatched); 3170-vs-759 labeled
not-dose-comparable (different trajectory lengths); per-cell r2 actual fields (0.84–0.99)
replaced the generic ~0.99.
