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
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 12.5
bare_answer_mass: 0.9805341362953186
source_output: "8"
target_output: "4"
donor_p_target: 0.9893007874488831
donor_first_answer: "4"
donor_generation_tokens: 67
p_target: 0.9803788065910339
p_source: 0.00015535209968220443
first_logits_sha256: {"base": "2973d67df11a211a4fa625d5493b79e8f5c91c266e76b455d56868bf0b743696", "donor": "8703900bfbf2d0fb2a7a805d07bde1bb5ffcd7bc8ae182167bcb9eb59679bc17", "steered": "d9f38a08f74c15061a87893aa145d4a857636609fbed2ce6b241e1bdd7b9172d"}
repeated_bigram_fraction: 0.04225352112676062
generation_tokens: 73
first_token: "4"
first_answer: "4"
mentions_spins_webs: false
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/007_span_correction_sweep_inspan_seed0_C2.0/run.md"
last_decode_readout: ["時間も", "卡和", "管理学院", ".blit", "嬉戏", " ยัง", " مؤسسة", "Iteration"]
---

# 007_span_correction_sweep_inspan_seed0_C2.0

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal known for spinning webs to catch insects have?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal known for barking while living as a domesticated pet have?\nAnswer: '
```

Unmodified donor generation (first 32 of 67 tokens, verbatim):

```text
4

The animal is a dog, a highly social mammal known for its loyalty and ability to communicate with humans. It typically has four legs, which allow
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' respuesta', ' risposta', 'getResponse', '拥有着', ' jawaban', ' resposta', '_response', 'responses']
```

Base generation (first 32 of 63 tokens, verbatim):

```text
8

The spider is an arachnid that typically has eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing
```

Base next-token distribution:

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.067  | 0.935530 | +0.000            |
| 2      | '6'     | -3.317  | 0.036274 | +0.000            |
| 3      | '4'     | -3.817  | 0.022002 | +0.000            |
| 4      | '1'     | -6.192  | 0.002046 | +0.000            |
| 5      | '3'     | -6.692  | 0.001241 | +0.000            |
| 6      | '2'     | -6.942  | 0.000967 | +0.000            |
| 7      | '0'     | -7.817  | 0.000403 | +0.000            |
| 8      | '5'     | -8.067  | 0.000314 | +0.000            |
| 9      | 'Eight' | -8.192  | 0.000277 | +0.000            |
| 10     | '八'     | -8.504  | 0.000203 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['$id', ' pia', ' respuesta', 'だら', ' contradictions', ' risposta', '大賽', 'トレンド']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `007_span_correction_sweep_inspan_seed0_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['時間も', '卡和', '管理学院', '.blit', '嬉戏', ' ยัง', ' مؤسسة', 'Iteration']
```

Unmodified donor readout:

```python
[' respuesta', ' risposta', 'getResponse', '_response', ' jawaban', ' resposta', 'returnValue', '拥有着']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`007_span_correction_sweep_inspan_seed0_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 73 tokens, verbatim):

```text
4

The animal is a cow, which is a large mammal with a smooth, light-colored coat and a long, curved black horn. It has a
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.020  | 0.980379 | +3.797            |
| 2      | '2'     | -4.270  | 0.013984 | +2.672            |
| 3      | ' Four' | -6.395  | 0.001670 | +4.484            |
| 4      | '1'     | -6.395  | 0.001670 | -0.203            |
| 5      | '四'     | -7.457  | 0.000577 | +5.547            |
| 6      | ' four' | -7.832  | 0.000397 | +6.547            |
| 7      | ' The'  | -8.645  | 0.000176 | +2.859            |
| 8      | '8'     | -8.770  | 0.000155 | -8.703            |
| 9      | '四条'    | -9.207  | 0.000100 | +5.109            |
| 10     | 'four'  | -9.520  | 0.000073 | +5.734            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
