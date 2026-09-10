---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 13995
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_newfamily_kimi.trace.jsonl
generated: 2026-09-09T15:22:17.610111+00:00
---

# bounded completion

## First call reasoning

Give brainstorm: mechanisms, construction change, falsifiable predictions, cheap checks, observed vs inferred, no winner. Address whether including answer behavior in contrast is right, and whether ant>dog M2 gap is actionable.
## First call answer

## Reconstruction (observed vs inferred)

**Observed:**
- U is a rank-4 projector fit on identity/prose template mean differences (dog/ant prose vs spider prose), L20 peak, L32 output attenuation.
- Patch: `P h' = (1−C) P h + C Δ` at prefill-last-3 + decode-last-1 positions, continuous steering.
- Naming + legs digit transfer reliably at C≈1.0–1.5; yes/no property answer does not (dog: No dominant at every C; ant: transfers weakly at C=1.0, reverts at C=2.0).
- M2: ||U Uᵀ d_answer||/||d_answer|| = 0.033 (dog), 0.041 (ant) — the Yes−No unembedding direction is ~3–5% inside the span.
- M3 probe: the answer position *does* attend to the patched `Answer:` region, yet No persists.
- Top-k is informative, not degenerate (M4 refuted); random in-span control shows dog digit is generic-prior readout, ant digit is direction-specific.

**Inferred (not directly shown):**
- That d_answer (a *weight-space* direction, Yes−No unembedding difference) is the right probe of the *activation-space* decision direction. The M2 ratio measures whether the logit-preference direction has support in U, not whether the residual-stream direction that *encodes* the decision is in U. These can diverge badly.
- That 3–5% projection is "the cause" of failure rather than a symptom of U being fit on the wrong contrast.
- That C=1.5 is a single operating point valid for both channels — evidence suggests legs/naming and yes/no have different C-response curves.

## Distinct mechanisms

**H1 — Construction mismatch (the framing question, favored structure of the fix):** U is fit on prose-identity variance, which is high-variance and rank-4-saturated; the yes/no decision direction is low-variance in the prose distribution and never enters the top-4 singular directions. The subspace is *correctly fit to the wrong data*. Construction change: augment the template set with **minimal answer-behavior pairs** — same question template, source vs target animal, forced ` Yes`/` No` completions — and take the mean difference at the answer-position residual (L20) as additional contrast directions before SVD. I.e., U = SVD([identity-prose deltas ; answer-behavior deltas]). This is *not* claiming the answer must leave the subspace; it's claiming the subspace was never given the answer's coordinates.

- *Falsifiable prediction:* with the augmented U (same rank or rank 5–6), ||U Uᵀ d_answer||/||d_answer|| rises from ~0.03–0.04 to >0.3, and prop-dog flips to ` Yes` at some C ≤ 1.5 **without** degrading naming at C=1.0. If the projection ratio rises but behavior doesn't move, the weight-space probe was the wrong instrument (H3).
- *Cheapest check:* pure weight math, no generation — refit U with answer pairs added, recompute the M2 ratio. Minutes.

**H2 — The decision direction genuinely cannot live in the same linear subspace (the "must leave" alternative):** the yes/no binding is computed downstream of L20 (e.g., in L24–L32 attention/MLP composition from the *question* semantics + the patched identity), so no rank-extension of an L20 prose subspace will contain it. The answer behavior isn't a direction to add; it's a *later-layer readout* of an in-span identity direction that the attenuation at L32 corrupts.

- *Falsifiable prediction:* even with answer-behavior contrast added (H1 fix), prop-dog stays No; but **patching at the layer where d_answer first becomes linearly decodable** (probe each layer for Yes/No decodability from the residual) transfers it. Distinct signature: augmentation raises the M2 ratio but behavior is flat.
- *Cheapest check:* linear probe of Yes/No decodability per layer on unpatched source/target runs — one forward pass each, no steering.

