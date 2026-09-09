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

## Displacement result (task 933) - read-out location is the discriminator, not delta alignment

Ran `slop/answer_position_run.sh` (both animals, one GPU job). Measured cos(delta, d_act) and
the displacement of the L20 answer-position residual along d_act, normalized by d_act_norm.

| animal | C | cos(delta,d_act) | displacement/d_act_norm |
|---|---|---|---|
| dog | 1.5 | 0.8417 | 1.3418 (over-shoot) |
| ant | 1.0 | 0.8486 | 1.0648 (near target) |

Both deltas point strongly along d_act (cos ~0.84-0.85 = d_act_inspan). Both displace the
answer-position residual along d_act by >= target (dog 1.34x, ant 1.06x). Dog displaces MORE
than ant (over-shoot).

Prediction tree applied: ant's displacement (1.06x) is NOT >> dog's (1.34x); both move
similarly (both >= target, both cos 0.84), but only ant flips (transfers at C=1.0, dog stays
` No`). => Delta alignment is NOT the discriminator; the read-out LOCATION is the problem.
The yes/no head does not read the L20 answer-position residual we are displacing (or dog's
over-shoot pushes it into a wrong region). Next test: H5 - patch the attended-but-unpatched
Question/Is positions (28,30) with current U; if prop-dog flips, the position set (not the
subspace or delta) is the culprit. If it still does not, the decision is read from a later
layer (H2), escalate to a per-layer yes/no decodability probe.

-- PI/[k3]

## CIRCULAR-BUG AUDIT (2026-09-10, supervisor-caught) - H3 reversal is INVALID, M2 re-opened

The equality cos_delta_dact == d_act_inspan (dog 0.8417==0.8417, ant 0.8486==0.8486) is a
circular-dependency artifact, not evidence. BOTH probes (m2_projection.py and
answer_position_probe.py) compute d_act as the mean L20 last-position residual difference
target MINUS spider over the NAMING CONCEPT_TEMPLATES:
    d_act = mean(template_residual[target, L20, -1] - template_residual[spider, L20, -1])
and delta_full (the prose delta) is computed IDENTICALLY:
    delta_full = mean(template_residual[target, L20, -1] - template_residual[spider, L20, -1])
So d_act == delta_full, and
    d_act_inspan = ||U U^T d_act||/||d_act|| = ||delta_proj||/||delta_full||
    cos(delta, d_act) = cos(U-projected delta_full, delta_full) = ||delta_proj||/||delta_full||
Both reduce to the naming-template contrast's in-span fraction (trivially high because U is
fit on those contrasts). d_act was never an independent answer-direction measurement.

=> The H3 "d_act ratio 84% => M2 was an artifact" reversal is WRONG. M2 is RE-OPENED. The
property source-binding answer direction was never actually measured against the property
prompts.

Correct measurement needed: d_act must come from clean forward passes of the PROPERTY prompt
pairs (spider property vs target property, e.g. "Is the animal that spins webs a mammal?" vs
"Is the animal that barks... a mammal?"), no patch, no U, at the answer position (content_end-1,
L20). delta stays the naming/prose contrast. Report cos(delta, d_act_raw), ||d_act_raw||, and
the in-span ratio of d_act_raw.

-- PI/[k3]

## CORRECTED (non-circular) answer-position result - M2 RE-CONFIRMED, H3 reversal was circular

Fixed probe (d_act now from clean property-prompt forwards; delta stays naming contrast).
circular_check_cos_eq_inspan = False for both. Corrected real numbers:

| animal | C | cos(delta, d_act) | d_act_inspan | displacement/d_act_norm |
|---|---|---|---|---|
| dog | 1.5 | 0.0748 | 0.0965 | 0.1416 |
| ant | 1.0 | 0.0317 | 0.0488 | 0.0656 |

Interpretation (calibrated): M2 is RE-CONFIRMED on valid (non-circular) grounds. The
yes/no answer direction d_act (from the property prompts) is near-zero in-span for BOTH
animals (~5-10%), the prose delta does NOT align with it (cos ~0.03-0.08), and the C-patch
displaces the answer residual toward target by only ~6-14%. The property source-binding is
consistent with the answer decision being largely OUTSIDE the identity-prose U-span and not
driven by the prose delta.

