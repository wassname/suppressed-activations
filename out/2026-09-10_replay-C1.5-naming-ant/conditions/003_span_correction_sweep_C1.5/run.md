---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-386-g0b9ad07"
code_sha256: {"scripts/oat_sweep.py": "b8af2df00361efa953b890e41571c487767375384b1feca941d1ff38f08758d5", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "003_span_correction_sweep_C1.5"
axis: "span_correction_sweep"
value: "C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Ant"
swap_log_odds_shift: 13.8125
bare_answer_mass: 0.00711057661101222
source_output: "Spider"
target_output: "Ant"
donor_p_target: 0.0022101402282714844
donor_first_answer: null
donor_generation_tokens: 65
p_target: 0.006845160853117704
p_source: 0.0002654158161021769
first_logits_sha256: {"base": "80d65f35351532b79f0dcae8c9462eb325f2b93824e9ec847e50110e0a0e8bcd", "donor": "c996ca6b775d1cdad771ed48fc8a8e7aec402c151a7ccfccc80fa8da44a63e12", "steered": "2e4b3d4114b01216c04bf3ad7c2e1d53f4b6d7fd60580f8ed75e3215eb6150e4"}
repeated_bigram_fraction: 0.032786885245901676
generation_tokens: 63
first_token: " Ant"
first_answer: "Ant"
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/003_span_correction_sweep_C1.5/run.md"
last_decode_readout: ["微小的", " mikro", " Малень", " KAR", "卡和", "small", " cari", "แคร"]
---

# 003_span_correction_sweep_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Ant`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_span_correction_sweep_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    18,
    20,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    20
  ],
  "intervention_positions": 3,
  "strength": 1.5,
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
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that lives in colonies and follows pheromone trails called?\nAnswer: '
```

Unmodified donor generation (first 32 of 65 tokens, verbatim):

```text
蚂蚁 (Ant)

The ant is a small, social insect known for living in large, organized colonies. They communicate with each other primarily through chemical signals called
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' respuesta', 'responseObject', ' respond', ' respuestas', 'getResponse', '谜底', '_response', ' cries']
```

Base generation (first 32 of 74 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to catch prey. They possess eight legs and often live in
```

Base next-token distribution:

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'       | -0.404  | 0.667500 | +0.000            |
| 2      | '蛛'        | -2.279  | 0.102364 | +0.000            |
| 3      | ' Spider'  | -2.529  | 0.079721 | +0.000            |
| 4      | 'Spider'   | -2.967  | 0.051472 | +0.000            |
| 5      | ' spider'  | -3.779  | 0.022841 | +0.000            |
| 6      | ' The'     | -4.592  | 0.010135 | +0.000            |
| 7      | '8'        | -5.154  | 0.005775 | +0.000            |
| 8      | ' **'      | -5.279  | 0.005096 | +0.000            |
| 9      | ' spiders' | -5.279  | 0.005096 | +0.000            |
| 10     | '1'        | -5.529  | 0.003969 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['-push', 'に近い', ' respuesta', '是何含义', 'leaders', 'remento', '粮食', '顶着']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_span_correction_sweep_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['微小的', ' mikro', ' Малень', ' KAR', '卡和', 'small', ' cari', 'แคร']
```

Unmodified donor readout:

```python
[' respuesta', 'getResponse', 'ưởi', 'responseObject', '谜底', '_response', ' respuestas', ' response']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_span_correction_sweep_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 63 tokens, verbatim):

```text
 Ant

Description:
The ant is a small, social insect known for its ability to live in large colonies.
They are famous for their incredible strength,
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Ant'    | -1.734  | 0.176539 | +9.326            |
| 2      | '蚂蚁'      | -1.859  | 0.155795 | +6.858            |
| 3      | ' The'    | -2.234  | 0.107076 | +2.358            |
| 4      | '1'       | -2.359  | 0.094495 | +3.170            |
| 5      | ' **'     | -2.922  | 0.053841 | +2.358            |
| 6      | ' Worker' | -3.047  | 0.047515 | +11.576           |
| 7      | '蜜蜂'      | -3.234  | 0.039391 | +5.045            |
| 8      | '答案'      | -3.484  | 0.030678 | +4.358            |
| 9      | '工'       | -3.984  | 0.018607 | +6.139            |
| 10     | '蚁'       | -4.109  | 0.016421 | +4.920            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
