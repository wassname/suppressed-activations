# Design review: end-of-pass logit contrast

**Recommendation: run the proposed comparison with the controls below.** It discriminates between two readout operations, not between genuine hidden reasoning and a shortcut. This is development on observed8, not holdout validation or approval for earlier-layer editing.

## Mathematical distinction

Let \(N\) be the model’s final RMSNorm, including learned gain, and \(W\) its unembedding:

\[
u_J=N(J_{24}h_{24}),\quad u_F=N(h_{32}),\qquad
d=Wu_J-Wu_F.
\]

These are dimensionless logit differences—not probability differences and not subtraction before normalization. With \(p_J=\operatorname{softmax}(Wu_J)\),

\[
d_t=\log\frac{p_J(t)}{p_F(t)}+\log Z_J-\log Z_F.
\]

Thus ranking \(d\) equals ranking log-probability ratios, measured in nats, because the partition-function difference is token-independent. The sign of \(d_t\), however, does **not** identify \(p_J(t)>p_F(t)\). Do not inherit the existing positive-only cutoff.

One-row erasure instead computes, for greedy output row \(w_o\),

\[
e_t=w_t^\top u_J-\alpha
\frac{u_J^\top w_o}{\|w_o\|^2}w_t^\top w_o.
\]

It suppresses tokens according to their alignment with one unembedding row. Contrast subtracts the entire final-state vocabulary profile. Neither operation isolates a proven semantic component.

## Observed evidence

In `scripts/english/08_jlens_one_pass.py`, `generate_readout` captures only the first hook invocation: `"if not coverage[residual_index]"`. The forecast branch currently computes `"softmax(-1) - ...softmax(-1)"`, then masks `"excess <= 0"`; the proposal must remain distinct from that branch.

`out/2026-09-30_142814_jlens-one-pass/run.md` reports alias-checked joint recovery:

- masked J: **4/8**;
- half-erased J: **3/8**;
- masked plain27: **5/8**;
- half-erased plain27: **6/8**.

These are useful baselines, not evidence that contrast wins. In the same directory’s `erasure_traces.json`, December/J half-erasure removes `"relative_removed_norm": 0.11775808781385422`; `readout.json` records hidden rank worsening from **1 to 71**. This supports testing an alternative, but does not establish the cause.

Erasure also targets `" the"`, `" William"`, `" a"` and `" "` for violin, Hamlet, hydrogen and triangle—not necessarily the semantic answer.

## What contrast can falsely reward

A token can rank highly because final probability is extremely small, although intermediate probability is also negligible. Contrast may reward lens miscalibration, generic topic alternatives, fragments or punctuation rather than a specific hidden concept.

The existing Thursday masked-J list begins `" Tuesday", " Thursday", " Monday"`: listing most weekdays can recover the label without identifying Thursday specifically. `data/english_hidden_words_v4.json` explicitly says labels are “hypothesized intermediates, not proof of use.”

Scoring also misses semantic leakage: violin/plain27 has `"alias_checked_pass": true` alongside `"emitted_word_piece_hits": ["wind"]` after “the woodwind family.” Unlisted translations and suffixes can therefore produce apparent wins.

**Falsifiable risk:** improvement is driven mostly by the denominator, not input-specific intermediate evidence. Compare against masked \(-z_F\) and a fixed cyclic mismatch of final states, retaining each case’s original masks. Similar recovery and top-list overlap would undermine that interpretation; substantially better matched contrast would weaken this concern.

## Smallest implementation and checks

1. Add three scores inside the existing end-pass branch: J24−final, plain24−final and plain27−final. Subtract finite float32 logits **before** masking; retain signed scores and fixed k32.
2. Keep masked originals, existing erasure strengths, and matched probability subtraction as controls. Report per-case hidden recovery and said-word exclusion separately, plus unchanged joint metrics.
3. Assert identical vocabulary shapes, finite operands, residual indices 24/27/32, same-prefill provenance and identical masks. Check log-ratio rank equivalence, self-subtraction zero and label/continuation permutation invariance of ranking.
4. Save selected tokens’ component logits/log-probabilities and cutoff ties. Audit complete lists, not just AUROC; masked negatives can inflate it.

Final-state information is available at **end of prefill**, without another transformer pass or generated-text input. Current code returns after generation, but its saved states remain prefill states. This is timing-valid for readout only. Using \(h_{32}\), its greedy mask or contrast to choose an earlier edit violates the local-state constraint.

No commands, edits or inference were performed. Proposed numerical checks remain unexecuted; no generalization claim follows.

— PI/OpenAI