# One context-projected reflection attempt

— PI/OpenAI

Contract: `slop/reviews/2026-09-30_context-invariant-coordinate-decision.md`. Existing goals remain open. The prior embedding-subtraction candidate failed2/8 and will not be run causally.

## Frozen change

Use the eight generic pair means from2627 as development data. Project the OLD donor direction off their top7 centered right-singular vectors, normalize the retained direction, and center on the mean pair mean. No embedding subtraction, current-question preparation, alternate rank, dose fit or position selection. All numerical work during fitting is float64; save operational center/direction in float32, then validate and edit with those saved parameters. Runtime reflection is unchanged apart from its loaded coordinate.

Numerical abort conditions are in `nuisance_coordinate`: require s1>0, s7>eps64*max(8,d)*s1 and retained norm>eps64*max(8,d). No fallback rank. Pinned training-state and coordinate hashes are in `data/donor_coordinate_validation_v2.json`.

Observed fit check: retained norm0.983891845; s7=1.97888094 versus rank tolerance6.01e-12. Training8/8 brackets and maximum training midpoint margin1.19e-7 are NOT held-out evidence: midpoint invariance is constructed. Logs: `slop/audits/2026-09-30_nuisance-coordinate-check.log`.

## Budget and execution

One queued default-lane job, no reordering. Exact shape of the outer command:

```sh
env PYTHONPATH=/dev/shm/suppressed-import-7ac02bf HF_HUB_OFFLINE=1 \
 timeout --signal=TERM --kill-after=15s 300 uv run --no-sync --offline python -u \
 .local/queued/context_projection_<commit>.py \
 .local/queued/08_projection_<commit>.py \
 .local/queued/donor_coordinate_v2_<commit>.json
```

All three inputs are copied from the final reviewed commit. The timeout covers imports, fitting, validation and both causal conditions as one process; TERM at300s, forced kill15s later if necessary. Timeout/incomplete artifacts do not relax the gate.

First:16 new generic prefills, exact contexts in v2 JSON, no generation. New context classifier must satisfy dog<0<spider for all8 pairs. Save every margin, raw state, token/embedding and source. Earlier positions remain diagnostic. On any failure, launcher records `passed:false` and performs no causal generations for this candidate.

Only on pass: both existing reverse leg and skeleton questions, block15/residual16, final-one-token prefill, every cached decode, unit conditional reflection. Five modes per property: Base, old raw reflection, context-projected reflection, natural addition, adaptive own-state random. Maximum320 generated tokens total,32 per mode/property. Existing post-condition clean-target probes do not control editing. Random is prefill norm-matched, not trajectory-dose-matched after divergence.

## Predictions / alternatives

| option | distinguishing observation | action |
|---|---|---|
| remove generic context variation | new pairs separate; same learned coordinate applies during causal prefill/decode | this single candidate |
| a new scalar cutoff on the old axis | cannot separate recorded2627 states: maxdog>minspider | rejected without fitting |
| different positions or question-matched donors | unvalidated selection rule or preparation leakage risk | deferred |

Context invariance generalises: plausible (~50%), predicts8/8 NEW brackets, not merely training invariance. Overfit to observed context/referent wording: plausible (~50%), predicts at least one new-pair sign/order failure. Semantic information is removed or insufficient: plausible (~60%), predicts held-out separation but no coherent same-method8/outside transfer. Implementation error: remote (~5%), addressed by tests/review, not assumed absent. Unknown causes remain (~10%); hypotheses overlap.

SHOULD: frozen raw control retains its original coordinate; candidate/random use the projected coordinate, including cached decoding. Requested fold margins equal abs(before), with applied BF16 deviations logged. Base first outputs should reproduce prior baselines. TODO validate: new context separation and coherent causal transfer.

The two properties have different initial difficulty: archived reverse Base gives p8=.00720431 versus p4=.943579 (4.875 nats pairwise disadvantage); body outside=.225063 versus inside=.255030 (about.125 nats disadvantage). A weak body change alone is particularly poor evidence of identity replacement. Zero-shift Base/raw and one random direction are controls, not a distributional chance estimate.8/8 validation is a predeclared engineering requirement, not a calibrated significance threshold.

## Execution checks

CPU algebra passes seeds0/1: span reconstruction, orthogonality, unit norm, rank-deficient/vanishing-direction rejection. Tiny real hybrid-Qwen smoke passes seeds0/1: genuine generic preparation, fit, NEW16-prefill validation, I/O and float64 replay; then separately exercises the actual production mode-selection and hook for5 modes×4 generated tokens, cached coverage, fold assertions, matched random prefill norm and cleanup. The tiny gates were false and not forced; hook tests are separate component tests, not proof of a passing end-to-end scientific gate. Full-size BF16 and the full main dispatcher are not covered by this CPU smoke.

The first smoke failed because its AST extraction namespace omitted the `Tensor` annotation import from `scripts/demo.py`. The test namespace was fixed; main inference code was not changed for that error. First failure and corrected logs are archived. Reviewe95ab13b/e8ee9d44 found no blocking dataflow bug conditional on the supplied outer timeout. It explicitly did not certify semantic success or full-size BF16 execution; report: `slop/reviews/2026-09-30_nuisance-projection-implementation-review.md`.

Three ways a positive result could mislead: constructed training invariance (new contexts gate), lexical or length differences (record exact strings and both referent styles; no claim of pure semantic isolation), and changed attributes without concept replacement (both properties, exact continuations/readouts, controls). No optimizer, LR, training loss or gradients apply. Successful execution or algebra alone cannot complete either goal.
