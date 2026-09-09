# New-family synthesis: should the subspace include the answer behavior?

Both GLM and Kimi new-family brainstorms agree the framing answer is CONDITIONAL, and the
refit must be deferred until two cheap instrument/position checks clear. Neither picks a
winner.

## Converged construction question (conditional)

Include answer behavior in the contrast (augment U with answer-behavior deltas) ONLY after:
- H3 confirms the decision direction is in-span (i.e. the M2 near-zero was not a
  wrong-instrument artifact), and
- H5 confirms the edited positions aren't the culprit.

Otherwise the construction change fixes the wrong variable.

## Kimi H1/H2/H3/H4/H5 set vs GLM A/B/C/D

- H1 (=GLM refit/U2): U fit on prose-identity variance (high-variance, rank-4 saturated); the
  yes/no direction is low-variance and never enters top-4. Fix: augment template set with
  answer-behavior pairs (source vs target, forced Yes/No completions), mean diff at the
  answer-position L20 residual, concatenate before SVD. Prediction: M2 ratio jumps 0.03->0.3+;
  prop-dog flips Yes at C<=1.5 without degrading naming C=1.0.
- H2 (later-layer composition, "must leave"): yes/no binding computed downstream of L20; no
  rank-extension of L20 prose U contains it. Check: yes/no linear decodability probe per layer.
- H3 (instrument error, CRTICAL): d_answer is a WEIGHT-space (unembedding) direction; the
  activation-space decision direction d_act = mean residual at answer position (source-correct
  - target-correct) may be IN-span while d_answer is out-of-span. M2's ratio measures the wrong
  vector. Check is FREE (projection on existing contrast activations). Stop before refit if
  d_act in-span.
- H4 (saturating head / reflection): the out-of-span ~95-97% of the decision signal is
  untouched by C; increasing C only overshoots the in-span part (dog p(Yes) 0.066->0.208
  asymptotes below No; dog p(No) 0.39 stays). One-rule-both-animals structurally guarantees dog
  fails (smaller in-span share). Check: C=3 run, fit saturation vs linearity.
- H5 (position/geometry, one run): decision read from attended-but-UNPATCHED Question/Is
  positions (28,30) rather than patched Answer: (41-43). Patch geometry edits where identity is
  written, not where answer key/value is read. Check: extend patch to Question/Is/animal-mention
  positions with current U, one run. If prop-dog flips, no refit needed.

## Cheapest-first order (Kimi; GLM equivalent)

1. H3 check (FREE): compute d_act projection ratio. If in-span, M2 was instrument artifact -
   stop before rebuilding U.
2. H5 check (ONE RUN): patch attended-but-unpatched Question/Is/animal-mention positions with
   current U. If prop-dog flips, construction innocent.
3. H1 check (minutes): refit U with answer-behavior contrast; M2 + d_act ratio jump. Then one
   steered run C=1.0-1.5: prop-dog flips -> construction mismatch; ratio up but flat -> H2.

## ant>dog M2 gap (0.041 vs 0.033): suggestive, not actionable

Directionally consistent across spaced/bare and aligns with the behavioral asymmetry (ant
transfers at C=1.0, dog never). But rank-4 SVD on ~3-5% residual support -> estimation noise is
the same order as the gap; no error bars. Actionable via bootstrap (drop-one-prose-pair refits,
ratio distribution). Treat as corroborating, not design input.

## Constraint

The span-correction construction still shows correct naming+legs at C=1.5 for both animals,
and the property source-binding is the last open goal-1 failure. The framing question is
whether the identity-prose U is the right contrast at all; the answer is conditional on H3/H5.

-- PI/[k3]
