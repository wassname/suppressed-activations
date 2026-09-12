---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-356-g8236af8-dirty"
code_sha256: {"scripts/oat_sweep.py": "e30786161485188960b27b50d8c9a1295608951061006e239b80946e2b45cb23", "scripts/demo.py": "ec0dfc89fba4948c35e5039e5c28ea484a820bef90b462dd7f2acbc37abc48c6", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_h5_extended_C1.0"
axis: "smoke_h5_extended"
value: "C1.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: -1.1422119140625
bare_answer_mass: 1.1644235655694501e-06
source_output: "No"
target_output: "Yes"
donor_p_target: 2.440312982798787e-07
donor_first_answer: null
donor_generation_tokens: 4
p_target: 3.1638600717087684e-07
p_source: 8.480375299768639e-07
first_logits_sha256: {"base": "e1f26e5829ed3e1b33791aa47c6f3d5d52764405f8f57aae1f2276c4fc5e2eb2", "donor": "51ed776f3c6d80fbfc8d1a936af2c5bd6b6c0d5efb1fb4b18a681e5a157341ee", "steered": "738c91dc16e9a968ff84feccc5057a77cdf7e9553056f9d539a577d999e1a2fe"}
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "Beat"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/000_smoke_h5_extended_C1.0/run.md"
last_decode_readout: ["/card", " לעומת", " lob", "ание", " Corvette", " peacefully", "assigned", "\"))\n"]
---

# 000_smoke_h5_extended_C1.0

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_smoke_h5_extended_C1.0`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    0,
    2,
    4
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 3,
  "strength": 1.0,
  "match_component_norm": true,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 4,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "none",
  "source_dominant_only": false,
  "template_contrast": true,
  "contrastive_suppression": false,
  "template_state_span": "attenuation",
  "discarded_fraction": 0.0,
  "normalize_selector_residuals": false,
  "bee_correction": 0.0,
  "bee_correction_seed": -1,
  "bee_correction_only": false,
  "project_bee_correction": false,
  "transport_readout": false,
  "template_clamp": false,
  "future_coordinate": false,
  "future_clamp": false,
  "future_lexical_union": false,
  "span_correction": true,
  "random_in_span": false,
  "extra_prefill_positions": [
    2
  ]
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Is the animal that spins webs a mammal?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Is the animal that barks and is called man's best friend a mammal?\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
 textView pixelежеж
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['的道理', '.KeyEvent', ' Wikimedia', '\tpr', 'Pool', 'opup', 'очной', ' qq']
```

Base generation (first 4 of 4 tokens, verbatim):

```text
 textView Taipei總原来的
```

Base next-token distribution:

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | ' textView'  | -4.684  | 0.009242 | +0.000            |
| 2      | 'acr'        | -4.934  | 0.007198 | +0.000            |
| 3      | 'Destroyed'  | -5.434  | 0.004366 | +0.000            |
| 4      | '終わ'         | -5.746  | 0.003194 | +0.000            |
| 5      | '快讯'         | -5.746  | 0.003194 | +0.000            |
| 6      | ' mountains' | -5.746  | 0.003194 | +0.000            |
| 7      | 'ipelines'   | -5.809  | 0.003001 | +0.000            |
| 8      | ' Thickness' | -5.871  | 0.002819 | +0.000            |
| 9      | 'otp'        | -5.871  | 0.002819 | +0.000            |
| 10     | ' newSize'   | -5.871  | 0.002819 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' HTTPS', ')r', '啁', 'רט', '\tpr', '(attributes', 'kg', 'bern']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_h5_extended_C1.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['/card', ' לעומת', ' lob', 'ание', ' Corvette', ' peacefully', 'assigned', '"))\n']
```

Unmodified donor readout:

```python
[' ünivers', ' Braz', 'arden', 'getService', ' Dise', ' beforehand', ' מכל', ' dataSet']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_h5_extended_C1.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
BeatdescendingSmoke.entries
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'ﳒ'      | -5.630  | 0.003587 | +1.397            |
| 2      | '视频'     | -5.630  | 0.003587 | +1.429            |
| 3      | 'Beat'   | -5.630  | 0.003587 | +1.741            |
| 4      | 'memset' | -5.880  | 0.002794 | +2.585            |
| 5      | ' radar' | -5.880  | 0.002794 | +2.022            |
| 6      | 'Block'  | -6.130  | 0.002176 | +2.179            |
| 7      | ' idea'  | -6.162  | 0.002109 | +2.866            |
| 8      | '殄'      | -6.162  | 0.002109 | +1.960            |
| 9      | ' seis'  | -6.224  | 0.001981 | +0.210            |
| 10     | ' kos'   | -6.318  | 0.001804 | +1.304            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
