# Frozen half-erasure in native chat

Written by PI/OpenAI before any pretrained generation on these inputs. Four prompts, two same-answer pairs; a transfer attempt for readout, not a causal experiment. Both goals remain open.

## Decision and selection

Use the previously frozen J24, last-prefill position, half-erasure, greedy output mask1, k32. It was selected on v2 before v3; the later v3 semantic audit found seven successes, all geography. This new geography-only selection is posthoc to that observation. Do not call it broad English-task generalisation. GP2668 is retired and reserved v5 remains unrun. Advisor recommendation: `slop/reviews/2026-10-01_after-gradient-next-test.md`.

Data: `data/english_geography_chat_v1.json`, SHAced9ce88e658b20c9088ff51039736abc6bf40402032bf8eb0fd36279869eabe. Fixed messages ask only for the continent of the country whose capital is Muscat, Doha, Windhoek or Gaborone. Gold hidden identities are Oman, Qatar, Namibia and Botswana; shared answers Asia and Africa. Frozen identity aliases include Omani, Qatari, Namibian, Botswanan. Prefix labels are evaluation-only and retain their existing ambiguity; fragments are reviewed rather than silently promoted.

Novelty preflight: all four countries and cities occur in the prior TwoHopFact corpus. Country row counts3/6/2/7 respectively; city counts6/6/4/6. None of these country names was found in the recorded case inventories searched, but Muscat appears in the old TwoHopFact result. Rejected generations were not retained, so unseen-concept status cannot be established. Call these new prompt/property pairs, not certified-new concepts. Exact inventory paths, hash, examples and renderings: `2026-10-01_chat-preflight.json`.

## Input and generation policy

Use `scripts/english/08_jlens_one_pass.py`, not another inference pipeline. Native tokenizer chat template: one user message, `enable_thinking=False`, `add_generation_prompt=True`; remove the old Japan/Tokyo demonstration. This changes the prompt setting, not the frozen readout parameters. Example rendered string:

```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Muscat?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

The explicit empty thinking block is in the input template. No generated thoughts have been read. Template SHAa4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715; rendered/native-tokenized IDs agree. Transformers5.16.1 defaults `return_dict=True`; the check requestsFalse explicitly. The earlier assertion compared a list to that dictionary and failed; both preflight errors are retained.

Stop at either `<|endoftext|>`248044 (model config) or `<|im_end|>`248046 (tokenizer). The pinned snapshot has no separate generation_config.json; text_config's model EOS is cross-checked with saved job2668 runtime defaults. This is an explicit new native-chat termination policy, not retrospective rescoring. Leave completion-mode defaults unchanged.

Four greedy generation trajectories, maximum32 new tokens each, retaining early EOS and actual token count. Capture residual24/27/32 during the same generation. Assert one prefill plus n-1 cached decode calls. Save exact IDs and verbatim decoded strings including special tokens. For this new chat evaluation only, remove special tokens from scoring text so protocol markers do not become alleged spoken words. Generated words/gold labels affect evaluation only, never masks or ranks. Final-layer greedy masking and erasure still use the initial prefill's final-layer distribution, not generated text or future decode states.

## Fixed comparisons and scores

Primary: `end-pass erased0.5 J-lens`. Controls: equally processed `end-pass erased0.5 plain24`, `end-pass erased0.5 plain27`, and `end-pass J-lens` (mask-only). Other already-produced method rows are retained but cannot replace this primary or decide a different layer/strength/k. Same trajectories for every comparison; no intervention or gradients.

Report baseline correctness and instruction adherence from the complete continuation, lexical joint passes/4, alias-checked AUROC with its eligible denominator, and symmetric semantic annotations of all32 returned entries for all four reported methods. Retain wrong answers, unscoreable words, empty continuations and truncations. A semantic pass requires a clear hidden country identity and no definite input/actual-output equivalent in the list. Record uncertainty, not a fabricated exhaustive multilingual guarantee. Lexical and reviewed counts stay separate.

For each method/case record the best hidden-alias rank and same-answer partner-alias rank after the same masks. Strictly greater score count defines rank, so tied scores share rank. A discriminating pair requires both baselines correct, both country readouts semantically clean, and each own-country rank strictly better than its partner's rank, with own country actually returned. An unchanged list of both countries is insufficient; reversed appropriate ranking is evidence of discrimination even if both occur. Report discriminating pairs/2; no universal-success threshold. At least one clean discriminating pair would support an honest restricted demo; no such pair would leave this proposed demonstration unsupported. A different control winning is recorded, not substituted.

A country label can reflect an input association rather than a causally necessary internal step: the model may know a city's continent directly. This test does not establish necessity or concept replacement. Four deliberately selected questions and two dependent pairs do not estimate a population rate. Any displayed example is selected after examining all four, under this single configuration.

## Execution and verification

Before submission: parse source; preserve old default scoring via tiny real-Qwen comparisons against the archived pre-chat source; exercise native chat,32-token capture, early EOS, replay invariance, hook ownership and unchanged parameters. No scientific pretrained outputs during tests. Freeze source, helpers, data, template and launcher hashes. Run one local pueue-default job,300s TERM plus15s grace. No retries with altered prompts or method parameters.

On completion check complete console, exact generation/rendering/capture artifacts and all four methods' readouts. Numerical checks support but do not replace semantic review. Do not declare either research goal complete from this four-question transfer test alone.
