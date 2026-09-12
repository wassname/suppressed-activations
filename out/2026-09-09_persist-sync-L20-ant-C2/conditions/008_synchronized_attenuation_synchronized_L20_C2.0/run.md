---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-336-ga1ee28b-dirty"
code_sha256: {"scripts/oat_sweep.py": "cf276602c7014e3a57df2bfc3670824aac779fc56b46518b2041d60453fdd3d3", "scripts/demo.py": "3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "008_synchronized_attenuation_synchronized_L20_C2.0"
axis: "synchronized_attenuation"
value: "synchronized_L20_C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Ant"
swap_log_odds_shift: 2.96875
bare_answer_mass: 0.05490169674158096
source_output: "Spider"
target_output: "Ant"
donor_p_target: 0.0022101402282714844
donor_first_answer: null
donor_generation_tokens: 65
p_target: 2.7633970603346825e-05
p_source: 0.05487406253814697
first_logits_sha256: {"base": "80d65f35351532b79f0dcae8c9462eb325f2b93824e9ec847e50110e0a0e8bcd", "donor": "c996ca6b775d1cdad771ed48fc8a8e7aec402c151a7ccfccc80fa8da44a63e12", "steered": "c9ad3cfd5652b7774011288b0859a86602f8ea87e93f81bfa6e55dc7bdb3c5a6"}
repeated_bigram_fraction: 0.0
generation_tokens: 64
first_token: "蜘蛛"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.75
readout_status: "computed; semantic validity not established"
log: "conditions/008_synchronized_attenuation_synchronized_L20_C2.0/run.md"
last_decode_readout: [" mettere", "wj", "ậy", "いきます", " тренер", "Ctrl", "笠", " патру"]
---

# 008_synchronized_attenuation_synchronized_L20_C2.0

Expected Base answer: `Spider`. Expected donor-directed answer:
`Ant`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `008_synchronized_attenuation_synchronized_L20_C2.0`. Check those for
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
  "match_component_norm": false,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 4,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "synchronized",
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
  "future_lexical_union": false
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
[' respuesta', 'responseObject', ' respond', ' respuestas', 'getResponse', '谜底', '_response', ' risposta']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `008_synchronized_attenuation_synchronized_L20_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' mettere', 'wj', 'ậy', 'いきます', ' тренер', 'Ctrl', '笠', ' патру']
```

Unmodified donor readout:

```python
[' respuesta', 'getResponse', 'ưởi', 'responseObject', '谜底', '_response', ' respuestas', ' response']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`008_synchronized_attenuation_synchronized_L20_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 64 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to catch prey. These eight-legged creatures are found in various
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'       | -0.528  | 0.589952 | -0.123            |
| 2      | '蛛'        | -2.090  | 0.123661 | +0.189            |
| 3      | ' Spider'  | -2.590  | 0.075004 | -0.061            |
| 4      | 'Spider'   | -2.903  | 0.054874 | +0.064            |
| 5      | ' spider'  | -3.715  | 0.024350 | +0.064            |
| 6      | ' The'     | -4.215  | 0.014769 | +0.377            |
| 7      | '1'        | -4.590  | 0.010151 | +0.939            |
| 8      | ' **'      | -4.778  | 0.008415 | +0.502            |
| 9      | ' Sp'      | -5.153  | 0.005784 | +0.502            |
| 10     | ' spiders' | -5.153  | 0.005784 | +0.127            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
