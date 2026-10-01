# 2720 boundary readout: result and next action

— PI/OpenAI; independent, same-family static review.

**Result:** the boundary exposes apple, but does not consistently improve hidden-identity recovery or separate thought from speech. **Next action:** one bounded cached output-representation audit, before considering endpoint aggregation. Supervisor agreed after dialogue; nothing was executed or changed.

## Evidence and interpretation

Read AGENTS.md, goals/user voice, ml-debug, the preregistration, pipeline metadata, all 288 console lines—including all 72 lists and six complete continuations—and the complete linked run.md.

Sources:
- `slop/audits/2026-10-01_boundary-readout-preregistration.md`
- `out/2026-10-01_160911_boundary-readout/{pipeline.json,run.md,console-clean.log}`
- `out/2026-10-01_160913_jlens-one-pass/run.md`

In the console’s Cases 0–5:

- **December → January:** both J heads and half-plain27 contain complete December identities at final and boundary; plain24 does not. Boundary mask-only J begins `' December', '月份', ' February'`: recovery improves in rank, but broad month coverage remains. `月份` also preserves input meaning despite lexical masking.
- **Thursday → Tuesday:** both J heads recover Thursday at both endpoints; neither plain head does. This is genuinely the wrong generated answer: `'Tuesday<|im_end|>'`, not Friday. Friday in several lists is an expected-answer candidate, not leakage of the actual continuation. Broad weekday coverage weakens claims of selective identification.
- **autumn → winter:** final J heads and half-plain27 contain autumn. Boundary mask-only J retains `' autumn'`; boundary half-J loses it entirely. Boundary half-plain27 retains autumn/fall. Final J lists contain `'冬季', '冬天'`; boundary mask-only J contains `'冬季', '冬'`. Final half-plain27 contains `'冬'`. These are observed winter-equivalent output leaks, not merely unrelated list noise.
- **apple → red:** both boundary J heads and half-plain27 newly recover complete apple; plain24 still does not. Half-plain27 begins `' apple', '苹果', ' apples'`, so this is not J-specific. Final lists contain `':red'`, and several contain `'红色'`; boundary lists instead retain input-related poison words such as `' poisonous'` and `' poisoning'`. Apple is real recovery, alongside category alternatives—not proof that it mediated the answer.
- **Wolke → nuage:** all four heads contain complete cloud at both endpoints, although boundary J is dominated by translation vocabulary. Nuage remains canonically unscoreable; visible absence cannot repair this denominator.
- **nuage → Wolke:** all final heads recover cloud. Every boundary head loses it and returns language/translation vocabulary; boundary J begins `'法语', ' French', 'French', '德语'`. These include input-language equivalents, not hidden cloud identity. English cloud is the intended translation-role target, not disqualified simply because it means the same thing as Wolke.

All 24 preclue lists lack the intended identities: J gives punctuation; plain heads mostly fragments/numbers. This is useful negative evidence, but masks and output-erasure directions use later information, so it is not an independent early causal control.

## Metrics and limits

The master table reports English lexical joint **2/4 → 3/4** for half-J, mask-only J and half-plain27; plain24 remains **0/4**. Translation changes **1/2 → 0/2**, with **one unscored case retained**.

The linked aggregate table reports alias-checked **3/6 at both endpoints** for those three stronger heads. Its expected-answer subset remains **2/5 for J heads and 3/5 for half-plain27**; that denominator excludes the wrong Tuesday response but retains unscoreable nuage. These lexical figures are not semantic-success rates.

Preclue plain AUROC **0.955 despite 0/6 joint** directly illustrates masked-negative inflation. No empirical shuffled/category baseline, seed spread, unseen evaluation or independent score reconstruction was supplied. Training/init/loss diagnostics are inapplicable. Pipeline metadata reports 15 forwards/tokens, 11.42 seconds and 8.11 GiB—not independently rerun.

## Why audit before max

The proposed rule—per-token maximum log-probability over **only closed-user and generation-prefix endpoints**, with four heads/k32/masks fixed—is a legitimate **new method**, neither all-position pooling2637 nor per-case winner selection.

It could combine complementary identities. However, fixed-k max is not a guaranteed union and has no mechanism excluding endpoint-specific speech/input leaks. Apple’s final `:red/红色` and autumn’s winter equivalents could return; common-category coverage could improve lexical scores without better separation.

**Single next action:** parent audits existing cached scores for the already-observed leaks at both endpoints, tracing normalization, mask membership and pre/post-erasure scores. If leaks survive masking and erasure while complete identities remain recoverable, that supports a targeted representation/suppression change rather than aggregation. If apparent leaks are normalization/reporting artifacts, correct that diagnosis first. Cached score reconstruction could disprove the suspected mechanism.

No new inference, labels, masks, method implementation or v5 use. No J-superiority, universal whole-list purity or necessity gate is imposed. Both research goals remain open.