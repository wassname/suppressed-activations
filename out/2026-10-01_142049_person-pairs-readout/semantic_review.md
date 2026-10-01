# Experiment 2716: fresh result review

**Finding:** None of the four frozen methods returns an identifiable own-person or partner-person identity on any case. Thus identity recovery and clean joint recovery are **0/4 per method**, not evidence that person information is absent from the model.

I read all four complete continuations and all sixteen top32 lists (512 entries) in `out/2026-10-01_142049_person-pairs-readout/run.md`, the complete pipeline/pair/verification records, raw capture traces, launcher, and relevant generation/readout/scoring code. No commands, inference, edits, or delegation were performed. Parent diagnostic/recommendation was not consulted.

## Most important findings

### 1. Country alternatives are not hidden-person recovery

The primary lists begin respectively:

> `Russia, Canada, Britain`  
> `Pakistan, England, Nigeria`  
> `Japan, Indonesia, Russia`  
> `Japan, Indonesia, Thailand`

These are overwhelmingly alternative answers/category associations, not Orwell, Rushdie, Cao Xueqin, or Wu Cheng’en. Plain controls instead contain multilingual country terms, fragments, and unrelated tokens. `Nagy`, `-Smith`, `Zhao`, and `Lâm` do not identify the requested authors.

`pair_diagnostics.json` records primary masked own/partner ranks of **308/419, 352/1288, 979/965, 862/1459** (strict-greater counts). Neither class appears in any returned list, before or after masking, for any method. Therefore masking alone does not explain the missing names.

### 2. Only one pair actually has matched outputs

Complete continuations, each two tokens including EOS:

| Case | Exact continuation | Correct? |
|---|---|---|
| Orwell | `England<|im_end|>` | No; expected India |
| Rushdie | `India<|im_end|>` | Yes |
| Cao | `China<|im_end|>` | Yes |
| Wu | `China<|im_end|>` | Yes |

The England/India pair is **not** same-output. Cao/Wu match both complete scoring strings and generated IDs.

All methods’ first pair has positive own margins, but this cannot isolate identity selectivity from different actual answers. For the genuinely matched China pair, **no method reverses preference correctly across both cases**. Primary margins are −0.03125 and +0.71875: Wu’s alias set wins on both. A positive double difference, here 0.6875, is not returned identity or successful two-way discrimination.

Correct country answers also do not establish person-mediated reasoning; title/cultural associations could suffice. No first-hop test was run, appropriately without dropping cases.

### 3. Lexical exclusion and semantic exclusion remain different

Compact classification below covers every case/method. **All cells have no own or partner identity.** HJ = half-erased J; P24/P27 = equally half-erased plain controls; J = mask-only J. “None seen” is not exhaustive certification.

| Case | HJ leakage/association | P24 leakage/association | P27 leakage/association | J leakage/association |
|---|---|---|---|---|
| Orwell | Britain/British/英国: related to actual England, not exact equivalents | Input-related `祖国`, `生的`; template `<think>` | Britain/英国/英伦; template `<think>` | Britain/British/英国; related, not exact England |
| Rushdie | No definite input/India equivalent seen | `Birth`, `OfBirth`, `fictional`, `祖国`; `<think>` | `<think>`; no definite India equivalent seen | No definite input/India equivalent seen |
| Cao | No definite input/China equivalent seen | Input `current`, `今天的`, `现在的`; output `中华人民共和国`, `中国的` | Numerous China equivalents, including `中国`, `中國`, `Китай`, `Chine` | Output `-China`, `Chinese`, `中国` |
| Wu | No definite input/China equivalent seen | Input `祖国`, `现`; output `中华人民共和国`, `中国的` | Output `中国`, `الصين`, `Chine`, plus others | Output `-China` |

Country alternatives are not automatically input leaks merely because the prompt requests a country. Likewise Britain is not literally England. These distinctions do not rescue joint recovery: identities are missing everywhere.

### 4. Metrics can look favorable without recovery

The primary report’s **AUROC 0.8404** coexists with zero recovered identities. In `scripts/english/08_jlens_one_pass.py:1421–1427`, AUROC compares masked hidden/said scores, including negatives driven to −∞. A trivial filter can improve this statistic without recovering a person. Random pair-ranking reference is 0.5, but this masked-label setting is not a useful unfiltered chance comparison.

At `:1153–1155`, `hidden_is_said` checks aliases against individual words; full-name-only aliases remain generally unsafe. Frozen surname aliases mitigate these cases, and no continuation actually spills a name. Wu’s canonical metric is unscorable under the default minimum, while the preregistered two-character alias diagnostic remains available. Do not conflate either with semantic identity.

## Debug disposition and uncertainty

Observed `pipeline.json`: **8 forwards, 8 generated tokens, zero replay forwards, 72 original rows exact**, 24.48 seconds and 8.079 GiB peak. Verification explicitly says:

> “no neural or semantic certification”

The SHOULD expectation of improved joint recovery is not observed: primary and controls all score zero. No executed-path blocker was established by static inspection. Training loss, gradient norms, and learning schedules are inapplicable.

Subjective competing explanations: category-dominated representation at this readout position 60%; scoring/alias limitations 15%; capture/transport implementation defect 10%; unknown 15%. These are not measured probabilities. Complete visible lists weaken an alias-only explanation; saved-score verification weakens, but cannot eliminate, an implementation explanation.

A future independently reproduced capture at the same settings could test implementation parity; a separately declared earlier-position diagnostic could distinguish last-position localization from broader absence. Neither was executed, and neither is a new gate. This result rejects only this frozen configuration on these four development prompts.

**PI/OpenAI — same-family/static review, not independent-family scientific approval.**