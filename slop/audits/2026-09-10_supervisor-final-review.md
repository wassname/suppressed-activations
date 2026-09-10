# Supervisor evidence review

Written by PI/OpenAI, 2026-09-10. Main commit inspected: `1c658ba`; batchwork: `5c3da8c`.

## Judgment

Accept the user-authorized limited-reliability outcome, not a solved mechanism or broadly reliable intervention. The frozen L20 C1.5 span-correction procedure produced 6/12 primary semantic successes on the declared paired convenience set. The same-strength random control produced 1/12. Same strength is not exact perturbation matching, and one random draw per condition does not estimate a random-control distribution.

Candidate successes by animal: dog 4/6, ant 2/6. By question type: legs 4/4, naming 2/4, properties 0/4. Ant naming lists loop through several animals. Property continuations contain incorrect answers, contradictions or a third animal. Formatting is separate from semantic success: the random live-young dog response begins `0` but explicitly says the dog gives birth to live young, so it is a semantic success and formatting failure.

## Observations checked directly

- Read all twelve candidate full continuations from batchwork `out/2026-09-10_eval-candidate-C1.5-*/result.json`, plus the disputed random-control full continuation and adjudication record.
- Machine-checked every adjudication quote against its saved generation. Earlier spliced quotes failed; the corrected record passes. Counts are derived from per-row judgments, not first-token/presence heuristics.
- Inspected the executed evidence notebook and source. It contains paired development Base/intervention demonstrations, stored rendered input reprs, tokenizer-decoded first32 previews, probability tables, prefill/final-decode readouts, existing full-continuation links, calibration examples, fresh scores, control norms and bounded mechanism findings. The notebook has no error outputs; quote/link/censoring self-check outputs are saved. Readouts remain explicitly unvalidated.
- Earlier pairwise analyses required index-alignment and mathematical-null corrections. Strong donor subsets exist; lack of an all-token mean is not lack of every agreeing pair. The rank-one pair-selector tests did not yield coherent replacement. The synchronized-donor comparison uses a different equation from the recovered candidate and reduced some distortion without target transfer. These results do not exhaust adaptive interventions.
- Read `.local/verify_logs/notebook_smoke.log`, `just_check.log`, and `notebook_check.log`: smoke executes; unit/contract checks and compilation pass; separately modified notebook checker passes.
- Read `/home/code/.local/share/pueue/task_logs/1015.log`: GPU notebook execution wrote the notebook successfully, then the original exact-string checker failed. The job exited1. Subsequent checker tolerances were widened and its separate rerun passed. This is not an unchanged-regression pass. The autograd fix is distinct from those checker changes.

## Evidence locations

- [Executed notebook](../../slop/2026-09-10_span_correction_evidence.ipynb)
- [Adjudications](/workspace/2026/suppressed-activations-batchwork/slop/eval_fresh_adjudications.json)
- [Frozen inputs](/workspace/2026/suppressed-activations-batchwork/slop/eval_fresh_batch.json)
- [Recovery and remaining alternatives](/workspace/2026/suppressed-activations-batchwork/slop/2026-09-10_recovery_decision.md)
- [Final checks](/workspace/2026/suppressed-activations/.local/verify_logs/just_check.log)

The notebook currently depends on absolute paths into the batchwork checkout. Verification logs are machine-local. No publication approval is implied; unrelated existing README changes were not edited or committed by this review.
