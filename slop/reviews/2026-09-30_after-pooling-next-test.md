## Inherited decisions
2637 failed: pooled J3/8 versus last4/8; pooled plain274/8 versus last5/8. Retire pooling without window/layer/k rescue. Earlier hidden-label peaks sometimes precede identifying clues, so membership alone cannot establish extraction. Both goals remain open.

The supervisor approved **one polar-transform experiment with a cached early-prefix control**.

## Diagnosis
Removing J’s anisotropic gains is a distinct representation hypothesis, not an established correction. It may reduce dominant transmitted features, but may instead elevate poorly estimated small-singular-value directions.

A sparse-clamp intervention remains possible, but currently requires additional algorithmic choices. The polar test is narrower and executable without new model inference. It is **not a published-reference reproduction**.

## Drift / contradiction check
Preserve final-position readout, existing probability excess, masks and k32. Do not combine polar transport with pooling, erasure, KL weighting, or a spectral sweep. Orthogonality establishes geometry—not semantics.

## Recommendation: approved contract

**Budget/data:** one local cached replay,300-second TERM deadline plus15-second kill grace. Use2637’s `prefill_positions.pt`, saved spans, final states and generations. **Zero transformer forwards, generations, or calibration**; retain the forward-rejection guard.

**Transform:** for the existing residual24 Jacobian, compute float64

\[
J=U\Sigma V^\top,\qquad Q=UV^\top.
\]

Require finite values, \(\sigma_{\max}>0\), and
\[
\sigma_{\min}>\epsilon_{64}d\,\sigma_{\max}.
\]
Otherwise abort: no rank truncation or arbitrary null-space extension. Repeated positive singular values do not make the full-rank polar factor ambiguous. Apply no determinant correction. Save J/Q identities, singular values, reconstruction and orthogonality errors, and casting details.

Transport the last-position residual as **\(hQ^\top\)**, then use the unchanged actual final norm/head. Normalize vocabulary logits before masking:

\[
s_Q(t)=p_Q(t)-p_{F,\mathrm{last}}(t).
\]

Only positive, unmasked scores qualify; keep the existing prompt/greedy1 masks and k32.

**Controls:** original J, plain24 and plain27 with identical probability-excess scoring; Q without subtraction; Q with cyclic-mismatched final distributions, retaining current-case masks; and Q at the fixed early-prefix position.

**Early-prefix position:** the **third fully-contained question token**, determined from2637’s saved offsets. Assert the first three decoded pieces are `Fact`, `:`, and ` The`/` In`. Use every case’s own final-LAST comparator and unchanged masks. This structural control does **not** isolate the identifying clue or exclude later topic priors.

**Evidence:** preserve existing last-position scores/generations. Record top32 and score components, all frozen hidden/said alias scores, final-versus-early hidden maxima, and rankings against the other seven v4 hidden-label sets. Those comparison labels are frozen evaluation-only negatives—not ranking inputs or necessarily topic-matched controls. Report raw signed excess alongside positive-score eligibility.

**Decision:** Q is the sole candidate; no representation reselection. Promising requires:
- ≥7/8 alias-checked joint passes;
- strictly exceeding original J, both equally scored plains, and Q’s mismatched control;
- every counted hit’s maximum eligible hidden score strictly exceeding its early-prefix maximum.

Keep incumbent half-plain27’s6/8 visible. Unsubtracted parity prevents attributing gains to subtraction. Retain all eight cases, unchanged alias scoring and AUROC denominators.

Before new examples, require symmetric blinded semantic review with no definite input/said leaks among counted passes. Then freeze the method for **output-matched clue substitutions**. Failure ends this candidate—no spectral/window/layer rescue.

## Risks
Early-prefix controls miss later topic priors; final-token subtraction misses later speech. Eight repeatedly inspected examples remain development, not generalisation evidence.

## Need from main agent
None; contract settled. No implementation handoff supplied.

— **PI/OpenAI**