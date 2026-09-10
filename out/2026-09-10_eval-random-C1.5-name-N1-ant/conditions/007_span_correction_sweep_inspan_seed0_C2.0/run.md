---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
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
expected_base_answer: "Spider"
expected_steered_answer: "Ant"
swap_log_odds_shift: 5.937500476837158
bare_answer_mass: 0.0018383230781182647
source_output: "Spider"
target_output: "Ant"
donor_p_target: 0.002417853334918618
donor_first_answer: null
donor_generation_tokens: 81
p_target: 3.306448343209922e-05
p_source: 0.001805258565582335
first_logits_sha256: {"base": "bceff1b7ef03d8c8bf90c2df6d7ba46556dd703cb0d455447dd5a674b0154aa5", "donor": "d78c4e5463f982cbcfb9c17f79aab901e2bfbff4e723415041798b4bebe0c68b", "steered": "bebc422a4e4c61f4136eb0c702dc35d4cbd0ec6c410adf98f2d783e3f1a3ccf5"}
repeated_bigram_fraction: 0.26771653543307083
generation_tokens: 128
first_token: "8"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/007_span_correction_sweep_inspan_seed0_C2.0/run.md"
last_decode_readout: ["优良传统", "ессиона", "routeParams", " země", "=back", " جزء", "-delete", "休闲娱乐"]
---

# 007_span_correction_sweep_inspan_seed0_C2.0

Expected Base answer: `Spider`. Expected donor-directed answer:
`Ant`. A digit match alone does not establish concept replacement;
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Which animal is known for spinning webs to catch insects?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Which animal is known for living in colonies and following pheromone trails?\nAnswer: '
```

Unmodified donor generation (first 32 of 81 tokens, verbatim):

```text
蚂蚁 (Ants)

Ants are social insects that live in large, organized colonies with a distinct hierarchy of workers, soldiers, and queens. They communicate
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' respuesta', ' risposta', 'responseObject', ' dikaren', '解决', '谜底', ' respuestas', 'ưởi']
```

Base generation (first 32 of 60 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid that lives in various environments, from forests to urban areas. It creates intricate webs to trap prey,
```

Base next-token distribution:

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'       | -0.295  | 0.744515 | +0.000            |
| 2      | '蛛'        | -2.795  | 0.061114 | +0.000            |
| 3      | ' Spider'  | -3.295  | 0.037067 | +0.000            |
| 4      | 'Spider'   | -3.420  | 0.032712 | +0.000            |
| 5      | ' spider'  | -3.858  | 0.021120 | +0.000            |
| 6      | '8'        | -3.983  | 0.018639 | +0.000            |
| 7      | ' The'     | -4.608  | 0.009977 | +0.000            |
| 8      | '1'        | -4.608  | 0.009977 | +0.000            |
| 9      | ' spiders' | -4.733  | 0.008804 | +0.000            |
| 10     | ' **'      | -5.358  | 0.004713 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
["('('", ' Giêsu', ' respuesta', ' \'"\'', '_ident', '是何含义', ' SimpleName', '(GUI']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `007_span_correction_sweep_inspan_seed0_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['优良传统', 'ессиона', 'routeParams', ' země', '=back', ' جزء', '-delete', '休闲娱乐']
```

Unmodified donor readout:

```python
[' respuesta', ' risposta', ' respuestas', 'responseObject', '谜底', ' dikaren', ' réponses', '_response']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`007_span_correction_sweep_inspan_seed0_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
80% of the world's spider population is found in the United States, and the **spider** is the primary animal known for spinning webs to catch
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.630  | 0.532831 | +3.353            |
| 2      | '5'     | -2.255  | 0.104921 | +4.915            |
| 3      | '1'     | -2.755  | 0.063638 | +1.853            |
| 4      | ' The'  | -3.067  | 0.046558 | +1.540            |
| 5      | '6'     | -3.192  | 0.041088 | +3.915            |
| 6      | '7'     | -3.317  | 0.036260 | +4.228            |
| 7      | '4'     | -3.380  | 0.034063 | +3.853            |
| 8      | '2'     | -3.380  | 0.034063 | +2.603            |
| 9      | '9'     | -3.380  | 0.034063 | +4.478            |
| 10     | '0'     | -4.192  | 0.015115 | +2.478            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
