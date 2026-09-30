## Inherited decisions
Both goals remain unmet.2628 failed its frozen prerequisite: projected bracketing2/8, ordering7/8, and no causal generations. Retire that candidate without changing its gate, rank, center, or dose.

The supervisor approved **B: one representation-neutral readout transform**, evaluated on cached development examples.

## Diagnosis
**A is not yet a minimal reference reproduction.** The pinned repository supplies transport/readout code, not executable sparse decomposition and causal clamping. Dictionary construction, coefficient replacement, normalization, and coverage remain consequential choices. Calling a new implementation “the reference” would hide those choices.

B directly tests the primary hidden-not-said goal without another geometric prerequisite. Its hypothesis is limited: probability weighting may reduce rare-token dominance relative to signed contrast. It does **not** eliminate tiny-denominator artifacts or predict everything subsequently spoken.

No better-supported third method warrants adding another candidate now.

## Recommendation: exact approved test

**Budget/data:** one ≤300-second local replay of all eight v4 cases from `out/2026-09-30_142814_jlens-one-pass`. Zero transformer forwards, generations, or calibration. Preserve the existing forward-rejection guard and cached-generation provenance.

For each un-erased representation \(R\in\{\mathrm{J24},\mathrm{plain24},\mathrm{plain27}\}\), obtain its existing logits \(z_R\) and same-prefill final logits \(z_F\). Normalize over the **entire vocabulary before masking**:

\[
\ell_R=\log\operatorname{softmax}(z_R),\quad
\ell_F=\log\operatorname{softmax}(z_F),\quad
d=\ell_R-\ell_F,
\]
\[
s(t)=e^{\ell_R(t)}\max(d(t),0).
\]

This is a **positive token-KL contribution score**, not total KL divergence.

Apply unchanged prompt-word and greedy-final-token masks, with \(k=32\). Only unmasked tokens with \(d>0\) qualify. Rank stably using \(\ell_R+\log d\), avoiding probability-product underflow; all other tokens receive rank score \(-\infty\). Return fewer than32 if necessary. Resolve exact ties deterministically by token ID.

**Controls:** apply that identical transform to all three representations. For each, also substitute the next case’s final distribution cyclically, retaining the current case’s masks. Retain probability-excess and incumbent half-erasure comparisons; do not combine erasure with the new candidate.

**Scoring:** preserve frozen aliases and actual-output scoring, with failures/unscorable cases retained in the denominator. Report alias-checked joint counts and within-prompt AUROC. Compute AUROC from these final ranking scores: ineligible labels rank below eligible labels; ties, including two \(-\infty\) scores, receive0.5. Report evaluable denominators; do not replace the scorer or expand aliases after inspecting results.

**Predeclared selection:** highest alias-checked joint count wins; ties prefer **plain27 > J24 > plain24**. Promising requires ≥7/8, exceeding the incumbent6/8, and strictly beating its own mismatched-final control.

Before new-example evaluation, symmetric blinded review must find no definite input/said leak among that winner’s counted passes. If it fails, do not switch retrospectively to another representation. If all three reach8/8, or matched≈mismatched, investigate ceiling/comparator irrelevance rather than infer useful subtraction.

Freeze a promising reviewed winner before new examples. All v4 results remain development.

## Minimal evidence and risks
Save cache/source identities, zero-forward assertion, masks, eligibility counts, tie counts, top32, per-case metrics, and—for selected tokens and scored aliases—\(\ell_R,\ell_F,d,\log s\), signed-contrast rank, and probability-excess rank. These distinguish probability weighting from denominator-driven promotion.

Multi-token speech leaks, incomplete aliases, probability miscalibration, and development-set selection remain risks. End-pass scoring must never feed an earlier edit.

## Need from main agent
None; contract settled. No implementation handoff here.

— **PI/OpenAI**