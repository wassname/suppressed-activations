# Complete-input-prefix semantic outcome review

**Result:** Both J methods still recover Oman and Qatar; neither plain control clearly recovers a country. The new filter removes the observed `continent` extensions, but does not establish full-list cleanliness. Half-erased J has **0/4 confirmed clean joint passes, with an unresolved bound of 0–2/4**; its clean-pair bound is **0–1/2**. Other methods have **0/4 clean joint passes and 0/2 clean pairs**.

This is a fresh, same-family semantic review—not independent replication, neural certification, or goal signoff. Method names and country labels were visible: **the review was nonblinded**.

## Scope and definitions

Read all supplied artifacts completely, including all 16 candidate top-32 lists (512 entries), their original comparison lists, and all four unchanged continuations. Read root `AGENTS.md`, global instructions, and the ML-debug skill. The literal path `rootAGENTS.md` did not exist; root `AGENTS.md` was read instead. No commands, edits, model inference, network, discovery, or delegation were performed.

Artifact root, abbreviated **R** below:

`/workspace/2026/suppressed-activations/out/2026-10-01_093659_jlens-one-pass/`

Roles follow the unchanged geography criterion:

- **Input:** the entire rendered prompt, including instructions, capital name, chat delimiters, and empty thinking block.
- **Hidden identity:** the particular country indicated by that capital—not another country, region, or ambiguous name fragment.
- **Said:** the actual cached continuation, including its terminal token.
- **Clean joint:** clear target identity returned, with full-list input and said exclusion established.
- **Clean pair:** both members meet clean joint and retain the frozen own-country-over-partner rank requirements.

A definite leak defeats cleanliness; an unresolved equivalent prevents confirmation but is not automatically a definite failure. These are semantic annotations, not replacements for frozen lexical scores.

### Unchanged continuations

| Capital → target | Complete cached continuation | Token IDs |
|---|---|---|
| Muscat → Oman | `Asia<|im_end|>` | `[37186, 248046]` |
| Doha → Qatar | `Asia<|im_end|>` | `[37186, 248046]` |
| Windhoek → Namibia | `Africa<|im_end|>` | `[71090, 248046]` |
| Gaborone → Botswana | `Africa<|im_end|>` | `[71090, 248046]` |

All four answer correctly and obey the requested answer format. They are four reused trajectories, not 16 independent generations. `<think>` is in the input, not these continuations.

## Candidate annotations

All methods below include `end-pass input-prefix`. **J½** means `erased0.5 J-lens`; **P24½/P27½** mean equally processed half-erased plain controls; **J-mask** means `J-lens` without half-erasure.

Positions marked `#` are one-based list positions, not strictly-greater-score ranks. “None definite” is not a cleanliness certificate. Evidence is in **R/case_comparison.md**, corroborated by the corresponding `method`, `concept`, and `top32` records in **R/readout.json**.

| Case | Method | Clear identity | Definite input leak | Definite said leak | Ambiguity / clean-joint status |
|---|---|---|---|---|---|
| Oman | J½ | ` Oman` #6 | None definite | None definite | `大陆` #10; ` Oce`, ` Euras` fragments. **Unresolved** |
| Oman | P24½ | None | None definite | None definite | `大陆` #12; `祖国` homeland; ` 동아`, ` premi`, `inį`, ` vaid` ambiguous/incomplete. **No identity** |
| Oman | P27½ | None | `<think>` #15 | `亚洲` #4 | ` آسی`, ` Oce`, ` Euras`, ` Antar`, letter fragments. **Fails** |
| Oman | J-mask | ` Oman` #9 | None definite | `亚洲` #8 | `大陆` #14; ` Oce`, ` Euras`. **Fails** |
| Qatar | J½ | ` Qatar` #5 | None definite | None definite | `大陆` #10; ` Oce`, ` Scandin`. **Unresolved** |
| Qatar | P24½ | None | None definite | None definite | `خلي`, ` Oce`, ` specif`, `IRTH`, `влека`, `inį` incomplete/polysemous. **No identity** |
| Qatar | P27½ | None | `<think>` #24 | `亚洲` #2 | ` châu`, `ทวี`, ` آسی`, ` Oce`, ` Euras`, ` Antar`. **Fails** |
| Qatar | J-mask | ` Qatar` #8 | None definite | `亚洲` #10 | `大陆` #16; ` Scandin`, ` Oce`, ` Euras`. **Fails** |
| Namibia | J½ | None | None definite | `非洲` #10; ` Afrika` #17 | `大陆` #4; regional associations do not identify Namibia. **Fails** |
| Namibia | P24½ | None | None definite | None definite | `大陆` #9; ` Bunda`, ` Lâm`, `xia`, `IRTH` do not establish Namibia. **No identity** |
| Namibia | P27½ | None | `<think>` #32 | `非洲` #1; ` Afrika` #2; ` África` #6; `Afrique` #15; ` Afrique` #25 | `洲`, `大陆`, ` châu`, ` kont`, ` конт`, ` Афри`, `AF`, ` Af`, `Af`, `ทวี`, ` 남아`, `�`. **Fails** |
| Namibia | J-mask | None | None definite | `非洲` #3; ` África` #8; ` Afrika` #10; ` Afrique` #15; `Afrique` #29 | `大陆` #9; `frica` #18 is an Africa fragment. **Fails** |
| Botswana | J½ | None | None definite | `非洲` #8; ` Afrika` #30 | `大陆` #6; other countries are not Botswana. **Fails** |
| Botswana | P24½ | None | None definite | None definite | `大陆` #32; ` Bunda`, `ardia`, `itic`, `xia`, `خلي`, `IRTH` do not establish Botswana. **No identity** |
| Botswana | P27½ | None | `<think>` #29 | `非洲` #1; ` Afrika` #4; ` África` #6; `Afrique` #13; ` Afrique` #28 | `洲`, `大陆`, ` châu`, Cyrillic/Latin fragments, `_CONT`, `,A`, ` Rhodes`, `�`. **Fails** |
| Botswana | J-mask | None | None definite | `非洲` #3; ` África` #8; ` Afrika` #10; ` Afrique` #19; `Afrique` #24 | `大陆` #14; `frica` #30. **Fails** |

