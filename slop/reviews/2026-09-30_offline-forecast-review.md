## Concrete bugs / implementation mismatches

- **“Said output” scoring uses intended answers, not actual outputs.** `said`/`said_alias_ids` derive from hard-coded `answers`; `said_text` is merely logged. The acknowledged gold-versus-euro currency example can therefore pass while retaining the actually emitted answer. This is an evaluation error relative to excluding said outputs, not label leakage into ranking.
- **Validation is not final-position-only.** `fit_forecast` concatenates every position of all four held-out records for argmax agreement and MSE. These are token-weighted, teacher-forced statistics, not four prompt-final predictions. They may be useful, but do not directly validate the final-position deployment.
- **Reported ranks can remain misleading.** Nonpositive differences become `-inf`; excluded targets can consequently receive tied ranks or appear as `best_hidden_token`. Actual finite-top32 membership correctly avoids this problem for pass/fail.

**Mathematical checks:** `fit_affine` correctly solves centered ridge regression toward the identity:
\(T=I+(X_c^\top X_c+\lambda I)^{-1}X_c^\top(Y_c-X_c)\),
with the appropriate intercept. `res[block+1]` matches block outputs; `res[32]` is the raw final residual through `trajectory`. The target is RMS-normalized final residual, not its original magnitude. There is no evident transpose error.

The coordinate swap correctly exchanges pseudoinverse coordinates for full-column-rank directions, preserving the orthogonal complement. These are coordinates in normalized vocabulary-derived directions—not necessarily independent semantic features or exact normalized-lens logits. The later observer only computes readouts and returns `None`; it does not replace activations or feed back into the earlier edit.

## Three main interpretation risks

1. **Argmax accuracy does not validate probability subtraction.** Ranking \(p_J-p_F\) depends on distributional calibration, while agreement ignores confidence. Improved agreement or residual MSE can coexist with worse output suppression. RMS normalization plus bf16 casting also means forecast decoding is not numerically identical to decoding raw final residuals.

2. **Generic calibration is not evidence of task robustness.** Four records provide few independent validation units despite many token observations; adjacent records may share articles. The code checks only record count, not deduplication, article separation, or task overlap. No evaluation labels enter the fit or ranking, but prior answer-correct selection and development prompts bias the eight-case evaluation. Checkpoint/model-revision compatibility is also not established by shape checks.

3. **Positive excess is not guaranteed hiddenness or exclusion.** A said token survives whenever J assigns it more probability than the forecast. Differences can reflect confidence, lexical associations, or forecast error rather than suppressed concepts. Full input trajectories and separate generations are executed, although ranking itself uses only residual24: this supports “no input-specific preparation,” not a literal truncated one-pass implementation.

**Cheapest distinguishing test:** Reuse already-computed actual final logits as an evaluation-only oracle baseline, comparing J-minus-final with J-minus-forecast and J-minus-plain. Score the genuinely generated outputs. If even the oracle retains them, the contrastive rule—not merely forecast quality—is inadequate. If only the forecast fails, investigate prediction/calibration.