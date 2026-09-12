---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-420-g8d10c03"
code_sha256: {"scripts/oat_sweep.py": "3309806c2f8fb89e7afb2efdd83cc6b1efafe8abe3e50b1157b0dead89fc063e", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_common_basis_location_L25_top8_C1.5"
axis: "common_basis_location"
value: "L25_top8_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Ant"
swap_log_odds_shift: -0.203125
bare_answer_mass: 0.02091897837817669
source_output: "Spider"
target_output: "Ant"
donor_p_target: 0.004396853968501091
donor_first_answer: null
donor_generation_tokens: 76
p_target: 9.204596835843404e-07
p_source: 0.02091805823147297
first_logits_sha256: {"base": "cc25b9a0722ee874c2c86ae7942eb501c2a6f7f92a4d18e01b2bd5093a69cbdb", "donor": "afb1d8d60cab2d91ebbd9943671610e8ead541b725e5e688be34123badbb65d5", "steered": "7469837c41f0181f820d410b159373dedc23731d0786d5e2db981ad1914628bc"}
repeated_bigram_fraction: 0.013333333333333308
generation_tokens: 77
first_token: " Spider"
first_answer: "Spider"
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/002_common_basis_location_L25_top8_C1.5/run.md"
last_decode_readout: [" соци", " социальной", " социального", " sosyal", " κοινων", "social", " sozial", " Sosyal"]
---

# 002_common_basis_location_L25_top8_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Ant`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_common_basis_location_L25_top8_C1.5`. Check those for
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
    25
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: spinning webs to catch insects?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: living in colonies and following pheromone trails?\nAnswer: '
```

Unmodified donor generation (first 32 of 76 tokens, verbatim):

```text
1.  **Ants** are social insects that live in large, organized colonies.
2.  They communicate primarily through chemical signals known as pher
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
[' iterable', 'Amazon', 'Instagram', ':', '-', ' amazon', '.', ',']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_common_basis_location_L25_top8_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' соци', ' социальной', ' социального', ' sosyal', ' κοινων', 'social', ' sozial', ' Sosyal']
```

Unmodified donor readout:

```python
[' sosyal', ' iterable', 'Social', ' соци', ' κοινων', 'instagram', ' социального', '社交媒体']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_common_basis_location_L25_top8_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 77 tokens, verbatim):

```text
 Spider

Description:
Spiders are arachnids characterized by eight legs and two main body sections, the cephalothorax and abdomen.

```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Spider' | -0.992  | 0.370781 | +0.752            |
| 2      | '蜘蛛'      | -1.242  | 0.288765 | +0.315            |
| 3      | '8'       | -2.930  | 0.053416 | -0.498            |
| 4      | ' spider' | -3.242  | 0.039080 | +0.440            |
| 5      | ' The'    | -3.430  | 0.032399 | +0.690            |
| 6      | ' **'     | -3.492  | 0.030436 | -0.248            |
| 7      | ' Sp'     | -3.617  | 0.026859 | +0.002            |
| 8      | 'Spider'  | -3.867  | 0.020918 | -0.873            |
| 9      | '蛛'       | -4.117  | 0.016291 | -0.873            |
| 10     | '1'       | -4.242  | 0.014377 | -1.873            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
