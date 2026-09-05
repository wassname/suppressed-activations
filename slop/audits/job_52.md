# Job 52 audit

Target: pueue job 52, dirty tree, command `uv run --project ../do_qwens_reason_in_english python scripts/demo.py --output data/causal_demo.json`; failed after 12 s. Full evidence: [`job_52_full.log`](job_52_full.log), [`job_52_status.json`](job_52_status.json).

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| model and prompts | Qwen3.5-4B loads, then heart/seat trajectories run | weights loaded; no prompt output before failure | unclear | log: `Loading weights: 100%` | prompt and selected-token printout | extraction cannot be checked from this run |
| semantic replacement | record its per-layer perturbation norms | completed silently before random loop | unclear | traceback reaches `for seed in range(32)` at `demo.py:227` | persisted semantic record | exact values were lost when the process exited |
| matched random | preserve residual norm and match semantic perturbation norm | assertion missed by 4.959e-05, relative 4.203e-05 | no | full traceback quotes both errors and tolerance 2e-05 | float32 error scale across layers | control did not run |
| generations | coherent base/replaced/random/removed outputs | not reached | no | no generation rows in the complete 71-line log | all generations | no qualitative result |
| artifact | complete JSON | old job-51 JSON remained on disk | no | job 52 exited before `write_text` | atomic run identity | existing JSON must not be attributed to job 52 |
| resolve condition | target shift outside 32-control distribution | no distribution | unclear | job label | all 32 controls | not judgeable |

## Chronology

The complete cleaned log contains 71 lines. It records the model load, then the first random-control forward fails inside the runtime invariant:

> `Greatest absolute difference: 4.9591064453125e-05 ... (up to 2e-05 allowed)`
>
> `Greatest relative difference: 4.2026971641462296e-05 ... (up to 2e-05 allowed)`

The failed quantity is computed by the closed-form sphere rotation in `suppressed_activation_subspace.py`: the output should have the same norm as `h` and chord distance `distance`. The mismatch is 42 ppm. No result metric or generation was produced, so this job says nothing about the causal hypothesis.

## Hypotheses

### H1 [harness | Almost Certain | 95%]

- Mechanism: the float32 construction accumulates more than the assertion's 20 ppm tolerance.
- Evidence: `Greatest relative difference: 4.2026971641462296e-05`; the error is small and local to `assert_close`.
- Contrary evidence: the same assertion passed on the smaller unit test; realistic residual norms were not covered.
- Discriminating test: rerun the operator over realistic norm/distance ranges with 1e-4 tolerance; a geometric bug would produce materially larger or systematic errors.
- Fix/action: use an error tolerance justified by float32 arithmetic and add a realistic-scale test.
- Interpretability: no; the scientific stages did not run.

### H2 [bug | Unlikely | 20%]

- Mechanism: the chord-distance formula or broadcasting is wrong for `[batch, sequence, d]` tensors.
- Evidence: the invariant itself failed in `matched_random_rotation`.
- Contrary evidence: the mismatch is only 42 ppm and both tensors contain one compared element.
- Discriminating test: compare the formula to a float64 calculation over batched shapes and inspect both norm invariants.
- Fix/action: change the formula only if float64 also misses materially.
- Interpretability: no.

### H3 [method | Remote | 10%]

- Mechanism: the requested semantic chord exceeds a valid spherical displacement at a later layer.
- Evidence: this would invalidate an exact matched control.
- Contrary evidence: the explicit diameter check did not fire; only the final numerical assertion failed.
- Discriminating test: persist `distance / (2 ||h||)` for every layer.
- Fix/action: report the ratio in diagnostics.
- Interpretability: no.

## Decision

1. Resolve-condition verdict: **not judgeable**. The required `32 exact perturbation- and residual-norm matched random controls` were not produced.
2. Prediction check: base, replacement, random, removal, and dose predictions are unresolved because no result rows were printed.
3. Earliest unsupported link: the matched-random operator at realistic float32 scale; a successful invariant check supports it.
4. Validity: `P(result is invalid) ≈ 0.99` where invalid means treating job 52 as causal evidence. Classification: invalid run, not a negative method result.
5. Highest-information clues: 42 ppm mismatch; failure before result printing; old JSON can survive a failed overwrite.
6. Missing metrics: full control distribution; selected tokens; generations; distance-to-diameter ratios.
7. Code change: H1 needs realistic tolerance/test; H2 needs float64 comparison only if the test fails; H3 needs diagnostic ratios.
8. Reinterpretation: none of job 51's earlier numbers can be attributed to the stronger job-52 control.
9. What changes the verdict: a complete rerun with all invariant checks and 32 controls.
10. Recommended sequence: add the realistic-scale unit test, adjust only the numerical tolerance, rerun unchanged science, then audit the full distribution.

Written by PI/gpt-5.4.
