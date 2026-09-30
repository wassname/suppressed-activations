# One active-coefficient gradient-pursuit readout test

Parent decision before production results, after advisor71cbb8ae. — PI/OpenAI

Purpose: test whether revising earlier coefficients reveals hidden concepts that fixed-coefficient matching pursuit misses. Better reconstruction alone does not count as success. Both research goals remain open.

Reference and exact solver: `slop/reviews/2026-10-01_after-pursuit-next-test.md`. The paper names nonnegative gradient pursuit; the inspected public lens implementation does not provide it. This is the specified feasible-gradient algorithm in that proposal, not a faithful-reproduction claim. Matching-pursuit2657 remains a completed negative, not an invalid run.

## Frozen experiment

- Same8 reused v4 development cases and2637 cached states; no transformer forward calls or new generations. v5 remains unused.
- J24 sole primary; plain24/plain27 receive the identical solver. Same full-vocabulary normalized dictionaries, precision, post-decomposition prompt/output masks and32-iteration maximum.
- At most one new positive-correlation atom per iteration, lowest-ID ties, followed by one feasible gradient update over all retained support. Earlier coefficients may decrease. Support retains zero-coefficient atoms. No NNLS convergence loop or OMP full least-squares fit.
- Float32 coefficients/atoms and float64 norms/line-search scalars. Set boundary-hitting coefficients to zero; permit only rounding-sized corrections with the specified32-epsilon bounds. Abort on nonfinite values, invalid line search or material energy increase. Stop on zero feasible gradient or unchanged coefficients.
- Positive accumulated coefficients divided by original state norm determine output. No zero-valued fillers, language rules or label access in decomposition.
- Preserve all288 old rows and all8 cache traces exactly. Keep existing native-cardinality matching pursuit, full32 dot baselines and half-erasure incumbent as separate controls. New raw/unit-dot comparisons use the gradient-pursuit returned cardinality. Matching pursuit may additionally be capped at that budget, with its actual returned count stated; never pad it or falsely call a shorter list equal-sized.
- Keep both diagnostic positions and unmasked inventories. Save coefficient revisions, support, step sizes, numerical tolerances, residuals and ranking scores. Labels remain evaluation-only.

## Advancement and stopping

Require positive net paired alias joint gain versus own equal-cardinality unit-dot control, followed by positive net semantic gain under symmetric review. Also require at least one reviewed new recovery relative to the original native matching-pursuit output, absent from both unmasked gradient-pursuit diagnostic inventories. Counted passes must exclude definite input/said equivalents. Report gains and losses, incomplete aliases and wrong baselines; do not rescore2657 or choose a plain control as the winner.

Residual improvement, coefficient revisions or an improved AUROC alone fail. Failure retires this exact configuration without layer/k/mask/precision tuning. A pass permits considering unseen evaluation, not declaring either goal complete. The earlier7/16 reviewed v3 result remains an honest partial result; no7/8 or all-baseline-dominance requirement is introduced.

## Cost, alternatives and checks

One default-queue local GPU job,300s TERM plus15s kill grace, returning to the usual initial bound. Retain launcher timing/stack diagnostics; no queue reordering. Previous complete cached experiment required47.657s, including24.2s imports, but intermittent startup remains a risk. No scientific change will be made to compensate for startup failures.

Prediction: coefficient updates can reduce reconstruction error without semantic improvement (rough70% chance); semantic advancement is less likely (rough15%). These are planning bets, not calibrated rates. Correlated January/Months allocations motivate the experiment but do not prove its mechanism. Generic associations and multilingual leakage remain the strongest alternative explanation.

Before submission: independent NumPy coefficient-update comparison at seeds0/1; a correlated two-atom example requiring an earlier coefficient to decrease; nonnegative/boundary/tie/zero/nonfinite checks; unchanged default matching-pursuit/scoring parity; actual tiny production integration and hook/cache checks. Save all failures. No synthetic success is a scientific result.

## Implementation evidence before submission

`08_jlens_one_pass.py` now accepts `--matching-pursuit --gradient-pursuit`. It retains288 old production rows and adds96 candidate/comparison rows, for384 total. Gradient records/tensors and both diagnostics use separate `gradient_pursuit_*` artifacts. Legacy erasure runs only as a separate incumbent/control; it is never applied to the solver's state.

Final CPU chain passed39s, seeds0/1, at sourceSHA5e31845bedb7df4a0fc9a924845ac1bb075f691142ba6cc63a95a7769653cb40. Independent float64 reference, decreasing coefficients, an exact nonnegative-boundary case, masks, ties and default matching-pursuit/scorer regression pass. Actual tiny32-layer BF16 Qwen capture/replay gives96 rows per seed and72 native matching-pursuit/baseline rows exactly unchanged; parameters, cached IDs/states and forward rejection checked. Correlated two-atom residual: GP0.000416 versus MP0.336, synthetic numerical evidence only.

Preserved failures: first helper fixture wrongly assumed the first-selected atom's support index; fixed the fixture, not the solver. First integrated main had a report-block IndentationError, also found by fresh reviewer753e5eda. Fixed both indent levels; whole-source parse and fresh full-main smoke pass as requested by that review. The reviewer found no other concrete defect, but did not inspect the later launcher or certify GPU behavior. Same-family review.

Launcher e2ddb1ba019b661469a82f413853bef9591b628c8ab789a74a832b0639c41c16 pins source/data/helpers/cache, requires384 unique rows and288 exact prior rows, validates cardinality/capped-MP controls and computes prospective comparisons. Semantic advancement remains false pending review. Parent AST/config/hash preflight passed; complete4B launcher path is unexecuted. Current logs are `gradient-pursuit-check.log`, `gradient-default-regression.log`, `gradient-main-smoke.log`; failures and pre-integration logs are retained. Ready for the one bounded GPU submission.

## Subsequent outcome, not a change to the criteria

Job2668 completed56.721s with384 rows/288 old rows exact. GP J3/8 versus matched unit-dot4/8, no paired gains, December loss, no new recovery over native MP. Coefficient revision and lower reconstruction error were observed; the prospective advancement criterion nevertheless fails. Independent selected-support checks and same-family result review complete. Exact setting retired, v5 not run. Full audit: `slop/audits/2026-10-01_job2668.md`. Both goals remain open. -- PI/OpenAI
