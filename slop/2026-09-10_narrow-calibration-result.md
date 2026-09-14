# Task 938 — final calibration sweep (two-site, narrow)

Supervisor-directed last calibration: prop-dog / prop-ant x answer-site C in {0.2, 0.25},
L20 identity fixed at C=1.5, L26 raw d_act patch, everything else at verified defaults.
Results: `out/2026-09-10_twosite-narrow-{prop-dog,prop-ant}-C{0.2,0.25}/result.json`.
Commit 2bf8a16 (code + spec). Pueue task 938 Success, 02:14:35-02:15:42.

## Results

| cell | first token | top-3 p | prose answer | r2 | verdict |
|---|---|---|---|---|---|
| prop-dog C=0.2 | `'1'` | ` No` .2157 / `1` .2157 / ` Yes` .1903 | "No, … is not a mammal; it is a domesticated dog" | 0.068 | fail — stuck at source |
| prop-dog C=0.25 | `'1'` | ` Yes` .2151 / `1` .2151 / ` No` .1898 | "No, … is not a mammal" (Yes tied on top but prose says No) | 0.070 | fail — contradictory |
| prop-ant C=0.2 | `' Yes'` | ` Yes` .3035 / `1` .2364 | coherent ant identity prose, 88 tok | 0.070 | **pass** (all 3 criteria) |
| prop-ant C=0.25 | `' Yes'` | ` Yes` .2949 / `1` .2602 | coherent ant prose to EOS, 66 tok | 0.047 | **pass** (all 3 criteria) |

Success criteria (from AGENTS.md): ` Yes`/` No` first token, r2 < 0.2, coherent target-identity prose to EOS.

## Decision

No single C gives both animals a pass on all three criteria → **freeze branch** of the decision rule.

- prop-ant passes across the whole swept range 0.05-0.25 (cells 937 C=0.05/0.15 + 938 C=0.2/0.25,
  4/4 meet all 3 criteria: ` Yes` first + coherent ant prose to EOS + r2 < 0.2).
- prop-dog never passes: at low C the answer stays at source (` No`, self-contradictory with dog
  prose); at C>=0.25 the top-2 becomes a ` Yes`/`1` tie but the generated prose still answers "No".
  The earlier C=0.3/0.6 cells (937) had correct Yes+dog content behind a `1` numeral artifact —
  so prop-dog moves toward Yes in probability mass but never commits to Yes-first coherent prose
  at any tested C in {0.05,0.1?,0.15,0.2,0.25,0.3,0.6,1.5}.

## r2 -1 placeholder (supervisor question)

Checked: no -1 placeholder exists in any 937/938 result.json. `repeated_bigram_fraction` is
populated in all cells (values above). The only -1 values in the raw JSON are legitimate seed
sentinels (`random_delta_seed`, `bee_correction_seed`). Likely the supervisor saw those.
Separate real quirk: `bare_answer_mass` = p(4)+p(8) is a legs/arithmetic metric and is
uninformative (~0.001-0.005) for Yes/No property cells, yet is rendered under a "p(Yes)+p(No)"
header in condition run.md. Column-label issue only, not a computation bug.

## Frozen rule for deliverable phase

Two-site span-correction: L20 `h' = h + 1.5(Δ − UUᵀh)` + L26 additive d_act.
- Identity/naming + limb-count: C=1.5 (both animals, established 929/936).
- Property answer: prop-ant C=0.15 (mid of passing range, largest ` Yes` margin); prop-dog = partial,
  documented as non-transferring (answer-stuck-at-source below C=0.25, numeral/contradiction above).

Next: reserved-string evaluation (spinneret naming, limb-count, live-birth + matched-random
controls) with the frozen rule; then notebook finalization with property labelled
partial (ant transfers, dog does not).

-- PI[Kimi K3]
