# Native-chat v4 semantic outcome review

**Result:** Both J methods clearly return 5/8 target identities; plain27 returns 3/8, with an additional ambiguous `viol` fragment; plain24 returns 0/8. **All four methods have 0/8 full-list clean joint passes under the previous role definitions.** This does not erase the identity recoveries. Nor does the lexical 4/8 tie establish equal semantic performance.

Same-family, nonblinded artifact review—not neural replication, independent-family adjudication, or goal signoff.

## Scope and criterion

Read the supplied instructions, ML-debug skill, previous role-definition review, complete master report/configuration artifacts, dataset, rendering and generation traces, and all **32 complete candidate records/top-32 lists**: 1,024 entries across four methods and eight cases. The much larger `readout.json` also contains legacy methods; those were not exhaustively reviewed and cannot become selected primaries here.

No commands, edits, inference runs, network, discovery, or delegation were performed.

Paths below use these abbreviations:

- **M:** `/workspace/2026/suppressed-activations/out/2026-10-01_102214_native-v4-readout/`
- **R:** `/workspace/2026/suppressed-activations/out/2026-10-01_102255_jlens-one-pass/readout.json`
- **T:** `/workspace/2026/suppressed-activations/out/2026-10-01_102219_jlens-one-pass/`

Preserving `slop/reviews/2026-10-01_input-prefix-result-review.md`:

- **Input:** entire rendered prompt, including instructions and thinking scaffold.
- **Hidden identity:** the particular target concept, not merely its semantic neighborhood.
- **Said:** actual saved capped continuation, including formatting and terminal tokens.
- **Clean joint:** clear hidden identity plus full-list input and said exclusion.
- Definite contamination defeats cleanliness; ambiguity prevents confirmation without automatically proving contamination.

I report formatting separately from semantic word equivalents, but do **not** silently remove formatting from the previous full-list criterion. Arbitrary punctuation overlap alone is not treated as a substantive finding; the violin formatting overlap is specifically the same Markdown emphasis used in the saved answer.

## All eight observed outputs

These are **eight shared scientific cases/trajectories, not eight new generations per readout method**.

| Case | Expected completion | Complete capped continuation | Tokens; outcome |
|---|---|---|---|
| December | January | `January<|im_end|>` | 2; correct |
| Thursday | Friday | `Tuesday<|im_end|>` | 2; wrong |
| autumn | winter | `winter<|im_end|>` | 2; correct |
| apple | red | `red<|im_end|>` | 2; correct |
| violin | strings | See verbatim block below | 32; wrong, capped without EOS |
| Hamlet | Shakespeare | `William Shakespeare<|im_end|>` | 3; correct |
| hydrogen | gas | `gas<|im_end|>` | 2; correct |
| triangle | 3 | `three<|im_end|>` | 2; correct |

Complete violin continuation:

```text
The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.

**Reasoning:**
1.  **Identify the instrument:**
```

Source: **T/generation_traces.json**, cases 0–7. Seven stop on EOS; violin does not. These counts total 47 tokens, consistent with **M/pipeline.json**.

The violin output actually affirms **woodwind**. It does not affirm strings, identify the instrument as violin, or provide the promised reasoning within the cap. Nothing after the cap can be inferred. Likewise, Thursday's actual answer is Tuesday, not the intended Friday.

## Symmetric candidate review

All method names below include `end-pass input-prefix`:

- **J½:** `erased0.5 J-lens`
- **P24½/P27½:** half-erased plain controls
- **J:** J-lens without half-erasure

Positions are one-based list positions, not score ranks. Each row covers one complete inspected list. The evidence column records decisive contamination and relevant ambiguities; related alternatives are not automatically synonyms.

