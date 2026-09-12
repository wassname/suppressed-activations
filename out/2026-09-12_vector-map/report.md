# Same-question vector/procedure map at L20: why the reference transfers and the replacements do not

2026-09-12, PI[claude]. CPU from saved artifacts: template corpus (task 1144,
`scripts/template_bank.py` — 8 CONCEPT_TEMPLATES × spider/dog/ant, sweep-identical
rendering), dev-bank residuals, and the runner's constructions rebuilt verbatim
(`scripts/vector_map.py` → `vector_map.json`). The reference tensors are reconstructed with
the sweep's exact operations: contrasts = donor-template − source-template suffix residual
(per template); P_ref = attenuation_basis(peak=L20 contrasts, output=L32 contrasts, rank 4)
on the sweep's fit split (first 4 templates); δ = template-mean difference at L20;
**applied δ′ = P_ref δ rescaled to ‖δ‖** (the sweep's match_component_norm renormalization);
v = Pd d (donor top8 temporal-union projection of the SAME-question donor residual at L20,
bank criterion 23/25/32); g = donor − source residual difference at L20.

## Headline (means over 12 cells × 3 end-aligned positions)

| quantity | dog | ant |
|---|---:|---:|
| ‖δ raw‖ = ‖δ′‖ (rescaled) | 5.47 | 4.13 |
| ‖v‖ | 1.92 | 1.77 |
| ‖g‖ (donor−source difference) | 5.87 | 4.75 |
| ‖h20‖ | 15.92 | 15.92 |
| **cos(δ′, v)** | **+0.005** | **+0.005** |
| cos(δ′, g) | +0.186 | +0.145 |
| cos(v, g) | +0.041 | +0.015 |

**The successful reference delta and the failed replacement vector are ORTHOGONAL
(cos ≈ 0.005).** Both are also nearly orthogonal to the plain donor−source residual
difference — the template-mean delta is NOT the donor−source direction.

## Fraction of each vector inside each span (norm fraction / energy fraction)

| span | δ′ norm/energy | v norm/energy |
|---|---|---|
| source top8 | 0.12 / 0.015 | 0.60 / 0.39 |
| donor top8 | 0.11 / 0.012 | 1.000 / 1.000 |
| joint [top8s] | 0.17 / 0.030 | 1.000 / 1.000 |
| **ref span (rank 4)** | **1.000 / 1.000** | 0.04 / 0.002 |

The two interventions act in (near-)DISJOINT subspaces: the replacements write into the
suppression-score top8 temporal-union spans; the reference delta writes into the rank-4
template-contrast attenuation span, orthogonal to them.

## What each vector WRITES (top gain-weighted readout tokens)

- δ′: `' Maria'`, `' hom'`, `'灵'`, `' sul'`, `' dans'` — a coherent multilingual
  NAME/LABEL direction (the templates are all "labeled '{animal}'" phrasings). The
  reference's transferable content is a label/naming direction, not animal semantics.
- v: `'ANDROID'`, `' leash'`, `'狗粮'` (dog food), `'生态保护'`, `'fetch'`, `'สุนัข'`
  (Thai: dog) — scattered multilingual token debris; the same tokens that surfaced as loop
  content in the degenerate interval runs (chien/狗粮). The suppression-score top8 spans'
  donor projections are debris-dominated.

## Procedure differences (explicit)

- Reference δ: TEMPLATE AVERAGING — mean over 8 generic "labeled '{animal}'" templates,
  DIFFERENT texts from the same-question prompts; the averaging may cancel question-specific
  coordinates (untested here); the contrast-energy criterion (rise at L20, fall at L32,
  fit split) selects the attenuation subspace.
- Replacement v: SAME-QUESTION donor residual, projected on the per-token suppression-score
  spans; no averaging over templates; no contrast-energy criterion on the injection
  direction.

## Reading (labeled inference)

On this evidence, the reference's advantage is that its injection direction is a coherent
low-rank label/identity direction whose energy sits in its own removal span (stable
operator), while the tested replacements inject projections of the donor state onto
debris-dominated vocabulary spans that are orthogonal to the label direction. This is a
direction-selection difference, not a magnitude difference (δ′ and v have comparable
norms relative to ‖h20‖: 0.34 vs 0.12 — v is smaller but the orthogonality, not the 2.8×
norm ratio, is the sharp separation). Hypotheses this suggests for a future 2×2: replace
the injection direction (template-label delta) while varying the removal span (Ps vs
P_ref-like) — the compact comparison the supervisor asked to design only after this map.

## Scope

L20 only; 12 dev pairs; the reference reconstruction reproduces the sweep's code path
(attenuation_basis verbatim; fit split; rescale) but was run on CPU from the template bank —
exact-tensor identity with the historical GPU runs is not bit-verified.
