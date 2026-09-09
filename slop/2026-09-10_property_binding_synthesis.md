# Property-binding brainstorm synthesis (propbind_glm + propbind_kimi)

Post-family /moa-brainstorm, plan task 3: why does the yes/no answer head stay spider-bound
while prose identity transfers? Both GLM and Kimi converge on M1-M5 with the same
mechanisms; neither picks a winner. Key cheap-resolution insight accepted by both: the
answer position IS patched (prefill last-3 = `Answer`/`:`/` `, decode last-1 = answer token;
C=2 perturbation 25.7), so "position unpatched" is refuted. The yes/no logits are DEGENERATE
(p_source ~ p_target ~ 0.000) at every property cell, so the sampled first token is
unreliable and the "answer head" framing may be measuring the wrong channel.

## Converged mechanisms (Kimi labels; GLM equivalent)

- M1 Implementation: patched tensor is not the stream the head reads (position/layer off-by-one
  between prefill and decode, or the answer logit reads a different position than the patch).
- M2 Subspace/gradient mismatch: yes/no decision lives OUTSIDE the rank-4 U-span (U is fit on
  prose templates; identity in-span, answer out-of-span). The digit transferring at C=1 shows
  SOME answer content is in-span; yes/no may be a lower-variance direction the rank-4 fit
  misses. Additive: the answer head sees the unpatched source residual component.
- M3 Unintended dynamic: the decision is committed EARLIER (during prefill at the
  animal-mention / question tokens); the answer position only reads out a cached decision via
  attention. Patching last-3 + answer token rewrites local identity but not the upstream
  key/value the answer position attends to. Explains mirror (source-correct Yes while prose
  says ant).
- M4 Degenerate-logit calibration collapse: p_src ~ p_tgt ~ 0 means yes/no both near-zero;
  the emitted Yes/No may be a fallback argmax or a wrong logit slice. Saturated head
  insensitive to a 25.7 perturbation.
- M5 Reflection overshoot at C=2: explains C=2 regressions (digit 2, prop-ant reverts, loops)
  but NOT prop-dog staying No at C=1, so it is co-occurring, not the whole story.

## Cheapest discriminating checks (both agree on the first move)

1. Top-k logit inspection (M4) - one forward pass: print full next-token distribution at the
   answer position (content_end) for prop-dog (and prop-ant) at C=0 and C=2. If Yes/No are not
   cleanly in top-k, the "answer head" is measuring the wrong channel. GLM: also dump the
   attention row for the same position, simultaneously testing M3 and M4.
2. ||U U^T d_answer|| / ||d_answer|| (M2) - no generation, projections only.
3. Full activation swap at answer position (M1) - one patched run.
4. Attention knockout to animal-mention positions (M3) - one patched run.
5. C-sweep C<1 for prop-dog (M5) - fill in C < 1.

## Selected next bounded test (decision)

Property-answer logit + attention dump at the answer position: prop-dog and prop-ant at C=0
and C=2, reading the full top-k distribution AND the attention row of the first decode step.
One forward pass discriminates M1 (which stream), M3 (where attention goes), M4 (degeneracy
real). This is CPU/GPU-local, no new prompt. Not yet run - GPU occupied by LUCID3 task 928,
929 naming C=1/1.5 queued behind it. Attn capture added to the runner
(`--capture-attention`, output.attentions first step last layer answer position); standalone
probe rejected (would compute a different delta/U).

## GPU-free top-k extraction (refutes M4, informs M2/M1)

Read from existing 926 `result.json` `top_tokens` (first-step answer-position distribution;
p_source/p_target tracked the wrong token-channel). No forward pass needed.

| cell | p(No) | p(Yes) | p(No)-p(Yes) | top3 |
|---|---|---|---|---|
| prop-dog C=0.0 | 0.298 | 0.066 | +0.231 | No, 1, thought |
| prop-dog C=0.5 | 0.332 | 0.079 | +0.253 | No, 1, thought |
| prop-dog C=1.0 | 0.387 | 0.098 | +0.289 | No, 1, Yes |
| prop-dog C=2.0 | 0.388 | 0.208 | +0.180 | No, Yes, 1 |
| prop-ant C=1.0 | 0.263 | 0.297 | -0.035 | Yes, No, 1 |
| prop-ant C=2.0 | 0.333 | 0.259 | +0.074 | No, Yes, 1 |