**H3 — Instrument error / wrong d_answer:** the Yes−No unembedding difference is a logit-space axis; the actual decision may be encoded as a direction d_act = mean residual at answer position (source-correct) − (target-correct), which could be largely in-span already while d_answer is out-of-span. Then M2's near-zero ratio is measuring the wrong vector and the real failure is elsewhere (H4 or H2).

- *Falsifiable prediction:* ||U Uᵀ d_act||/||d_act|| ≫ 0.05 while d_answer stays at 0.03. If so, "out-of-span" was an artifact and the construction change should target d_act, not d_answer.
- *Cheapest check:* compute d_act from cached activations (the contrast pairs already exist for building U); projection math only.

**H4 — Unintended learning/steering dynamic: reflection geometry + saturating head.** At the answer position the patch sets P h′ = Δ (C=1) regardless of h, but the head's logit gap responds to the *full* residual, and the out-of-span component of h (≈95–97% of the decision signal) is untouched and source-bound. Increasing C doesn't scale the out-of-span component at all — it only overshoots the in-span part (C=2 regressions: dog digit 2, ant revert). So the C-sweep *cannot* cross the yes/no threshold no matter how large C gets; the observed dog p(Yes) rise 0.066→0.208 is the small in-span share of d_answer (≈3%) being amplified, which asymptotes below the No logit. One-rule-both-animals then structurally guarantees dog fails (smaller in-span share).

- *Falsifiable prediction:* p(Yes)_dog(C) fits a saturating curve asymptoting below p(No); doubling C to 4 raises p(Yes) < 0.30 while wrecking prose. Contrasts with H1, which predicts a flip at moderate C once the direction is in-span.
- *Cheapest check:* already half-done — fit the existing 4 C-points; one extra run at C=3 discriminates saturation from linearity.

**H5 — Implementation error (layer/position mismatch at the answer token specifically):** the edited positions are "prefill last-3, decode last-1," and attention shows mass on 41–43 (patched) — but the *decision* may be read from the `Is`/question positions (28, 30), which are attended but **unpatched**. The patch geometry edits where identity is written, not where the answer-relevant key/value is read.

- *Falsifiable prediction:* extending the patch to the `Question`/`Is` positions (or to the animal-mention token) flips prop-dog at C=1.0 with the *current* U. If it does, no construction change is needed — the subspace was fine, the position set wasn't.
- *Cheapest check:* one patched run with the position set extended; reuses existing U and Δ. This is cheaper than H1's refit and should arguably be run first as a control.

## On the ~5% ant > dog gap (0.041 vs 0.033; bare 0.051 vs 0.036)

**Observed:** the ordering is consistent across spaced/bare tokenization, and it aligns with the behavioral asymmetry (ant transfers at C=1.0, dog never does). **Inferred:** that the difference is causal. With rank-4 SVD on ~3–5% residual support, estimation noise on these ratios is plausibly of the same order as the gap; no error bars were computed. Verdict: **suggestive, not yet actionable**. Cheap way to make it actionable: bootstrap the template set (drop-one-prose-pair refits) and report the ratio distribution; if dog's 95% interval stays below ant's point estimate, treat the asymmetry as real and let it set per-animal expectations (ant flips first under any fix). Cost: projection math only.

## Discriminating sequence (cheapest-first, no winner chosen)

1. **H3 check (free):** compute d_act projection ratio from existing contrast activations. If in-span, M2's framing was an instrument artifact — stop before rebuilding U.
2. **H5 check (one run):** patch the attended-but-unpatched `Question`/`Is`/animal-mention positions with current U. If prop-dog flips, construction is innocent.
3. **H1 check (minutes):** refit U with answer-behavior contrast pairs; M2 ratio (and d_act ratio) should jump. Then one steered run at C=1.0–1.5: prop-dog flips → construction mismatch confirmed; ratio up but behavior flat → H2 (later-layer composition), escalate to the per-layer decodability probe.

The framing question's answer is therefore conditional, not yes/no: include answer behavior in the contrast **only after** H3 confirms d_answer (or d_act) is the right vector and H5 confirms the positions aren't the culprit; otherwise the construction change fixes the wrong variable.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_newfamily_kimi.trace.jsonl`
