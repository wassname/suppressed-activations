# Same-question vector/procedure map at L20: why the reference transfers and the replacements do not

2026-09-12, PI[claude]. PROVENANCE (validated after a first draft had two defects):
- δ is the HISTORICAL tensor the successful runs actually applied — loaded from the sweep's
  own `out/2026-09-10_eval-candidate-C1.5-legs-L1-{dog,ant}/template_vectors.pt` (saved
  sweep-side), not reconstructed.
- P_ref is rebuilt from the PINNED template-bank suffixes (revision 851bf6e8; the first
  extraction 1144 was UNPINNED due to a model-name comparison bug — fixed and re-extracted
  as task 1145; the dev bank 1127 was pinned correctly) using the RUNNER's own
  `attenuation_basis` function (imported, not duplicated).
- The SWEEP DOES NORM-MATCH: the sweep projects the delta onto the shared basis AND
  renormalizes to the raw delta norm upstream (sweep line ~2376), BEFORE the
  span_corrected_delta hook (which doesn't read match_component_norm). The earlier
  "hook doesn't read the flag therefore no norm matching" inference (mine and the first
  review's) was incomplete — hook vs construction distinguished; correction recorded in the
  ARJ. So δ′ = P_ref δ rescaled to ‖δ‖ is the actual applied reference delta.
- v = Pd d (donor top8 temporal-union projection of the same-question donor residual at
  L20, bank criterion 23/25/32, pinned dev bank); g = donor − source residual difference
  at L20. Script: `scripts/vector_map.py` → `vector_map.json`.

## Headline (means over 12 cells × 3 end-aligned positions)

| quantity | dog | ant |
|---|---:|---:|
| ‖δ raw‖ = ‖δ′‖ (rescaled; historical tensor) | 6.81 | 5.70 |
| ‖v‖ | 1.92 | 1.77 |
| ‖g‖ (donor−source difference) | 5.87 | 4.75 |
| ‖h20‖ | 15.92 | 15.92 |
| **cos(δ′, v)** mean (per-row min/med/max) | **+0.008** (−0.02/+0.01/+0.04) | **+0.010** (−0.02/+0.01/+0.04) |
| cos(δ′, g) mean (range) | +0.182 (−0.04…+0.46) | +0.149 (−0.03…+0.36) |
| cos(v, g) mean | +0.041 | +0.015 |

**The successful reference delta and the failed replacement vector are effectively
ORTHOGONAL**: mean cos +0.008/+0.010, per-row |cos| ≤ 0.04 (36 rows; negative in 6/18
dog and 3/18 ant rows — the mean does not hide large mixed signs; the distribution is
tightly around zero). Both vectors are also near-orthogonal to the plain donor−source
difference; the template-mean delta is NOT the donor−source direction. Norm differences
remain (δ′ 3.5× v) and are NOT ruled out as contributors by orthogonality.

## Fraction of each vector inside each span (norm fraction / energy fraction)

| span | δ′ norm/energy | v norm/energy |
|---|---|---|
| source top8 | — / — | 0.60 / 0.39 |
| donor top8 | — / — | 1.000 / 1.000 |
| joint [top8s] | — / — | 1.000 / 1.000 |
| **ref span (rank 4)** | **1.000 / 1.000** | 0.04 / 0.002 |

SPAN-LEVEL subspace relation (principal-angle cosines, legs cells; vector-level fractions
above): span(P_ref) vs span(source top8): max principal cosine 0.15; vs span(donor top8):
max 0.14 — near-orthogonal at the subspace level, with small real overlaps (not asserted
zero). Full angle lists in `vector_map.json`. The two interventions act in near-disjoint
subspaces: the replacements write into the suppression-score top8 temporal-union spans;
the reference delta writes into the rank-4 template-contrast attenuation span.

## What each vector WRITES (top gain-weighted readout tokens)

- TOKEN READOUTS ONLY (a vocabulary-level statistic; the semantic story below is a
  HYPOTHESIS, not established): δ′ top readouts `' Maria'`, `' hom'`, `'灵'`, `' sul'`,
  `' dans'` — name/label-like tokens across languages (the templates are all
  "labeled '{animal}'" phrasings). v top readouts `'ANDROID'`, `' leash'`, `'狗粮'`,
  `'生态保护'`, `'fetch'`, `'สุนัข'` — heterogeneous multilingual tokens; the same token
  families that appeared as loop content in the degenerate interval runs.

## Procedure differences (explicit)

- Reference δ: TEMPLATE AVERAGING — mean over 8 generic "labeled '{animal}'" templates,
  DIFFERENT texts from the same-question prompts; the averaging may cancel question-specific
  coordinates (untested here); the contrast-energy criterion (rise at L20, fall at L32,
  fit split) selects the attenuation subspace.
- Replacement v: SAME-QUESTION donor residual, projected on the per-token suppression-score
  spans; no averaging over templates; no contrast-energy criterion on the injection
  direction.

## Reading (labeled inference; norm differences NOT ruled out by orthogonality)

The measured facts: the two injection directions are near-orthogonal at both the vector
level (|cos| ≤ 0.04) and the span level (principal cosines ≤ 0.15); δ′ is 3.5× larger
relative to ‖h20‖; δ′ sits fully in its own removal span (stable operator per the algebra);
v sits fully in the donor top8. HYPOTHESIS (not established): the reference's advantage is
direction selection — a coherent low-rank label/identity direction in its own removal span
— while the replacements inject projections onto debris-dominated vocabulary spans;
template averaging may cancel question-specific coordinates (untested). The norm difference
co-varies and is not separated. Bounded 2×2 (supervisor-approved shape, after provenance
validation): injection {δ_ref, v} × removal {P_ref, Ps} at the SAME L20 single site,
permitting the exact successful-baseline cell.

## Scope

L20 only; 12 dev pairs; the reference reconstruction reproduces the sweep's code path
(attenuation_basis verbatim; fit split; rescale) but was run on CPU from the template bank —
exact-tensor identity with the historical GPU runs is not bit-verified.

## Recovered historical ablations (injection-only / removal-only; actual configs+results)

From the migrated main-repo artifacts (`/workspace/2026/suppressed-activations/out/
2026-09-07_190240_svd-ant-parts/result.json`, job 500 — the journal's linked source for
"Token-persistent SVD changes digits mainly through source removal"; token-persistent SVD
era, L24, different delta construction):

| condition | swap | first token |
|---|---:|---|
| svd_parts_difference (removal + injection) | +5.375 | `6` (donor digit) |
| **svd_parts_source_remove (REMOVAL ONLY)** | **+6.125** | `6` |
| **svd_parts_target_add (INJECTION ONLY)** | **+0.000** | `8` (unchanged) |

Historical reading (journal, quoted): "source removal probably explains the apparent ant
transfer at the selected setting, because removal alone is stronger and donor addition
alone has no log-odds effect."

## Synthesis with the current map (both eras' evidence)

- Historical era (token-persistent donor delta): removal-only carried the digit change;
  injection-only did nothing.
- Current era (template-label delta): injection direction carries naming/identity transfer
  (B: δ_ref′ + Ps removal = 3/12 full passes); removal span barely matters for it.
- Common structure across eras: the EFFECTIVE component is the one aligned with the
  removal span's construction (historical: the removed source component; current: the
  δ-ref label direction in its own span). Injection effectiveness is direction-dependent.

## Proposed next smallest distinguishing test (NOT queued)

At the CURRENT operating point (L20, C1.5, same 12 questions): the ONE ablation never run
in the template era — **δ_ref′ injection WITHOUT removal** (h + C·δ_ref′, the runner's
existing fixed_delta op; the sweep computes δ_ref′ already) vs **removal WITHOUT
injection** (remove op with source_basis = P_ref) vs A (both). 24–36 cells. This separates
whether δ_ref′ alone transfers (injection-sufficient) or needs the matched removal
(synergy), directly on the successful baseline — the smallest test that discriminates the
two readings of the 2×2.