| Case | Method | Clear identity | Input-equivalent evidence | Actual-said evidence / ambiguity |
|---|---|---|---|---|
| December | J½ | `December` #14 | `事实` = fact; `-month` | No definite January equivalent |
| December | P24½ | None | `_fact`, `事实`, `事實`, `факт`, `Fakta`/`fakta`; `…the` | No definite January equivalent |
| December | P27½ | `December` #11, #26 | `事实`, `事實`, `Fakta`, `факта` | `元旦` is New Year's Day, **not** January |
| December | J | `December` #2, #29 | `事实`, `-month`, `/month` | No definite January equivalent |
| Thursday | J½ | `Thursday` #11 | `事实` | Friday #4 is intended but **unsaid**; no definite Tuesday equivalent |
| Thursday | P24½ | None | `_fact`, `事实`, `的事实`, `факт`, `사실`, `Fakten`, `fatos` | No definite Tuesday equivalent |
| Thursday | P27½ | None | `事实`; `요일` is day-of-week language | Friday #16/#21 is unsaid; `fr`, `금`, `جم`, `sund` remain fragment/polysemy concerns |
| Thursday | J | `Thursday` #5 | `事实` | Friday #3 and `Fridays` #29 are unsaid; no definite Tuesday equivalent |
| autumn | J½ | `autumn` #22 | `事实`, `-season` | `冬季`, `冬天`, `寒冬` return winter |
| autumn | P24½ | None | `_fact`, `事实`, `fakta`, `факта`, `fatos`, `사실을` | No definite winter equivalent; incomplete `temper`, `наступ` |
| autumn | P27½ | `autumn` #26; `fall` #32 in seasonal context | `ฤดู` = season | `冬` = winter; `zim` incomplete/ambiguous |
| autumn | J | `autumn` #13, `Autumn` #26 | `-season`, `_season` | `冬季`, `冬天`, `寒冬`, `冬天的`, `冬`, `vinter`; `зим` fragment |
| apple | J½ | None | `的颜色` = color | `红色`, `红色的`, `:red`; crimson is a narrower red term, not needed for verdict |
| apple | P24½ | None | `สี` = color; `setBackgroundColor` is compound/programming contamination | `:red`; `红了` context-dependent; `imson`, `uby`, `мали` incomplete |
| apple | P27½ | None | `五颜六色的` is color-related, not an exact substitute for “color”; `struments` is incomplete | `:red`, `_red`, `红色`, `通红`, `สีแดง`, `الأحمر`; `крас` incomplete |
| apple | J | None | No definite input-word equivalent identified | `红色`, `红色的`, `:red`, `_red`, `-red`, `(red`, `rouge` |
| violin | J½ | `violin` #22 | No definite semantic input-word equivalent identified | Exact said markup ` **` #5; no clear complete woodwind equivalent |
| violin | P24½ | None | `的事实`, `事实`, `факта`, `fapt` | No definite complete woodwind equivalent |
| violin | P27½ | **Ambiguous** `viol` #31 | `struments` fragment of instrument, not a complete equivalent | Exact emitted piece `wind` #1; wind-family terms overlap woodwind category but are not exact synonyms; strings are **unsaid** |
| violin | J | `violin` #19 | No definite semantic input-word equivalent identified | Said markup ` **` #3, `**` #8; `Wood` #28 is ambiguous rather than a full woodwind equivalent |
| Hamlet | J½ | None | No definite input-word equivalent identified | `Shakespeare` #1, `莎士比亚` #25; `akespeare` fragment |
| Hamlet | P24½ | None | `onstage`, `tragedia`, `-fiction` are related, not exact play equivalents | `akespeare` #1 is strong name-fragment evidence, not a complete name |
| Hamlet | P27½ | None | `-play`, `这部剧`, `该剧`, `话剧`; theater words may be broader | `Shakespeare` #4, `莎士比亚` #5; `Shakespe`, `akespeare` fragments |
| Hamlet | J | None | No definite input-word equivalent identified | `Shakespeare` #1, `莎士比亚` #22; `akespeare` fragment |
| hydrogen | J½ | None | No definite input-word equivalent identified | `vapor`/`Vapor` are gas-related but not unqualified synonyms of hydrogen's state; fluid includes liquids |
| hydrogen | P24½ | None | `常温` = room/ordinary temperature | No definite gas equivalent |
| hydrogen | P27½ | None | State alternatives are not automatically equivalents of the word “state” | `气体`, `气体的`, `的气体`, `газ`, `газа`, `gaz`, `_gas`, `گاز`, `غاز`, `الغاز`, `gás`, `газов`; `气`, `газо`, `gaze` context-sensitive |
| hydrogen | J | None | No definite input-word equivalent identified | Same vapor/fluid distinction as J½ |
| triangle | J½ | `Triangle` #23 | `事实`, `的事实`, `Fakt`, `fakta` | No definite three equivalent |
| triangle | P24½ | None | `事实`, `_fact`, `的事实`, `Fakten`; `zahl` = number | No definite three equivalent; exact **input markup** `<think>` #10 |
| triangle | P27½ | `triangles` #2, `_triangle` #16, `三角形` #25, `三角形的` #31 | `事实`; exact **input markup** `<think>` #1 | `thirds` is not the cardinal answer three; `ilateral` incomplete |
| triangle | J | `Triangle` #21 | `事实`, `的事实`, `Fakt`, `fakta`, `Fakta` | No definite three equivalent |

**R candidate-record locations:** December lines 2686–3276; Thursday 5981–6575; autumn 9313–9911; apple 12647–13245; violin 16786–17568; Hamlet 20329–20940; hydrogen 23668–24266; triangle 27009–27612.

### Formatting and discourse contamination

These are separate from semantic equivalents:

