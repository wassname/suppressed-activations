# completed2705: semantic review

**Decision:** Do not promote generic subtraction as an improved hidden-identity readout from this run. Preserve it as a completed development comparison while causal work progresses; no tuning, new experiment selection, control promotion, or per-case method selection is warranted here.

Read all 668 lines of `out/2026-10-01_123620_generic-reference-readout/run.md`, including all 120 lists, and the supplied summary, margins, pipeline, console, preregistration, and reference files. Read applicable instructions and ml-debug. This is a same-family, nonblinded manual review, not neural replication. No commands, inference runs, edits, or delegation were performed.

## Three different measurements

“Literal” below means the saved `lexicaljoint` result, not my semantic judgment. Console distinguishes that primary alias-checked result from its separate actual-output lexical-only metric.

“Clear identity” means the list contains an identifiable hidden target, regardless of contamination elsewhere. It does not establish that the model used that intermediate.

“Strict joint” is my conservative whole-list diagnostic: clear identity plus exclusion of identifiable input/actual-said content and conspicuous formatting/task debris. It is **not a universal user completion gate**.

Abbreviations: G=generic reference, R=random reference, E=unchanged erased0.5; J0=unchanged input-prefix J-lens. All rows retain the common end-pass/input-prefix configuration.

| Method | Saved literal /8 | Clear identity /8 | Strict joint /8 |
|---|---:|---:|---:|
| G-J | 3 | 5 | 0 |
| R-J | 2 | 2 | 0 |
| G-plain24 | 0 | 0 | 0 |
| R-plain24 | 0 | 0 | 0 |
| G-plain27 | 3 | 4 | 0 |
| R-plain27 | 1 | 0 confirmed | 0 |
| E-J | 4 | 5 | 0 |
| E-plain24 | 0 | 0 | 0 |
| E-plain27 | 4 | 3 | 0 |
| J0 | 3 | 5 | 0 |

All ten methods have **0/4 confirmed clear identities and 0/4 strict joint** on animals, matching the saved 0/4 literal results. Unknown fragments are unresolved, not proved meaningless.

### Token-level adjudication

Evidence below is from the corresponding case/method headings in `out/2026-10-01_123620_generic-reference-readout/run.md`.

- **December:** G-J, G-plain27, E-J, E-plain27 and J0 contain `" December"` or `"December"`. R-J instead has calendar/season alternatives; R-plain27’s `"_Dec"` alone is not an unambiguous identity. Both plain24 variants lack a clear target. G-J also returns `"月份"` (month), `"..."`; G-plain27 has `"圣诞"` (Christmas, input), `"元旦"` and `"-Jan"`. Identity recovery is not clean separation.
- **Thursday:** G-J, R-J, E-J and J0 explicitly return `" Thursday"`. G-plain27 adds a genuine semantic identity, `"星期四"` (Thursday), despite its false literal result. But it also returns `" terça"`—Portuguese Tuesday in this weekday context—so actual-said exclusion fails. R-plain27’s `" thu"` remains ambiguous; do not promote its literal success to confirmed identity. Neither plain24 list identifies Thursday. **Actual output is Tuesday, not intended Friday**; other weekday names are distractors, not automatically leakage of the actual answer. G-J retains `".week"`/`"_week"` and day-category content; other J lists retain `"事实"`/`" **"`.
- **Autumn:** G-J, G-plain27, E-J, E-plain27 and J0 contain `" autumn"`; no other method clearly identifies it. They also contain `"冬"`, `"冬季"` or `"冬天"`: unambiguous winter equivalents. Thus both plain27 literal successes fail semantic actual-said exclusion. Season names are identities here, but `"季节"` alone is not autumn.
- **Apple:** No method clearly returns apple. Color alternatives dominate J lists; plain lists contain fragments and color/output material. Examples include `"红色"`, `":red"` and `"สีแดง"` (red). Neither “berries” nor color categories identify the poisoned fruit.
- **Violin:** G-J, E-J and J0 explicitly contain `" violin"`. R-J does not. Neither plain24 nor plain27 identifies violin unambiguously: `" viol"`, `"viol"`, `"strings"` and `" viola"` are insufficient or different. G-J includes `"乐器"` (instrument: input and actual-output content), while E-J/J0 contain formatting markers. The saved continuation wrongly says **woodwind**, then ends at `"**Identify the instrument:**"`. Violin remains in /8; nothing after that cap is inferred.
- **Hamlet:** No method clearly returns Hamlet. `" Shakespeare"`/`"莎士比亚"` identify the actual author output, not the hidden play. `"这部剧"`, `"话剧"` and theatrical fragments are generic play-related content.
- **Hydrogen:** No method clearly returns hydrogen. `"液态"`/`" solid"` identify state alternatives, while `"气体"` and `"_gas"` expose actual-answer content in several lists. Category recovery is not element recovery.
- **Triangle:** G-J’s `" triangular"`, G-plain27’s `" triangles"`, R-J/E-J/J0’s `" Triangle"`, and E-plain27’s `"三角形"` are clear identity evidence. Both plain24 methods and R-plain27 lack it. G-plain27 additionally contains `"叁"` and `" สาม"` (three), defeating actual-said exclusion. Other identity-bearing lists retain `"**"`, answer-template material, or `"<think>"`.

For **horse, cow, cat and goat**, generic J mostly returns numbers; random J returns numbers plus `"humans"`/`"mammals"`; plain24 returns fragments; plain27 returns parity, formatting and unrelated vocabulary. This applies symmetrically to unchanged controls. `"quine"`, `"trots"`, `"驮"` and `"农牧"` are not sufficient target identities. Horse explicitly appears in its saved output—`"The animal is a horse"`—and remains in /4.

## Paired changes, not selected winners

Against each unchanged E counterpart, saved literal changes on /8 are:

- G-J: +0/−1, losing violin.
- R-J: +0/−2, losing December and violin.
- G-plain24 and R-plain24: +0/−0.
- G-plain27: +0/−1, losing violin.
- R-plain27: +1/−4; gains Thursday, loses December, autumn, violin and triangle.

For confirmed **identity presence**, G-J changes +0/−0; R-J +0/−3 (December, autumn, violin); both plain24 variants +0/−0; G-plain27 +1/−0 (translated Thursday); R-plain27 +0/−3 (December, autumn, triangle). These are not clean-joint gains. Strict-joint changes are +0/−0 throughout. On /4, all three measurements have +0/−0 for every candidate.

## Limits and research interpretation

`pipeline.json` reports `"generic_forward_calls": 1`, `"case_forward_calls": 0`, exact old-row counts 176+88, 47.03 seconds and 8.02 GiB peak. This attests to cached comparison, not independent reproduction.

`animal_margins.json` reports positive D values, yet generic plain27’s cat/goat reversal has own margins only `0.03125, 0.38134765625`; random plain27 reverses both pairs. No returned animal identity accompanies these diagnostics. Animal AUROC uses /3, not /4; near-0.996 plain/random values do not overturn missing identities.

Competing explanations remain shared-signal removal, reference-dependent vocabulary shifts, and scoring coverage limitations; implementation error is untested here. A separate blinded adjudication of the quoted translations/fragments could change semantic counts. Source/numerical reconstruction, seed spread and held-out generalization are outside this review. Norms match **before projection only**; no orientation-only causal attribution follows.

— PI/OpenAI