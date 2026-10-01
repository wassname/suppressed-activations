# Next test: paired animal identities with the same answer

— PI/OpenAI

## Decision and evidence

Choose **four prospective generations using the unchanged readout**, pairing horse/cow and cat/goat, all asking for leg count. The supervisor approved this concrete choice over generic-reference subtraction.

This tests identity selectivity, **not purity or necessary intermediate computation**. These are already-used v2 concepts with new prompts/properties, not unseen-concept generalization.

Evidence:
- `slop/research/2026-10-01_after-native-v4-question.md`: “identity information survives, but answer-category association remains a plausible alternative.”
- `slop/reviews/2026-10-01_native-v4-result-review.md`: “There are no same-answer pairs in this dataset.”
- `data/english_hidden_words_v5_matched_output.json`: “reserved for a method that first passes its development and semantic gates.” Its contents were read as instructed; **no evaluation or advancement is authorized here**.
- The supplied reference review establishes no missing centering operation. Subtraction would introduce a new representation plus arbitrary-template/norm confounds; inverse-affine fitting adds greater complexity. Neither is selected.

## Frozen inputs and execution

In this order, use these exact prompt strings, without trailing spaces:

1. `Fact: The number of legs on the animal that neighs and is ridden using a saddle is`
2. `Fact: The number of legs on the farm animal that moos is`
3. `Fact: The number of legs on the domestic animal that purrs is`
4. `Fact: The number of legs on the farm animal with a beard and curved horns is`

User content is exactly `Complete the fact with only the missing word or phrase:\n` followed by the prompt. Retain 2688’s native rendering, thinking scaffold, pinned model/tokenizer, greedy decoding and EOS policy; no Japan/Tokyo demonstration. Four trajectories only, maximum 32 new tokens each, no retries or output-dependent replacement.

Primary: J residual24, half-erasure, output mask1, k32, unchanged input-prefix exclusion. Controls: equally processed half-erased plain24/plain27 and mask-only J24. All readouts share the same trajectories and last-prefill captures. No layer, dose, mask or k rescue.

## New diagnostic: unmasked identity scores

This is **new evaluation**, never a reinterpretation of already-masked ranks.

For each method, obtain full-vocabulary logits **after its representation transformation and half-erasure where applicable, before both lexical masks**, preserving production operation order. Compute float32 log-softmax.

Freeze label sets:

- horse: `horse`, `horses`
- cow: `cow`, `cows`
- cat: `cat`, `cats`
- goat: `goat`, `goats`

An eligible vocabulary token’s individually decoded string, stripped of surrounding whitespace and casefolded, must equal one entire declared label. Exclude punctuation wrappers, compounds and partial pieces. Enumerate and save eligible IDs before viewing outputs; empty sets are unsupported, not permission to add prefixes. Labels are evaluation-only: never inputs to erasure, ranking, masks or generation.

Define \(s_x(c)\) as the maximum log-probability over eligible tokens for concept \(c\). Maximum-over-variants has frequency/tokenization bias; report winning tokens and constituent scores.

For pair \(a,b\), report:

\[
d_a=s_{x_a}(a)-s_{x_a}(b),\qquad
d_b=s_{x_b}(a)-s_{x_b}(b),\qquad
D=d_a-d_b.
\]

Identity preference reverses when \(d_a>0>d_b\). \(D\) is the paired difference-of-differences: a fixed preference for one label cancels, although context-dependent tokenization/frequency effects need not.

Report both pairs individually, four own-minus-partner margins, reversal count /2, and primary-minus-control \(D\). No fitted cutoff or baseline-dominance acceptance gate. For scale, a context-independent label preference gives \(D=0\); enumerate the four within-pair label-assignment permutations as descriptive null comparisons, not powered significance tests.

## Integrity and separate goal metrics

Reuse `scripts/english/08_jlens_one_pass.py`. Prefer diagnostic persistence in its production scoring path. Cached reconstruction is acceptable only after demonstrating parity with production logits and final masked rankings using pinned states/weights. No second transformer pass or separate inference pipeline.

Preserve exact rendered IDs, generated IDs/text, actual token counts, full top32 lists, scores and configuration. Keep incorrect, capped and nonshared answers in /4 and /2 denominators. Separately report pairs whose complete lexical answers casefold/strip to exactly `4` or `four`; do not substitute expected answers for actual output.

Retain frozen lexical joint scoring and within-prompt AUROC as legacy metrics, explicitly mask-sensitive. Separately review all top32 lists for clear identity, input equivalents, actual-said equivalents and formatting. No generated text becomes a future-text mask.

## Interpretation and next action

- **Reversals with positive \(D\):** evidence against a purely context-independent animal/number association; retain the representation for a subsequent targeted exclusion improvement. Purity and causal use remain open.
- **Positive \(D\), no reversals:** contextual discrimination with persistent label bias; report partial progress, not clear own-identity selection.
- **No separation across methods:** favors association or weak identity information on these prompts; next consider the explicitly new generic-reference subtraction, not parameter rescue.
- **Plain controls selective, primary not:** investigate suppression’s loss of identity information rather than declaring identity absent.
- **Answers differ or scoring parity fails:** respectively limit the same-output interpretation or repair diagnostic persistence; never replace prompts post hoc.

ML-debug limitations: no new run, smoke, tensor comparison, timing, memory or seed spread was executed. Implementation mismatch, evaluation undercoverage, cue association and unknown causes remain live; supplied evidence does not justify numerical causal probabilities.