---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-459-g6e4fcfd-dirty"
code_sha256: {"scripts/oat_sweep.py": "bffdb169feef7d427c5dfd9bd75a9a93b364f2a8ead7268189eea8716f594f1d", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_common_basis_norm2x2_delta_scaled_to_v_C1.5"
axis: "common_basis_norm2x2"
value: "delta_scaled_to_v_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 2.5
bare_answer_mass: 0.5562753081321716
source_output: "8"
target_output: "4"
donor_p_target: 0.9893007874488831
donor_first_answer: "4"
donor_generation_tokens: 67
p_target: 0.12388257682323456
p_source: 0.4323927164077759
first_logits_sha256: {"base": "2973d67df11a211a4fa625d5493b79e8f5c91c266e76b455d56868bf0b743696", "donor": "8703900bfbf2d0fb2a7a805d07bde1bb5ffcd7bc8ae182167bcb9eb59679bc17", "steered": "873a5b4f279173def6ad8d2227497529c84b8e3e60455f4379285db654e827bf"}
repeated_bigram_fraction: 0.01388888888888884
generation_tokens: 74
first_token: "6"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/000_common_basis_norm2x2_delta_scaled_to_v_C1.5/run.md"
last_decode_readout: [".g", "卡和", "卡的", "GL", " scratched", "这样一个", "内蒙古自治区", "One"]
---

# 000_common_basis_norm2x2_delta_scaled_to_v_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_common_basis_norm2x2_delta_scaled_to_v_C1.5`. Check those for
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
  "strength": 2.5,
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
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null,
  "common_basis": "top8_union",
  "common_window": 4,
  "common_random_rank": 8,
  "common_seed": 0,
  "common_bank_layers": [
    23,
    25,
    32
  ],
  "common_removal": "pref",
  "common_inject_norm": "cross_v",
  "common_inject": "ref_delta",
  "common_inject_restricted": false,
  "sync_donor": false
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
[' respuesta', ' risposta', 'Task', 'ai', '同一', ' genera', 'Ty', 'Link']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_common_basis_norm2x2_delta_scaled_to_v_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['.g', '卡和', '卡的', 'GL', ' scratched', '这样一个', '内蒙古自治区', 'One']
```

Unmodified donor readout:

```python
[' respuesta', ' risposta', 'getResponse', '_response', ' jawaban', ' resposta', 'returnValue', '拥有着']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_common_basis_norm2x2_delta_scaled_to_v_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 74 tokens, verbatim):

```text
6

The animal is a spider, which belongs to the class Arachnida and is characterized by having eight legs rather than six. Spiders are famous
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '6'     | -0.838  | 0.432393 | +2.478            |
| 2      | '8'     | -0.838  | 0.432393 | -0.772            |
| 3      | '4'     | -2.088  | 0.123883 | +1.728            |
| 4      | '1'     | -5.588  | 0.003741 | +0.603            |
| 5      | '3'     | -5.963  | 0.002571 | +0.728            |
| 6      | '2'     | -6.213  | 0.002002 | +0.728            |
| 7      | '0'     | -7.088  | 0.000835 | +0.728            |
| 8      | '5'     | -7.338  | 0.000650 | +0.728            |
| 9      | '7'     | -8.151  | 0.000288 | +0.416            |
| 10     | ' Six'  | -8.526  | 0.000198 | +2.166            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
