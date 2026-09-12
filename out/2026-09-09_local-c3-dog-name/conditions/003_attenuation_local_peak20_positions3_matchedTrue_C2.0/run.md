---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-335-g122ec1a"
code_sha256: {"scripts/oat_sweep.py": "cf276602c7014e3a57df2bfc3670824aac779fc56b46518b2041d60453fdd3d3", "scripts/demo.py": "3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "003_attenuation_local_peak20_positions3_matchedTrue_C2.0"
axis: "attenuation_local"
value: "peak20_positions3_matchedTrue_C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 24.93896484375
bare_answer_mass: 0.006706924177706242
source_output: "Spider"
target_output: "Dog"
donor_p_target: 0.006302356719970703
donor_first_answer: null
donor_generation_tokens: 69
p_target: 0.00670689856633544
p_source: 2.5749965715249346e-08
first_logits_sha256: {"base": "80d65f35351532b79f0dcae8c9462eb325f2b93824e9ec847e50110e0a0e8bcd", "donor": "a4b6da56d070cc63e591072c949e6297fd7a0ddb19f0b9b30354b924b162ea15", "steered": "98cebf2136fc66e12e98e46d43539e8a55be3613884c5ad0570bf0eb875ec41b"}
repeated_bigram_fraction: 0.0
generation_tokens: 63
first_token: "狗"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
log: "conditions/003_attenuation_local_peak20_positions3_matchedTrue_C2.0/run.md"
last_decode_readout: ["卡和", "向记者", " عاط", "Parameter", " tah", " sentimental", "Mirror", "社交媒体"]
---

# 003_attenuation_local_peak20_positions3_matchedTrue_C2.0

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_attenuation_local_peak20_positions3_matchedTrue_C2.0`. Check those for
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
  "future_lexical_union": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that barks and is called man's best friend called?\nAnswer: "
```

Unmodified donor generation (first 32 of 69 tokens, verbatim):

```text
狗 (Dog)

The dog is a domesticated carnivorous mammal that has been bred by humans for thousands of years. They are known for their loyalty
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
[' respuesta', 'ErrorResponse', ' faj', '对记者', 'بيه', ' sụt', 'responseObject', '向记者']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_attenuation_local_peak20_positions3_matchedTrue_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', '向记者', ' عاط', 'Parameter', ' tah', ' sentimental', 'Mirror', '社交媒体']
```

Unmodified donor readout:

```python
[' respuesta', '谜底', 'anjangan', 'responseObject', 'getResponse', ' response', ' respond', '大名']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_attenuation_local_peak20_positions3_matchedTrue_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 63 tokens, verbatim):

```text
狗 (Dog)

The dog is a popular domesticated animal that has been raised by humans for thousands of years. They are known for their loyalty, intelligence
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '狗'     | -0.505  | 0.603736 | +10.900           |
| 2      | '犬'     | -2.380  | 0.092586 | +10.743           |
| 3      | '狗狗'    | -2.942  | 0.052754 | +10.962           |
| 4      | ' Dog'  | -3.005  | 0.049558 | +12.056           |
| 5      | ' The'  | -3.192  | 0.041085 | +1.400            |
| 6      | ' A'    | -3.380  | 0.034060 | +3.025            |
| 7      | '1'     | -4.442  | 0.011771 | +1.087            |
| 8      | '一只'    | -4.567  | 0.010388 | +1.775            |
| 9      | '猫'     | -4.692  | 0.009167 | +5.306            |
| 10     | ' **'   | -5.005  | 0.006707 | +0.275            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