- Markdown-like `**`, `…**`, `...**`, punctuation wrappers and ellipses occur broadly, especially in J lists. They are not said-output leaks when the actual continuation is only a bare answer plus EOS.
- They **are** actual-output formatting contamination in the violin J lists, where emphasis is present in the saved output.
- `<think>` in both triangle plain lists is consumed input markup, not generated reasoning.
- `Answer`, `Answers`, `答案`, `答案是`, `正确答案`, `Actually`, `Definitely`, `Based`, and `According` indicate answer/discourse framing. They are not words actually emitted in the triangle continuation.
- `Known`, `Unknown`, `nonexistent`, `Nothing`, `Silent`, and `none` in violin lists are candidates, not model assertions made in the saved continuation.
- Copyright boilerplate (`版权声明`), exam boilerplate (`本题考查`), coding fragments (`.gradle`, `.isFile`, `../../../../`), replacement characters, and incomplete multilingual pieces are noise or unresolved contamination—not evidence of hidden identity.

All remaining entries were inspected. I do not certify every multilingual fragment or promote unrelated names, colors, seasons, instruments, and authors to target synonyms.

## Counts and ambiguity bounds

“Frozen lexical” below means the report's `alias_checked_pass`, not full semantic exclusion and not necessarily the intended-answer `alias_pass`.

| Method | Clear identity /8 | Identity bound /8 | Frozen lexical joint /8 | Full-list clean joint /8 | Clean bound /8 |
|---|---:|---:|---:|---:|---:|
| J½ | 5 | 5–5 | 4 | 0 | 0–0 |
| P24½ | 0 | 0–0 | 0 | 0 | 0–0 |
| P27½ | 3 | 3–4 | 4 | 0 | 0–0 |
| J | 5 | 5–5 | 3 | 0 | 0–0 |

These are annotation bounds on the saved lists, not statistical confidence intervals. P27½'s extra possible identity is `viol`: it could suggest violin, but also a viol or another continuation. It is not clear violin recovery.

The strict clean upper bounds are zero because every clear-identity list has definite input contamination, actual winter contamination, or—in the violin J lists—actual said formatting. Removing formatting from the criterion would create a **different diagnostic**, not revise these counts. Under that word-only diagnostic, the violin J lists merit further scrutiny; `Wood` remains ambiguous for J.

### Expected-answer subset

The correct-output subset is cases **0, 2, 3, 5, 6, 7**, fixed by observed outputs, not selected separately by method.

| Method | Clear identity /6 | Frozen lexical joint /6 | Full-list clean joint /6 |
|---|---:|---:|---:|
| J½ | 3 | 2 | 0 |
| P24½ | 0 | 0 | 0 |
| P27½ | 3 | 3 | 0 |
| J | 3 | 2 | 0 |

Thus both extra clear J identities—Thursday and violin—occur where the baseline answer is wrong. On the correct-output subset, plain27 ties both J methods on clear identity count. Its lexical advantage is not semantic purity: autumn still contains `冬`, and the other identity cases contain input equivalents.

There are no same-answer pairs in this dataset. No pair metric is inferred.

## Selected primary example

**Case 0, December**, is the first original-order case with a clear hidden concept in the preregistered primary J½ list. Selection does not require a clean list or a top-one identity.

Input, exactly as rendered:

