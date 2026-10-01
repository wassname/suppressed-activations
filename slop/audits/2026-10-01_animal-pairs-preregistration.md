# Four same-answer animal probes

— PI/OpenAI. Frozen before pretrained inference; design dialogue: `slop/reviews/2026-10-01_after-native-v4-next-test.md`.

## Goal and decision

Test whether the existing readout distinguishes particular hidden identities when the answer is held constant, rather than returning only generic animal/number associations. This is a diagnostic of the current representation, not a new method, necessary-computation claim, purity certificate or research-goal completion. Four known-v2 concepts, new prompts/properties; v5 remains reserved/unrun.

Use exactly `data/english_animal_pairs_chat_v1.json`, order horse/cow/cat/goat, pairs horse/cow andcat/goat. Do not replace wrong, ambiguous or nonshared outputs. Uniform native-chat frame from2688, no trailing spaces, thinkingFalse, greedy32 cap, EOS248044/248046. Reuse08, J residual24, final-prefill position, half-erasure. Controls equally masked halfplain24/27 and mask-onlyJ. Same2686 input-prefix extension, output-mask1, k32. No new layer/k/dose/filter. No current-input preparation/backward or extra transformer pass. Cached scoring is permitted and asserted to make zero transformer calls.

## Label-independent readout; new diagnostic only

Persist four full-vocabulary logits after norm/head and representation/half-erasure, but before both lexical masks. Logging must not alter generation, ranking or scores. Labels enter only the diagnostic evaluator and existing outcome scorer.

Before any pretrained output, enumerate individually decoded vocabulary tokens whose stripped, casefolded string exactly equals horse/horses, cow/cows, cat/cats or goat/goats. Save all IDs/strings. No punctuation wrappers, partial prefixes or extra aliases; empty sets fail. Take float32 log-softmax over full-vocabulary logits. For each concept, score is maximum log-probability over its eligible IDs; save every constituent score and winner. Maximum-over-variants carries frequency bias.

For pair a,b with prompts x_a,x_b:

- d_a = s(x_a,a) − s(x_a,b).
- d_b = s(x_b,a) − s(x_b,b).
- D = d_a − d_b, in log-probability units (nats).
- Reversal iff d_a > 0 > d_b; ties do not count.

Report both pairs separately, each of four own-minus-partner margins, reversal count/2 and primary-minus-controlD. Also enumerate four independent within-pair label swaps as descriptive null comparisons, not powered significance tests. A context-independent preference givesD=0. No fitted cutoff, universal pass criterion or required dominance over baselines.

All cases remain in/4 and all pairs in/2. Report separately pairs where complete scoring text strips/casefolds to4 orfour on both cases; also report exact scoring-text equality, so four versus4 does not masquerade as identical strings. Do not substitute expected labels for actual output. Preserve complete raw output IDs/text/token counts, rendered input, legacy lexical/AUROC outcomes and all four top32 lists. Fresh semantic review distinguishes identities, input/actual-said equivalents, fragments and formatting. No future-text masking.

## Verification and next decision

SHOULD: four trajectories,≤128 generated tokens, same count of transformer forwards as generated tokens, zero cached forwards;72 legacy rows exact plus16 prefix candidates; raw pre-mask vectors exact across capture/replay and equal production half-erasure. Tiny CPU Qwen tests at seeds0/1 already check direct logits/erasure, selected scores and replay; full launcher smoke remains required. Preserve failures.

Reversals with positiveD support cue-dependent identity information and justify a targeted exclusion improvement next. PositiveD without reversals is partial discrimination with label bias. No separation across methods motivates a distinct generic-reference subtraction; plain success/J failure instead points to identity loss through suppression. Different answers limit same-output interpretation. None authorizes another mask/layer/k rescue or automatic v5 use.

Limit: these cues may independently activate animal words without the model using them to compute four. No causal-necessity claim. No pretrained result has been seen for these prompts.