NOTABLE asymmetry: ant has LOWER d_act_inspan (0.049), LOWER cos (0.032), LOWER displacement
(0.066) than dog (0.097, 0.075, 0.142), yet ANT transfers (C=1.0) and dog does not. So the
tiny in-span fraction is NOT what separates ant (flips) from dog (doesn't). That points the
read-out location / other mechanism (H5: patch the attended-but-unpatched Question/Is
positions, or later-layer composition H2) even more strongly.

-- PI/[k3]

## H5 result (task 934): patched Question/Is positions does NOT flip prop-dog -> escalate to H2

Extended patch to attended-but-unpatched positions [28,30] (Question/Is) in addition to
last-3, same U and delta. Result (pueue 934, `out/2026-09-10_h5-prop-*`):

- prop-dog C=1.5: first ` No`, p(No)=0.342, p(Yes)=0.142, r2=0.014, coherent prose
  ("The animal that spins webs is a dog... Dogs are mammals"). STILL No - did NOT flip.
- prop-ant C=1.0 (positive control): first ` Yes`, p(Yes)=0.284, p(No)=0.250. Flip preserved.

Prediction tree: dog still stuck => the position set is NOT the culprit. ESCALATE to H2:
per-layer yes/no decodability probe - at which layer does the target-vs-source yes/no answer
first become linearly decodable from the residual, and is it before or after L20? If the
answer direction becomes decodable only AFTER L20 (e.g. L24-32), a L20 edit cannot carry it
(H2 "must leave" / later-layer composition), and the source binding persists regardless of
patch geometry on the L20 identity span.

-- PI/[k3]

## RECORD CORRECTION (supervisor): prop-ant C=1.0 (H5) is NOT a clean transfer

The prop-ant C=1.0 H5 continuation begins ` Yes` but the prose identity is still SPIDER:
"The spider is a small, hardworking insectivore that builds intricate webs... possesses two
pairs of short, stubby antennae..." So it is answer-movement WITHOUT identity persistence
(the plan's failure modes: digit/answer movement without identity is not transfer). Label
prop-ant C=1.0 as answer-movement-without-identity-persistence, and note ant property
transfer is WEAKER than the C-sweep top-k suggested (top-k ' Yes' 0.297 at C=1, but the
continuation stays spider). The property family currently has NO clean transfer cell; the
spider-binding persists for both identity-holding and answer-moving cases.

-- PI/[k3]

## H2 per-layer decodability probe result (naive logit-lens)

Ran `scripts/h2_layer_probe.py` (logit-lens: RMS-normalize each layer residual difference,
scale by norm_gain, unembedding, report Yes-No logit gap) for dog and ant property. Result:
gaps oscillate between ~+0.78 and -0.78 across layers for BOTH animals (e.g. dog L1-6 +,
L8-13 -, L18-19 +, L20 =0.0000, L21-22 -, L23-27 +, L28-30 -, ...). The constant +/-0.78
magnitude indicates the raw-logit naive logit-lens is NOT calibrated (RMS-normalizing each
layer makes every layer's projection onto the normalized Yes-No axis near-parallel, so the
magnitude is dominated by one direction).

ROBUST observable (not an artifact): dog L20 answer-position target-source diff_norm = 0.000,
and ant L20 gap = -0.781 (negative). For dog the L20 answer-position residual is IDENTICAL
for the dog and spider property prompts (diff 0.000), consistent with the earlier finding that
patching the L20 answer position does nothing for dog's answer. The target-vs-source answer
signal is NOT resident at L20 for dog at all.

Interpretation (calibrated, cautious): the naive logit-lens is unreliable for locating the
decodable layer (oscillation = uncalibrated readout). The dog-L20-zero is a robust signal that
the answer identity difference is not in the L20 answer-position residual. A per-layer linear
probe (train a logistic regression Yes vs No on the residual at each layer, report
cross-validated accuracy OR separating-direction cosine) would be the calibrated follow-up.
But the family evidence already locally excludes L20 spans, positions, and delta alignment; the
answer decision is most likely formed later or read from a differently-located residual.

-- PI/[k3]
