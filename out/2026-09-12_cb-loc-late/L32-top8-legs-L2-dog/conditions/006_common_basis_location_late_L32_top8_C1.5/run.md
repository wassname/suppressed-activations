---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-423-ged7d7e9"
code_sha256: {"scripts/oat_sweep.py": "6484410b7ec00f2fa224b46252ee98b64bb3f36bc77273a11242967cdecff1c0", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "006_common_basis_location_late_L32_top8_C1.5"
axis: "common_basis_location_late"
value: "L32_top8_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 2.125
bare_answer_mass: 0.9151177406311035
source_output: "8"
target_output: "4"
donor_p_target: 0.9920498728752136
donor_first_answer: "4"
donor_generation_tokens: 76
p_target: 0.061813175678253174
p_source: 0.8533045649528503
first_logits_sha256: {"base": "604fae9f54c39f1fc5b5a6c433d9160b17d5a1beb774519a2ef291c1e0e4fe58", "donor": "1cbb95e1533805432f30d9741b6ef0159bfa6320c5f25372f38f382b31471fca", "steered": "8d120f80f9c4f677d831eac2af274c7d54f63d61d564c2d3bbd2e4dd4a6991c8"}
repeated_bigram_fraction: 0.0
generation_tokens: 75
first_token: "8"
first_answer: "8"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/006_common_basis_location_late_L32_top8_C1.5/run.md"
last_decode_readout: ["万吨", "聚氨酯", "环绕", "Implemented", "election", "味", " instituto", "_aligned"]
---

# 006_common_basis_location_late_L32_top8_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `006_common_basis_location_late_L32_top8_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    29,
    30,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    32
  ],
  "intervention_positions": 3,
  "strength": 1.5,
  "match_component_norm": false,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 0,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "none",
  "source_dominant_only": false,
  "template_contrast": true,
  "contrastive_suppression": false,
  "template_state_span": "none",
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
  "common_seed": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: An animal known for spinning webs to catch insects has how many legs?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: An animal known for barking while living as a domesticated pet has how many legs?\nAnswer: '
```

Unmodified donor generation (first 32 of 76 tokens, verbatim):

```text
4

The dog is a highly social and intelligent mammal that has been domesticated by humans for thousands of years. They possess a keen sense of smell and
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' Август', ' вось', ' søger', ' vuốt', ' fotovolta', ',s', '林志', ' submar']
```

Base generation (first 32 of 62 tokens, verbatim):

```text
8

The spider is an arachnid that possesses eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing vibrations
```

Base next-token distribution:

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.028  | 0.972707 | +0.000            |
| 2      | '6'     | -4.278  | 0.013875 | +0.000            |
| 3      | '4'     | -4.778  | 0.008416 | +0.000            |
| 4      | '1'     | -6.278  | 0.001878 | +0.000            |
| 5      | '2'     | -7.028  | 0.000887 | +0.000            |
| 6      | '3'     | -7.278  | 0.000691 | +0.000            |
| 7      | '0'     | -8.028  | 0.000326 | +0.000            |
| 8      | '5'     | -8.153  | 0.000288 | +0.000            |
| 9      | 'Eight' | -8.403  | 0.000224 | +0.000            |
| 10     | '7'     | -8.653  | 0.000175 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' вось', ' Август', '第八条', ',s', 'eight', '.s', 'Eight', ' восьми']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `006_common_basis_location_late_L32_top8_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['万吨', '聚氨酯', '环绕', 'Implemented', 'election', '味', ' instituto', '_aligned']
```

Unmodified donor readout:

```python
[' vuốt', ' reimburse', '兩個人', ' fotovolta', 'ری', ' そこで', 'sker', ' ifstream']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`006_common_basis_location_late_L32_top8_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 75 tokens, verbatim):

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments called the cephalothorax and abdomen. Unlike insects,
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.159  | 0.853305 | -0.131            |
| 2      | '4'     | -2.784  | 0.061813 | +1.994            |
| 3      | '6'     | -2.909  | 0.054550 | +1.369            |
| 4      | '1'     | -4.159  | 0.015629 | +2.119            |
| 5      | '2'     | -5.284  | 0.005074 | +1.744            |
| 6      | '3'     | -5.409  | 0.004478 | +1.869            |
| 7      | '0'     | -6.284  | 0.001867 | +1.744            |
| 8      | '5'     | -6.534  | 0.001454 | +1.619            |
| 9      | '7'     | -7.284  | 0.000687 | +1.369            |
| 10     | '9'     | -8.096  | 0.000305 | +1.432            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