```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Primary top-32:

```text
[' **', ' Calendar', ' Year', ' Next', '事实', ' ...', '...', '次年', ' calendar', ' Tomorrow', ' Leap', '**', ' February', ' December', ' Future', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', '…', ' weeks', '(next', 'Calendar', ' Summer', '-month', ' Seasons', ' Holidays', ' Season', ' year']
```

Actual output:

```text
January<|im_end|>
```

Disclosure: December is #14, not the dominant candidate. `事实` repeats input “fact”; `-month` repeats input “month.” Markdown/ellipsis contamination is present. Calendar/year/next-year and seasonal alternatives are associated concepts, not automatically January equivalents. No definite January equivalent appears. The matched P27½ control also clearly returns December; this example is not J-exclusive.

## Findings and implications

### 1. Lexical joint is not full-list semantic success

**Observed:** **M/summary.json** reports lexical `4/8, 0/8, 4/8, 3/8`. Yet **R**, autumn P27½, has:

> `"alias_checked_pass": true`

and its top-32 includes:

> `"冬"`

That is winter, the actual answer. December and triangle identity lists also contain `事实`, an input equivalent.

**Affected:** all claimed clean-success interpretations of the lexical table.

**Disproving check:** challenge the individual translation/role annotations against the exact rendered input and continuation. Merely confirming the frozen alias implementation would not disprove semantic undercoverage.

### 2. Wrong outputs alter what “said excluded” means

**Observed:** Thursday J½ has:

> `"scoring_text": "Tuesday"`  
> `"answer": "Friday"`  
> `"alias_checked_pass": true`  
> `"alias_pass": false`

Friday remains #4, but is unsaid. Violin P27½ has:

> `"best_hidden_token": " viol"`  
> `"emitted_word_piece_hits": ["wind"]`

while its lexical joint is true. J's `Wood` yields an actual-word hit, but is not itself a complete semantic equivalent of woodwind.

**Inference:** headline differences partly reflect actual-output tokenization and wrong-answer trajectories, not only selective intermediate-concept readout.

**Disproving check:** separately adjudicate actual answer words, intended-but-unsaid answers, complete identities, emitted pieces, and formatting. Do not substitute intended labels for the observed response.

### 3. Concise outputs reduce one confound, but do not establish selective hidden thought

**Observed:** seven outputs are short and EOS-terminated; six are correct. The violin output remains a wrong, verbose, capped continuation. The primary J methods still miss apple, Hamlet, and hydrogen while returning colors, authors, and physical-state alternatives.

**Inference:** broad answer-category association remains a plausible explanation for many readout lists. Clear identity return is partial positive evidence, not proof that the intermediate was necessary or causally used.

The supplied scope does not contain the old v4 traces, so I cannot independently quantify an old-to-new output improvement. The preregistration also warns that both framing and prefix exclusion differ from old completion results; any historical difference is not a pure chat effect.

### 4. Artifact consistency is reported, not independently re-executed

**M/pipeline.json** reports:

> `"actual_forward_calls": 47`  
> `"generated_tokens": 47`  
> `"original_rows_exact": 144`  
> `"candidate_rows": 32`  
> `"rescore_forward_calls": 0`  
> `"goals_completed": false`

Trace lengths support the token count. I did not execute parity checks, verify hashes, inspect tensors, or audit implementation correctness. Empty `input_hits` fields are visibly insufficient semantic evidence.

## ML-debug review notes

| Required check | Evidence / limitation |
|---|---|
| Log/configuration | Entire supplied master report read; J24, final-prefill, k32, half-erasure primary, greedy-one output mask and frozen prefix masks; four matched readouts |
| SHOULD versus observed | Eight trajectories and zero cached forwards reported; 144 old rows exact reported. No independent checker execution |
| Init/training/schedule/loss/gradients | Not applicable: frozen readout evaluation, no training |
| Baselines | Clear identities J½/J 5/8, P27½ 3/8 plus one ambiguity, P24½ 0/8; correct-output subset ties at 3/6 for J and P27½ |
| Null and scale | No shuffled/random control supplied. AUROC 0.5 is only an exchangeable unmasked reference, not a calibrated null for masked scores |
| Full sample | December input, entire readout and exact continuation above; all eight outputs inspected |
| Surprising evidence | P27½ autumn lexical pass despite `冬`: explained by incomplete lexical coverage, not semantic cleanliness |
| Missing trust evidence | Code/tensor audit, independently executed parity checks, blind independent-family annotation, seed spread and untouched concepts |
| Fresh review | This is the requested fresh same-family review. No further reviewer was launched |
| Cost | Pipeline reports 40.9658 s capture, 52.0561 s total and 8.0790 GiB peak allocated; no detailed stage memory breakdown |
| Execution | Read-only review only; no recommended experiment executed or queued |

Subjective explanatory weights—not calibrated causal estimates: **45%** answer-category association rather than selective intermediate representation; **35%** evaluation/tokenization/mask undercoverage; **10%** implementation/state-selection defect; **10%** unknown. These mechanisms can coexist. Category-heavy lists support the first; exact missed translations and `viol` support the second. Reported parity constrains, but does not independently exclude, implementation defects.

Three ways a broad “J wins” conclusion could fail:

1. The correct-output subset already ties P27½ on identity count.
2. Known concepts and visible labels can favor a nonblinded interpretation; untouched matched cases and blind adjudication could reverse it.
3. Masking can improve lexical scores without separating representations; unmasked paired identity margins could fail despite current hits.

Conversely, strict clean 0/8 is not a rejection of the overall idea: a useful identity signal can coexist with generic fact/format directions and incomplete exclusion.

## One recommended representation-level discriminator

**Recommendation only; not executed:** freeze a **same-output, different-hidden-identity transfer test** with the existing J24/k32 representation and matched plain controls unchanged. For example, use two uniformly framed identity-to-color prompts whose different intermediate objects both correctly produce `red`. Fix the cases and analysis before capture.

Measure each method's **own-hidden versus partner-hidden score margin before lexical masking**, then retain the unchanged top-32 semantic review as a separate outcome.

- Identity-sensitive representation predicts margins that reverse with the hidden object while the actual answer stays `red`.
- Answer-category or generic frame association predicts color-heavy lists without reliable own-object separation.
- Preserve wrong outputs in the all-case denominator; report the correct same-output subset separately.

This tests representation selectivity rather than rescuing the current result with another mask, layer, or k. It does not impose an all-cases/all-languages human acceptance gate.

**Signed: PI/OpenAI**