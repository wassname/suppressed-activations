---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-394-gb488cc0"
code_sha256: {"scripts/oat_sweep.py": "f355663f7b205045541e3f018612feff783b76226b4322931cabcc76b1123534", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "007_span_correction_sweep_inspan_seed0_C2.0"
axis: "span_correction_sweep"
value: "inspan_seed0_C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: -1.125
bare_answer_mass: 0.008037482388317585
source_output: "No"
target_output: "Yes"
donor_p_target: 0.0006593887810595334
donor_first_answer: null
donor_generation_tokens: 57
p_target: 0.0040187411941587925
p_source: 0.0040187411941587925
first_logits_sha256: {"base": "91d3b6107e211637b71e94f8128a3f93512c82784a60399f1c9f575ce4115589", "donor": "a7d392e91f31628aa948e61312ea02f0ed2d0b50b7e90e5a49df5af77f919ad3", "steered": "d41d124e685628b9ba2db5f2cdc37eea644eb2d88f572b9942ba6d80f9f8f805"}
repeated_bigram_fraction: 0.033333333333333326
generation_tokens: 92
first_token: "0"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/007_span_correction_sweep_inspan_seed0_C2.0/run.md"
last_decode_readout: ["時間も", " ยัง", "Mirror", "稻谷", "Sy", "编程语言", " مؤسسة", "卡和"]
---

# 007_span_correction_sweep_inspan_seed0_C2.0

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `007_span_correction_sweep_inspan_seed0_C2.0`. Check those for
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
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 4,
  "random_delta_seed": 0,
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
  "random_in_span": true,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for spinning webs to catch insects give birth to live young instead of laying eggs?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for barking while living as a domesticated pet give birth to live young instead of laying eggs?\nAnswer: '
```

Unmodified donor generation (first 32 of 57 tokens, verbatim):

```text
1. Yes, the dog gives birth to live young.
2. Dogs are mammals that typically have a gestation period of about 63 days.
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', ' réponses', ' respuestas', ' respostas', ' resposta', 'λευτα', '.va']
```

Base generation (first 32 of 79 tokens, verbatim):

```text
1. No.

The animal you are likely thinking of is the spider, which lays eggs rather than giving birth to live young. Spiders typically spin webs
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.467  | 0.230509 | +0.000            |
| 2      | '<think>' | -1.592  | 0.203423 | +0.000            |
| 3      | ' No'     | -2.155  | 0.115907 | +0.000            |
| 4      | '0'       | -2.217  | 0.108885 | +0.000            |
| 5      | '5'       | -3.092  | 0.045390 | +0.000            |
| 6      | ' **'     | -3.092  | 0.045390 | +0.000            |
| 7      | '2'       | -3.342  | 0.035350 | +0.000            |
| 8      | '3'       | -3.655  | 0.025862 | +0.000            |
| 9      | '否'       | -3.717  | 0.024295 | +0.000            |
| 10     | ' Yes'    | -3.780  | 0.022823 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['$id', ' risposta', '桂冠', ' مؤسسة', 'preso', "('/')", ' respuesta', 'iterations']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `007_span_correction_sweep_inspan_seed0_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['時間も', ' ยัง', 'Mirror', '稻谷', 'Sy', '编程语言', ' مؤسسة', '卡和']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' resposta', 'λευτα', ' réponses', ' respuestas', ' {}:', 'っちり']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`007_span_correction_sweep_inspan_seed0_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 92 tokens, verbatim):

```text
0
The animal described is a dog, which is a mammal that gives birth to live young rather than laying eggs. Unlike the common image of a pet
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '0'       | -1.017  | 0.361756 | +1.201            |
| 2      | '1'       | -1.642  | 0.193634 | -0.174            |
| 3      | ' No'     | -2.392  | 0.091466 | -0.237            |
| 4      | '<think>' | -2.642  | 0.071234 | -1.049            |
| 5      | '5'       | -3.142  | 0.043206 | -0.049            |
| 6      | '2'       | -3.267  | 0.038129 | +0.076            |
| 7      | '4'       | -3.392  | 0.033649 | +0.638            |
| 8      | '8'       | -3.704  | 0.024618 | +1.576            |
| 9      | '否'       | -3.767  | 0.023126 | -0.049            |
| 10     | '3'       | -4.079  | 0.016920 | -0.424            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
