# Next readout attempt: distinguish people, without another subtraction variant

— PI/OpenAI. Prospective design only; no new inference, dataset, method implementation or queued readout job. Job2706 remains the active causal attempt.

## Why not immediately change the erasure direction?

Current half-erasure is applied to the normalized intermediate decoder state z using the original final-prefill greedy token's embedding w:

`z_out = z - 0.5 * dot(z,w)/dot(w,w) * w`

Replacing w by the normalized final residual f initially looked like a different way to remove speech-related content. But it is:

`z_out = z - alpha(z,f) * f`, with `alpha = 0.5 * dot(z,f)/dot(f,f)`.

Before casting and a linear head, this is a current-alignment-dependent version of the signed-logit subtraction already tried in2621. It differs from fixed subtraction and token-row erasure, but not enough to justify treating it as an unrelated discovery. It could remove hidden concepts that remain represented at the final layer. I will not automatically run it as a coefficient rescue. This algebra does not prove all such projections fail.

Observed code: `scripts/english/08_jlens_one_pass.py:1282–1309`; old signed-subtraction test: `slop/audits/2026-09-30_logit-contrast-check.py`. Generic subtraction2705 retained5/8 primary identities and returned no animal identities. Its plain27 translatedThursday gain remains a limited control result, not a new primary.

## A smaller goal-directed option

Test the unchanged2686 J24/half-erasure/mask1/k32/input-prefix method on four person-bridge prompts. A person's name differs from the previously successful country names and from the animal leg-count class, where four can be guessed without identifying the animal. Compare the same frozen plain24/plain27 and mask-only J controls; do not use2705's generic subtraction.

Reuse `data/twohop/TwoHopFact.csv`, SHA256 `522d3764eba5c297f9fc630073ce5e897eac134e1d04824fed4d5349e605e338`, CC-BY-4.0. The original repository entrypoint06 already uses this corpus. Prior1027 attempts did not save every rejected output, so these cannot be certified unseen concepts or previously unqueried source rows. Native-chat prompt instances would be new; claim development evidence only.

Selection was made from corpus facts, not model outputs: in file order, take the first two birth-country groups in `novel-author-birthcntry` containing at least two distinct authors; take each group's first two distinct authors. This gives:

| CSV row (zero-based) | UID | Book | Hidden person | Present-day country |
|---:|---:|---|---|---|
|3379|27160|Nineteen Eighty-Four|George Orwell|India|
|3406|27187|The Satanic Verses|Salman Rushdie|India|
|3381|27162|Dream of the Red Chamber|Cao Xueqin|China|
|3395|27176|Journey to the West|Wu Cheng'en|China|

This differs from the initial idea of hand-selecting Orwell/Kipling and Einstein/Planck. The deterministic corpus rule instead yields Rushdie and the two Chinese authors. Preserve this selection history.

The corpus labels the latter country `People's Republic of China`, which did not exist when those authors were born. A uniform present-day-country instruction is necessary; otherwise the benchmark wording itself is anachronistic. Wu Cheng'en is the traditional attribution for Journey to the West, not an undisputed historical identification. These limitations stay with the cases.

Proposed user content, same rule for all four:

`Complete the fact with only the missing country name. Use present-day country names:\nFact: ` + the exact CSV `r2(r1(e1)).prompt`.

Native template, thinking disabled, tokenizer/model EOS union, maximum32 generated tokens; no replacement or extension after seeing outputs. One generation per input; existing08 captures states in that pass and later scores cached states with forward rejection. No first-hop knowledge-filter pass. Labels, country aliases and paired-author comparisons are evaluation-only. Reuse08, not a new inference pipeline.

## What would count as progress?

Report each full returned list and actual continuation. A useful result identifies the specific unspoken person while excluding the input and actual answer; retain partial identity evidence when exclusions fail. Strict whole-list purity remains diagnostic, not a newly imposed user threshold. Names/fragments/transliterations need semantic review; tokenization failures remain explicit nonpasses, not grounds to replace a case.

Within each same-country pair, compare own versus partner identity membership/ranking before and after masks. If both lists simply contain both authors, that is weak selectivity. If outputs differ, keep the cases but do not call the pair an identical-output control. High margins without returned identities are not recovery. No pair-rate significance claim from two pairs.

Remaining alternative: a book's country associations may let the model answer without computing the author. Returned cue-specific names would demonstrate information in the readout, not causal necessity. This test cannot settle that distinction.

Prediction before implementation: likely some author identity signal, with residual input/said content; plausible wrong or overlong Base answers. A clean primary gain outside country identities would motivate a genuinely fresh frozen evaluation, not immediate goal completion. Continued absence of identities would argue against another ranking-only repair on these cases.

Next dependency: inspect2706's actual causal outputs when its native completion arrives, then settle this bounded readout test. No production source, queued payload, mask, dose, layer, k or reservedv5 has changed.