Unlisted entries were inspected; none supplies another clear target identity or definite input/said equivalent in this review. This does not certify every multilingual fragment.

### `大陆` in context

The exact token `大陆` can mean **continent**, but also **mainland**, including mainland China. In these continent questions, especially the J lists dominated by geographic names, the continent reading is plausible input-equivalent evidence. The mainland reading remains viable: these are ranked isolated tokens, not a disambiguating sentence. Plain24's mixed lists provide still less contextual resolution.

Accordingly, I retain `大陆` as **unresolved input-equivalent evidence**, consistently across methods. It is not automatically an equivalent of the particular answer Asia or Africa. This preserves the prior review's ambiguity treatment without turning the removal of English `continental` into certified cleanliness.

Similarly:

- `洲` and ` châu` have continent-related but context-sensitive readings.
- `南非` denotes South Africa, not Namibia/Botswana or the whole continent Africa.
- Arabia, Arabian, Asian subregions, Sahara, and `-Saharan` are relationships or regions—not automatically synonyms of the actual continent answer.
- `<|endoftext|>` in African J½ lists is not the observed `<|im_end|>` terminal token. I do not equate them merely because both are special tokens.

## Separate outcomes and bounds

Frozen lexical values below come from **R/paired_summary.json**. Bounds describe these saved lists under unresolved annotation—not statistical confidence intervals.

| Method | Clear country identity /4 | Frozen lexical joint /4 | Confirmed full-list clean joint /4 | Clean-joint bound /4 | Lexical same-answer pairs /2 | Confirmed clean pairs /2 | Clean-pair bound /2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| J½ | 2/4 | 2/4 | 0/4 | 0–2/4 | 1/2 | 0/2 | 0–1/2 |
| P24½ | 0/4 | 0/4 | 0/4 | 0/4 | 0/2 | 0/2 | 0/2 |
| P27½ | 0/4 | 0/4 | 0/4 | 0/4 | 0/2 | 0/2 | 0/2 |
| J-mask | 2/4 | 2/4 | 0/4 | 0/4 | 1/2 | 0/2 | 0/2 |

The J½ upper bound requires resolving both Asia lists' ambiguities without finding another disqualifying entry. Treating `大陆` as continent would make both definite input-exclusion failures; resolving it as mainland alone would not automatically certify the rest of each list.

Input/said exclusion, separately:

| Method | Lists with definite input leaks /4 | Lists with definite said leaks /4 | Remaining status |
|---|---:|---:|---|
| J½ | 0/4 | 2/4 | Input exclusion unresolved in all four; Asia said exclusion has no definite counterexample |
| P24½ | 0/4 | 0/4 | No definite leaks found; fragment/polysemy uncertainty remains |
| P27½ | 4/4 | 4/4 | Definite failures on both roles |
| J-mask | 0/4 | 4/4 | Input ambiguity remains; said exclusion definitely fails |

### Frozen candidate own/partner ranks

| Method | Oman | Qatar | Namibia | Botswana |
|---|---:|---:|---:|---:|
| J½ | 4/17 | 4/126 | 121361/929 | 759/141804 |
| P24½ | 8813/8257 | 598/41573 | 14477/30660 | 18636/46389 |
| P27½ | 2978/11298 | 1330/89051 | 26324/190 | 116/66898 |
| J-mask | 8/22 | 7/159 | 83426/1628 | 1950/103499 |

