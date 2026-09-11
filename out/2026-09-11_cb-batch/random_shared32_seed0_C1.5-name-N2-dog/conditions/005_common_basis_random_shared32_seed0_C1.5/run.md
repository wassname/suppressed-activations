---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-408-gfc92ae4"
code_sha256: {"scripts/oat_sweep.py": "a9427ddb76028ae9dd693b964a2c57823cc7ff58ec98d41bcec111f52c985a48", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "005_common_basis_random_shared32_seed0_C1.5"
axis: "common_basis"
value: "random_shared32_seed0_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 0.4375
bare_answer_mass: 0.03470220789313316
source_output: "Spider"
target_output: "Dog"
donor_p_target: 0.015015699900686741
donor_first_answer: null
donor_generation_tokens: 59
p_target: 6.77591344810935e-07
p_source: 0.03470152989029884
first_logits_sha256: {"base": "cc25b9a0722ee874c2c86ae7942eb501c2a6f7f92a4d18e01b2bd5093a69cbdb", "donor": "ac874a9acbda1ec84fd61d05c846f2399056a769d9defc82b8e16d89b02f0871", "steered": "449065c54b4b0501a5519d1d395e7c9bd415210024a20ed08d2f2f4fef6f39bc"}
repeated_bigram_fraction: 0.0
generation_tokens: 63
first_token: " Spider"
first_answer: "Spider"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/005_common_basis_random_shared32_seed0_C1.5/run.md"
last_decode_readout: [" って", " víz", " tph", "viet", "_bank", "_coin", " srl", " первым"]
---

# 005_common_basis_random_shared32_seed0_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `005_common_basis_random_shared32_seed0_C1.5`. Check those for
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
  "common_random_rank": 32,
  "common_seed": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: spinning webs to catch insects?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: barking while living as a domesticated pet?\nAnswer: '
```

Unmodified donor generation (first 32 of 59 tokens, verbatim):

```text
1. The dog.
2. The dog is a highly social and intelligent mammal known for its ability to communicate with humans through barking.
3
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['Budget', ' yummy', '.ExecuteNonQuery', 'Mbps', '拉丝', ' urbano', ' mdi', ' harap']
```

Base generation (first 32 of 63 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to trap prey. It uses silk threads to create a sticky
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'      | -1.557  | 0.210828 | +0.000            |
| 2      | ' Spider' | -1.744  | 0.174782 | +0.000            |
| 3      | '1'       | -2.369  | 0.093554 | +0.000            |
| 4      | '8'       | -2.432  | 0.087886 | +0.000            |
| 5      | 'Spider'  | -2.994  | 0.050076 | +0.000            |
| 6      | '蛛'       | -3.244  | 0.038999 | +0.000            |
| 7      | ' **'     | -3.244  | 0.038999 | +0.000            |
| 8      | ' Sp'     | -3.619  | 0.026804 | +0.000            |
| 9      | ' spider' | -3.682  | 0.025180 | +0.000            |
| 10     | '2'       | -3.744  | 0.023654 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['Budget', ' yummy', 'Mbps', '拉丝', ' ინ', ' harap', ' comem', ' urbano']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `005_common_basis_random_shared32_seed0_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' って', ' víz', ' tph', 'viet', '_bank', '_coin', ' srl', ' первым']
```

Unmodified donor readout:

```python
[' chien', 'Fetch', ' собаки', ' Hunde', 'fetch', ' кино', ' perros', ' labs']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`005_common_basis_random_shared32_seed0_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 63 tokens, verbatim):

```text
 Spider

Description:
Spiders are arachnids characterized by eight legs and two main body sections. They are famous for spinning silk webs to trap prey
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Spider' | -1.611  | 0.199694 | +0.133            |
| 2      | '蜘蛛'      | -1.798  | 0.165552 | -0.242            |
| 3      | '8'       | -2.173  | 0.113782 | +0.258            |
| 4      | '1'       | -2.548  | 0.078201 | -0.179            |
| 5      | ' **'     | -3.298  | 0.036940 | -0.054            |
| 6      | '蛛'       | -3.298  | 0.036940 | -0.054            |
| 7      | 'Spider'  | -3.361  | 0.034702 | -0.367            |
| 8      | ' The'    | -3.548  | 0.028769 | +0.571            |
| 9      | ' Sp'     | -3.548  | 0.028769 | +0.071            |
| 10     | '<think>' | -3.673  | 0.025388 | +0.071            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
