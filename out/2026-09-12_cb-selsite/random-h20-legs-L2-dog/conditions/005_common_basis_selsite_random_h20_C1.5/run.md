---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-495-gede3e98-dirty"
code_sha256: {"scripts/oat_sweep.py": "24d314b9124a9ba1a1c481a78a2277d9c0c1150fe2ddcef6e71e5ebd790284c8", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "005_common_basis_selsite_random_h20_C1.5"
axis: "common_basis_selsite"
value: "random_h20_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9789111018180847
source_output: "8"
target_output: "4"
donor_p_target: 0.9920498728752136
donor_first_answer: "4"
donor_generation_tokens: 76
p_target: 0.008396593853831291
p_source: 0.9705145359039307
first_logits_sha256: {"base": "604fae9f54c39f1fc5b5a6c433d9160b17d5a1beb774519a2ef291c1e0e4fe58", "donor": "1cbb95e1533805432f30d9741b6ef0159bfa6320c5f25372f38f382b31471fca", "steered": "fc3081d987c7f6a157936053b836684ce5751cbcbee7d4b5ca2e60b337a78a2d"}
repeated_bigram_fraction: 0.015873015873015928
generation_tokens: 65
first_token: "8"
first_answer: "8"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/005_common_basis_selsite_random_h20_C1.5/run.md"
last_decode_readout: ["気に", " trien", "ทัน", " víz", " związane", " って", " srl", "バンク"]
---

# 005_common_basis_selsite_random_h20_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `005_common_basis_selsite_random_h20_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    20
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
  "common_basis": "random_shared",
  "common_window": 4,
  "common_random_rank": 8,
  "common_seed": 0,
  "common_bank_layers": [
    23,
    25,
    32
  ],
  "common_selector": "snapshot",
  "common_removal": "joint",
  "removal_only": false,
  "common_inject_norm": "own",
  "common_inject": "pd_d",
  "common_inject_restricted": false,
  "sync_donor": false
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
['_disc', '_target', 'هام', 'Taylor', ' cream', '枉', 'må', ' laba']
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
['_disc', '_target', 'هام', 'Taylor', '枉', 'må', 'Disc', ' comem']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `005_common_basis_selsite_random_h20_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['気に', ' trien', 'ทัน', ' víz', ' związane', ' って', ' srl', 'バンク']
```

Unmodified donor readout:

```python
['signature', ' infi', '踏上了', '_unix', 'atom', ' PEOPLE', 'かというと', ' disobed']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`005_common_basis_selsite_random_h20_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 65 tokens, verbatim):

```text
8

The spider is an arachnid that possesses eight legs, distinguishing it from insects which have six. These eight legs are typically long and jointed,
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.030  | 0.970515 | -0.002            |
| 2      | '6'     | -4.155  | 0.015687 | +0.123            |
| 3      | '4'     | -4.780  | 0.008397 | -0.002            |
| 4      | '1'     | -6.155  | 0.002123 | +0.123            |
| 5      | '2'     | -7.030  | 0.000885 | -0.002            |
| 6      | '3'     | -7.155  | 0.000781 | +0.123            |
| 7      | '0'     | -7.905  | 0.000369 | +0.123            |
| 8      | '5'     | -8.155  | 0.000287 | -0.002            |
| 9      | 'Eight' | -8.405  | 0.000224 | -0.002            |
| 10     | '7'     | -8.530  | 0.000197 | +0.123            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