Both J methods return each Asia country's identity above its partner. This identity distinction survives the filtering change and is not erased by cleanliness problems. The African ranks concern saved alias pieces, not successful country identification.

## Findings and verification limits

### 1. Narrow lexical repair observed; broader exclusion remains unsupported

**R/input_prefix_exclusions.json** records `" continents"` and `" continental"` with `"originating_words": ["continent"]`. Those extensions disappear from the candidate lists. However, **R/case_comparison.md** still contains the exact input token `"<think>"` in all four P27½ lists, plus the definite output translations listed above.

This contradicts any claim that complete-input-prefix filtering establishes complete input or output exclusion. It does not contradict the stated lexical recipe.

**Disproving check:** an exact rendered-input/token comparison showing `<think>` was not consumed would defeat that specific input-leak finding; the supplied prompt explicitly contains it. Translation adjudication could challenge individual semantic labels, but multiple complete Africa equivalents support the African findings.

### 2. Prefix expansion also excludes unrelated meanings

The new recipe retains the old mask and adds normalized vocabulary strings extending complete input words of length ≥3. It uses no semantic or language model. Observed exclusions include:

- `"the" → " theory"`, `" therapy"`;
- `"capital" → " capitalism"`;
- `"user" → " useRef"`.

These are lexical matches, not semantic equivalents. The preregistered `art→article` counterexample remains relevant; retained legacy `name→nam` masking is also unchanged. `readout.json` continues to list six excluded Namibia variants.

**Uncertainty:** these examples establish overbroad semantic coverage, not that the additional exclusions caused the African misses. Both countries were already missed.

**Disproving check:** surviving-score and mask-membership comparisons could disprove a claim of implementation-induced score change. They cannot make `theory` synonymous with `the`.

### 3. Verification and AUROC do not certify semantic success

**R/verification.json** reports:

> `"rows_checked": 16`, `"old_rows_exact": 72`, `"passed": true`

Its scope explicitly states:

> “tied cutoff membership checked, not CPU/GPU tied ordering; no neural or semantic certification”

This is saved-checker evidence, not a checker execution by this reviewer. **R/pipeline.json** reports zero model forwards and zero new generations.

All four candidate methods retain mean alias AUROC **0.8928571492433548**, eligible **4/4**. Per-case values remain **1, 1, 0.5714285969734192, 1**. The preregistration explains that said negatives are masked to `-inf`; even poorly ranked finite positives can beat them. Thus neither high AUROC nor absent English aliases establishes cleanliness. The data contains no `input_word`; empty `input_hits` is not an exclusion check.

## Original results preserved

Job **2673**, represented by the prior geography review, remains unchanged: J½ and mask-only J had lexical **2/4**, plain controls **0/4**, and all four methods had reviewed clean joint **0/4** and clean pairs **0/2**. Their definite English input leaks supported those original outcomes independently of `大陆`.

This report annotates the **new filter** separately. It does not retrospectively rescore original rows or transfer earlier geography successes to the candidate.

## ML-debug notes and residual risks

- **Configuration/control:** cached final-prefill J24, k32, retained output/input masks; half-erasure except J-mask. Plain controls recover **0/4**, versus J identities **2/4** on these selected cases.
- **Predictions checked:** continent extensions disappear; Asia identities persist; clear African recovery does not appear. These observations fit lexical filtering without improved representations.
- **Null/scale:** no random or shuffled control is supplied for this candidate. AUROC 0.5 is the exchangeable-unmasked-label reference, not an appropriate operative null after these masks. No universal pass threshold is imposed.
- **Training/init/schedule/loss/gradients:** inapplicable to this cached readout change. Neural-state correctness remains outside this review.
- **Competing explanations:** semantic mask undercoverage is directly observed; vocabulary granularity and inherited label masking may contribute to identity misses; numerical defects are constrained by the supplied checker but not independently excluded here. No calibrated causal percentages are available.
- **Cheapest remaining discriminator:** adjudicate the exact ambiguous tokens in the full Asia J½ lists under the unchanged role definitions. A continent reading of `大陆` defeats cleanliness; a mainland reading leaves other entries to review. No such additional adjudication was executed.
- **Generalization:** four deliberately selected development cases form two dependent pairs. No held-out transfer or necessity of a country intermediate is established; direct city-to-continent association remains possible.
- **Cost evidence:** pipeline reports **10.3659 seconds**, **8.0206 GiB** peak allocated, and no new neural calls; no stage breakdown.
- This fresh review is same-family and nonblinded. Independent-family semantic adjudication and neural replication are absent.

**Signed: PI/OpenAI**