Interpretation (calibrated): the yes/no answer-position distribution is NOT degenerate (M4
refuted) - it is informative and moves with C. prop-dog stays source-bound (`No` dominant at
every C; at C=2 `Yes` rises 0.066->0.208 but `No` 0.388 still wins), a real monotone
source-bound effect, *likely* (0.7) a decision direction not carried by the delta or committed
early. prop-ant transfers at C=1.0 (`Yes` 0.297 edges `No` 0.263, margin -0.035) and reverts
at C=2.0 (`No` 0.333 over `Yes` 0.259) - the over-shoot signature, consistent with M2/M5.
The remaining open question is M3 (attention path) - does the yes/no head attend to early
unpatched tokens - which needs the attention capture; M1/M2 need the projection check
(||U U^T d_answer|| / ||d_answer||).

## Attention-capture finding (M3 deferred)

Added a minimal `--capture-attention` flag to the runner (attn_implemented via
`generate_with_first_logits` output_attentions). Result: the model uses **SDPA attention**
by default (`transformers` error: `sdpa attention does not support output_attentions=True;
please set your attention to eager`). With SDPA, `output.attentions` is a 0-length tuple, so
no attention weights are returned; `answer_position_attention` is None. Getting attention
weights requires reloading the model with `attn_implementation="eager"` - a model-loading
change, separate from the generate path, and a real cost. Per supervisor (keep the flag
minimal, no general attention framework), this is DEFERRED: the M3 attention discriminator
needs an eager attention run, not a runner patch. The standalone probe was rejected earlier
(risks a different delta/U); the runner extension is correct but blocked by SDPA. Leave
`--capture-attention` in place (harmless, returns None under SDPA) and note the eager
prerequisite.

## M3 attention result (task 930, eager attention)

Ran prop-dog C=1.5 and C=2.0 with `SUPPRESSED_ATTENTION=eager` + `--capture-attention`
(result `out/2026-09-10_attn-prop-dog-C1.5` and `-C2.0`). Answer-position attention row
(last layer, mean over heads), q_len 44, first decode step:

- C=1.5: first `No`, top5 `[(No,0.397),(1,0.165),(Yes,0.100),(thinking,0.100),(2,0.042)]`.
  Top-6 attention positions (by mass): [43,42,30,27,41,28].
- C=2.0: first `No`, top5 `[(No,0.423),(Yes,0.156),(1,0.137),(thinking,0.057),(2,0.045)]`.
  Top-6 attention positions: [43,42,30,27,41,28].

Decoding positions: 43=` `, 42=`:`, 41=`Answer` (the patched prefill last-3), 30=`Is`,
28=`Question`, 27=newline (early question tokens). The answer position attends to BOTH the
patched `Answer:` region (43,42,41) AND the question header/`Is` tokens (28,30,27).

Interpretation (calibrated): this partially refutes pure-M3 (the head reads the patched
`Answer:` region). The `No` stays dominant at both C despite the `Answer:` region being
patched toward dog/prose. The source-binding therefore is not that the answer head ignores
the patch; it is that the yes/no DECISION direction is not carried by delta (M2), even
though the answer position attends to the patch. Weight M2 over pure-M3, *likely* (0.65);
the mid-prompt `Question`/`Is` attention (28,30,27) may also carry a question-format/pragma
prior that fixes the `No` answer-shape regardless of the animal (DeepSeek's pragmatic-default
account). Discriminating those two needs a prompt rephrase or the M2 projection check
(||U U^T d_answer|| / ||d_answer||).

## M2 projection ratio (real model) - M2 CONFIRMED

Ran `scripts/m2_projection.py` on the real Qwen (L20 peak / L32 output attenuation span,
rank 4). d_answer = unembedding( Yes) - unembedding( No) (pure weight math). Ratio
||U U^T d_answer|| / ||d_answer||:

| target | ratio Yes/No (spaces) | ratio (bare) |
|---|---|---|
| dog | **0.0326** | 0.0355 |
| ant | **0.0410** | 0.0509 |

Both are near-zero (<5%), and ant > dog (0.041 vs 0.033, bare 0.051 vs 0.036) as the
asymmetry predicted. Tiny-model smoke: dog 0.21 / ant 0.24 (not representative).

Interpretation (calibrated): **M2 is confirmed** - the yes/no decision direction is almost
entirely OUTSIDE the U-span for both animals; the U-span carries ~3-5% of the answer
behavior. ant's U carries slightly more, consistent with ant property transferring at C=1.0
while dog never does. This explains the source-binding: the patch can move identity/prose
(near-in-span) but barely touches the yes/no decision (out-of-span), so `No` stays dominant.
The principled next question (new family): should the subspace be built from a contrast that
includes the answer behavior (Yes/No tokens), not just identity prose. Near-zero dog ratio
makes this the central design question.

## References

- GLM: `slop/reviews/2026-09-09_glm-5.3-flash_propbind_glm.md`
- Kimi: `slop/reviews/2026-09-09_kimi-k3_propbind_kimi.md`
- Brief: `batchwork/slop/2026-09-10_property_binding_brief.md`

-- PI/[k3]
