# Norm-vs-direction factorial at fixed L20/P_ref (task 1152, 60 cells)

2026-09-12, PI[claude]. Run: pueue 1152, `slop/common_basis_norm2x2_batch.json`, one model
load, 571 s; protocol `slop/norm_factorial_protocol.md`. Fixed: L20 single site, P_ref
removal (rank 4), C=1.5, frozen donor, last-3 + all-decode, 12 dev questions. Varied:
injection direction {δ_ref′, v} × injection norm {own, cross-rescaled per-position}.
Rescaling asserted per position (direction cos = 1.0 exact, target norm exact; saved per
cell). Raw: `out/2026-09-12_cb-norm2x2/{condition}-{cell}/result.json`.

## Factorial (swap means over 12; splits 4 cells)

| direction \ norm | ‖v‖ ≈ 1.9/1.8 (low) | ‖δ_ref′‖ ≈ 6.8/5.7 (high) |
|---|---:|---:|
| **δ_ref′ direction** | +1.01 | **+10.01** (A replay) |
| **v direction** | +0.43 (C replay) | **+3.54** |

Norm-target checks: max rel err 0.0, min cos 1.0 (both scaled arms). C0 exact identity.

## Semantic adjudication (full continuations read)

- δ_ref′ at v-norm: clean spider everywhere (name/legs/prop; r2 ≤ 0.01) — NO transfer;
  the +1.01 swap never entered behavior.
- v at δ-norm: DEGRADED or partial — name-N1-dog `蜘蛛 (Spider)…The spider is an arachin
  that lives in the water. It fetches the water…` (incoherent, early EOS 37t); legs-L1-dog
  `6.` (wrong digit) + `arthrop虫` (broken token); ONE partial identity bleed: name-N2-dog
  `1. A dog is a loyal and intelligent animal…` (the description moved to dog) — not a
  coherent answer to the naming question.

## Verdict (observed outcomes at the TESTED two norm levels; durable per-row table:
`per_row_adjudications.json` — answer/identity/coherence/format judged separately)

- δ direction: 0/12 semantic passes at v-norm → 6/12 at own norm (A: legs 4/4 digits +
  naming-dog 2/2).
- v direction: 0/12 at own norm → **1/12 at δ-norm** (name-N2-dog: a numbered DOG
  description with persistent dog identity, coherent, format compliant — a SEMANTIC PASS;
  the numbered description is an answer, per the same rubric as the earlier leading-0
  correction). Other v rows degrade (loops r2 0.87/0.93, incoherent water-fetching spider,
  broken `arthrop虫`).
- Observed: magnitude improved at least one donor-vector case to a semantic pass; the
  δ direction has the larger tested-level outcome counts. No general necessity claim and
  no log-odds-ratio-as-direction-quality measure: the +10.01-vs-+3.54 swap gap is an
  aggregate log-odds observation, not a validated quality measure.

## 1149 B per-row adjudications (pending item; saved `B_per_row_verdicts.json`)

B (δ_ref′ + Ps removal): **3/12 FULL PASS** — legs-L2-dog (digit 4 CORRECT + coherent dog
identity — a pass, not collapsible), name-N1-dog, name-N2-dog. legs-L1/L2-ant: digit wrong
(3, not 6) but ANT IDENTITY moves coherently ("The red ant…", "the ant… lives in
colonies") — identity-without-digit. name-N1-ant: honey bee (wrong insect). A: 6/12
(legs digits 4/4 + naming-dog 2/2; ant-naming loops). The removal span interacts with
WHICH content survives: A (P_ref removal) transfers digits; B (Ps removal) transfers
naming/leg identity without digits — hypothesis-grade, one comparison.

## Standing (tested settings)

Tested constructions with coherent-transfer outcomes: the reference (δ_ref′ + P_ref
removal; audited 6/12 fresh) and B (δ_ref′ + Ps removal; 3/12 dev). The v direction
produced 1/12 at high norm in the tested settings. No claim that other constructions
cannot transfer — only these were tested at these two norm levels.
