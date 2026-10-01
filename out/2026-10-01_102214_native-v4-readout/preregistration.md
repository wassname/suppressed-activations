# Native-chat v4, frozen prefix readout

— PI/OpenAI. Frozen before new outputs; prior v4 completion outputs are known development data. This is a prompt-frame/domain test, not unseen-concept evaluation, pure chat attribution, or causal editing. Reuse scripts/english/08_jlens_one_pass.py unchanged at SHA69455b6a07824eb675d6f738c6178691d9ff31929267944aae1b9ddf4eac6f3d and the five unchanged pinned helpers. Adviser dialogue: slop/reviews/2026-10-01_after-prefix-next-test.md.

## Decision and alternatives

The new2686 filter retained geography identities2/4 versus plain0/4, with full-list clean0confirmed and0–2/4 unresolved. Description-donor2687 changed0/2 intended initial answers. Test whether the frozen readout transfers beyond geography under native chat. More geography cases would not directly test that restriction; another filter would confound it. Reserved v5 remains unrun because its earlier prospective condition was not met.

## Exact data and method

- All eight data/english_hidden_words_v4.json cases, original order and labels/aliases unchanged. User content is exactly `"Complete the fact with only the missing word or phrase:\n" + case["prompt"]`. Preserve original prompt bytes, no appended space. Omit the old Japan/Tokyo demonstration. No case-specific additions or label-derived formatting.
- One native user message, no system message; pinned Qwen tokenizer, enable_thinking=False, add_generation_prompt=True. Thinking scaffold is input, not generated reasoning. EOS union248044/248046, greedy32-token cap. Keep wrong/refused/truncated/unscoreable outputs.
- J24, final-prefill position, half-erasure, output mask greedy1, k32, dtypes and old+complete-input-prefix masks exactly2686. No new stemming, synonyms, output-text mask, label selection, k/layer changes or fitting.
- Matched half-plain24/27 and mask-onlyJ controls. Other existing rows retained but cannot become a selected primary.
- Reuse unchanged08: first call captures eight ordinary generation trajectories and144 legacy rows; second call rescoring those saved states adds32 candidate rows and requires144 old rows exact (176total). Cached stage rejects full-model/inner-transformer forwards. This is not a second current-input neural pass and has no intervention.
- Record actual forward events by phase. Exactly eight prefills plus cached decode calls equals total generated tokens (at most256); rescoring has zero model forwards. No backward or current-input preparation.

## Checks and measurements

Pin source, original/derived dataset, this contract and helpers before work; copy them into the master artifact. Preserve generation IDs/text, rendered input, coverage, prefill tensors, all full-vocabulary candidate scores, exclusions/origins, results and matched controls. Check source/trace/state/row parity between capture and rescoring. Score each case's correct completion, hidden recovery and semantic exclusion separately. Record all8 denominator, expected-answer subset, definite input/said leaks and ambiguities; AUROC is not semantic certification and may be favored by masked labels. No same-answer pairs exist in v4, so no invented pair metric.

Selection: display the first case in original order with a clear returned hidden concept, with all leaks disclosed; if none, display case0 as a failure. No output-dependent prompt replacement. Full-list purity is reported under the previous convention, not added as a universal human gate.

## Predictions and falsifiers

- SHOULD: capture exactly eight trajectories; cached stage zero forwards;144 old rows exact. Any mismatch blocks interpretation and gets diagnosed before another experiment.
- Native answers likely become concise (rough planning bet75% at least7/8 correct, not an acceptance threshold). Wrong/long/NLI answers would weaken the frame hypothesis.
- Competing outcomes:35% useful non-geography identity examples;40% correct answers but plain ties/wins or J misses;15% persistent format/semantic-assay problems;10% implementation/other. Subjective planning weights, not measured probabilities.
- J-specific identity recovery with coherent outputs motivates a separately frozen matched-output transfer test. Plain ties/wins with coherent outputs argues against completion framing as the sole cause. Leaky identities remain partial positive examples, not clean successes. No automatic posthoc filter/parameter rescue.
- Preserve the difference between this comparison and old v4: both prompt frame and prefix exclusion differ from old completion results. Only matched methods within this run share all non-representation factors.

## Cost and verification

One normal default-queue job,300s TERM+15s grace, local GPU only, no priority change, ≤256generatedtokens. The already tested production source is unchanged. Re-run tiny real-Qwen chat+prefix smoke and verify new launcher's postflight against existing real artifacts before queuing. Independent artifact/semantic checks follow completion; neither alone signs off a goal. No figure or public push.
