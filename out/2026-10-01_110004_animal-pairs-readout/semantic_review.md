# Animal-pairs semantic review — 2694

**Result:** All four answers contain the correct number, but only three leave the target identity unsaid. No method clearly returns a target identity in its top-32 lists: lexical joint and strict full-list semantic joint are both **0/4 per method**. Unmasked scores show partial cue-dependent discrimination, not preference reversals or selective hidden-thought recovery.

Same-family artifact review; not goal approval, independent-family adjudication, or neural replication.

## Scope and observed outputs

Read completely: both supplied AGENTS.md files, ML-debug skill, preregistration, prior native-v4 review, and:

- **M:** `/workspace/2026/suppressed-activations/out/2026-10-01_110004_animal-pairs-readout/` — `run.md`, `pipeline.json`, `pair_metrics.json`, `labels.json`.
- **T:** `/workspace/2026/suppressed-activations/out/2026-10-01_110004_jlens-one-pass/generation_traces.json`.

Inspected all 16 complete top-32 lists in **M/run.md**, totaling 512 entries. Only the opening of the duplicate replay `out/2026-10-01_110021_jlens-one-pass/readout.json` was read; no claim of complete replay-record verification.

| Case | Saved continuation | Tokens | Correct number | Identity unsaid |
|---|---|---:|---|---|
| horse | Full quotation below | 32, capped; no EOS | Yes | **No** |
| cow | `four<|im_end|>` | 2 | Yes | Yes |
| cat | `four<|im_end|>` | 2 | Yes | Yes |
| goat | `four<|im_end|>` | 2 | Yes | Yes |

Horse, verbatim:

> The number of legs on the animal that neighs and is ridden using a saddle is **four**.
>
> (The animal is a horse, which has four legs.)

Thus factual correctness is 4/4; missing-phrase-only compliance is 3/4. “Hidden-not-said” eligibility is 3/4, **not evidence that these identities were necessary internal computations**. Horse remains in every all-case denominator.

Of the two preregistered pairs, only cat/goat has identical complete scoring text (`four`): **1/2**. Horse/cow shares the numerical answer but not the complete answer.

## Symmetric full-list review

J½ denotes half-erased J-lens; P24½/P27½ are matched plain controls; J is mask-only J-lens. Every row below represents a complete inspected list. **None contains a clear target identity.**

| Case | Method | Decisive evidence and distinctions |
|---|---|---|
| horse | J½ | `事实` = input “fact”; ` Four` = said answer; ` **` = said formatting. `Dogs`, `mammals` are not horse. |
| horse | P24½ | `_fact`, `事实`, `的事实`; `zahl`, `总数` concern number/count. `trots` is a gait, not identity. |
| horse | P27½ | `事实`; `trots`, `驮` concern movement/carrying, not an unambiguous horse. |
| horse | J | `事实`, ` Four`, ` **`; other numbers and `Dogs` do not recover horse. |
| cow | J½ | `事实`, `的事实`, `:number`; answer/discourse vocabulary dominates. |
| cow | P24½ | `事实`, `_fact`, `zahl`, `:number`; `pupper` is dog-related, not cow. |
| cow | P27½ | `事实`, exact input `<think>`; `农牧` is farming/pastoral context, not cow. |
| cow | J | `事实`, `:number`; alternative numbers are not the actual answer four. |
| cat | J½ | `Count`, `mammals`, `Dogs`: number/category associations, not cat. |
| cat | P24½ | `_fact`, `事实`, `zahl`, `总数`; fragments and unrelated names do not identify cat. |
| cat | P27½ | `偶`, `odd`, `pairs` concern parity/grouping; `pupper` is not cat. |
| cat | J | Predominantly alternative numbers and formatting; no clear cat. |
| goat | J½ | `事实`, exact input `<think>`; answer/number framing, no goat. |
| goat | P24½ | `事实`, `_fact`, `zahl`, `总数`; `trots` is not goat identity. |
| goat | P27½ | Exact input `<think>`; parity terms and boilerplate, no goat. |
| goat | J | Alternative numbers, answer terms and formatting; no goat. |

`Answer`/`答案` are discourse terms, not words actually emitted by the three bare-answer cases. Markdown-like tokens are not automatically said contamination for those cases. Multilingual fragments and boilerplate remain uncertain/noisy, not positive identity evidence.

For **each method**: clear identity **0/4**, reported lexical joint **0/4**, strict semantic joint **0/4**; on the three identity-unsaid cases, all are **0/3**. Strict failure already follows from missing clear identity, without needing to certify every fragment’s exclusion.

## Unmasked margins and arithmetic

From **M/pair_metrics.json**; own margins are own-minus-partner. D equals their sum.

| Method | Pair | Own a | Own b | D |
|---|---|---:|---:|---:|
| J½ | horse/cow | 2.90625 | −1.28125 | 1.625 |
| J½ | cat/goat | 1.9375 | −1.625 | 0.3125 |
| P24½ | horse/cow | 1.7109375 | −1.421875 | 0.2890625 |
| P24½ | cat/goat | 0.7578125 | −0.953125 | −0.1953125 |
| P27½ | horse/cow | 1.875 | −0.4375 | 1.4375 |
| P27½ | cat/goat | 0.84375 | −0.4140625 | 0.4296875 |
| J | horse/cow | 2.78125 | −1.59375 | 1.1875 |
| J | cat/goat | 1.96875 | −1.6875 | 0.28125 |

All methods prefer horse over cow on both prompts and cat over goat on both prompts: **0/2 reversals each**.

Manual subtraction agrees with saved scores and reported rounding. Primary-minus-control D, horse/cow then cat/goat:

- P24½: **1.3359375, 0.5078125**
- P27½: **0.1875, −0.1171875**
- J: **0.4375, 0.03125**

The four assignment-null means also agree arithmetically: J½ ±0.96875/±0.65625; P24½ ±0.046875/±0.2421875; P27½ ±0.93359375/±0.50390625; J ±0.734375/±0.453125. These are descriptive swaps, not powered significance tests.

## Bounded implication and residual uncertainty

**Observed:** positive J½ D persists on the genuine same-complete-answer cat/goat pair, but P27½ has larger D there. High alias AUROCs coexist with zero returned identities; ranking selected aliases is not top-k recovery.

**Interpretation:** the scores support partial context sensitivity with persistent label preference. They establish neither purity nor necessity. Maximum-over-variants bias, direct cue association, and implementation/state-selection errors remain competing explanations.

**Disproving checks:** challenge specific semantic annotations against complete lists; independently recompute saved score differences and capture/replay parity. Stronger identity discrimination would require own-preference reversals on fixed same-complete-answer cases. No new mask/layer/k rescue follows.

ML-debug limits: frozen evaluation, so training/init/loss/schedule checks are inapplicable. Trace counts give **32+2+2+2=38**, matching reported forwards; zero cached forwards, 72 exact legacy rows, and 16 candidates are reported, not independently executed. Pipeline reports 25.72 seconds and 8.079 GiB. No commands, edits, model inference, delegation, or network were performed.

**Signed: PI/OpenAI**