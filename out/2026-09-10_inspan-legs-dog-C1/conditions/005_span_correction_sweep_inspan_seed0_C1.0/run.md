---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-342-gf00bb07"
code_sha256: {"scripts/oat_sweep.py": "01901b17a9ade112d49e60c260c8cfa723ffc6b692196cff319c1a7079baf13c", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "005_span_correction_sweep_inspan_seed0_C1.0"
axis: "span_correction_sweep"
value: "inspan_seed0_C1.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 6.375
bare_answer_mass: 0.9933021068572998
source_output: "8"
target_output: "4"
donor_p_target: 0.9885791540145874
donor_first_answer: "4"
donor_generation_tokens: 69
p_target: 0.9604377150535583
p_source: 0.032864369451999664
first_logits_sha256: {"base": "cd58e983bf2bdbe71f66d3fe48907993f9dbe6c5d32a594f6a75de678329a5d4", "donor": "cb6532e1e1862c05056d5404c0aa1d3b8efaaab1a02b3dd0fb31f36aecfdb0bf", "steered": "5dc912f9b408aafc35ecdf3af0d3703e357e9a1a26eafc54b0ad51f131ee0aa1"}
repeated_bigram_fraction: 0.045454545454545414
generation_tokens: 68
first_token: "4"
first_answer: "4"
mentions_spins_webs: false
readout_overlap: 0.375
readout_status: "computed; semantic validity not established"
log: "conditions/005_span_correction_sweep_inspan_seed0_C1.0/run.md"
last_decode_readout: ["時間も", "卡和", "嬉戏", "クラウド", "常规赛", "جاع", "网游", "getMock"]
---

# 005_span_correction_sweep_inspan_seed0_C1.0

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `005_span_correction_sweep_inspan_seed0_C1.0`. Check those for
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
  "strength": 1.0,
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
  "random_in_span": true
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that barks and is called man's best friend have?\nAnswer: "
```

Unmodified donor generation (first 32 of 69 tokens, verbatim):

```text
4

The animal you are referring to is a dog, which is a domesticated carnivorous mammal known for its loyalty and versatility. Dogs typically have four
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' respuesta', ' risposta', 'getResponse', '拥有着', ' resposta', 'response', '_response', ' respond']
```

Base generation (first 32 of 58 tokens, verbatim):

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect
```

Base next-token distribution:

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.084  | 0.919164 | +0.000            |
| 2      | '4'     | -3.084  | 0.045763 | +0.000            |
| 3      | '6'     | -3.584  | 0.027756 | +0.000            |
| 4      | '3'     | -6.084  | 0.002278 | +0.000            |
| 5      | '1'     | -6.334  | 0.001774 | +0.000            |
| 6      | '2'     | -6.709  | 0.001220 | +0.000            |
| 7      | '0'     | -7.459  | 0.000576 | +0.000            |
| 8      | '5'     | -7.834  | 0.000396 | +0.000            |
| 9      | '7'     | -7.959  | 0.000349 | +0.000            |
| 10     | 'Eight' | -8.584  | 0.000187 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' respuesta', ' risposta', '$id', 'renders', 'getResponse', ' pia', ' contradictions', '､']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `005_span_correction_sweep_inspan_seed0_C1.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['時間も', '卡和', '嬉戏', 'クラウド', '常规赛', 'جاع', '网游', 'getMock']
```

Unmodified donor readout:

```python
[' respuesta', '拥有着', 'getResponse', ' risposta', '_response', ' response', ' respond', 'responses']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`005_span_correction_sweep_inspan_seed0_C1.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 68 tokens, verbatim):

```text
4

The animal is a domestic cat, which is a common household pet known for its soft fur and playful nature. It typically has a round face, large
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.040  | 0.960438 | +3.044            |
| 2      | '8'     | -3.415  | 0.032864 | -3.331            |
| 3      | '6'     | -6.040  | 0.002381 | -2.456            |
| 4      | '2'     | -6.415  | 0.001636 | +0.294            |
| 5      | '1'     | -7.165  | 0.000773 | -0.831            |
| 6      | '3'     | -7.415  | 0.000602 | -1.331            |
| 7      | ' Four' | -7.665  | 0.000469 | +2.856            |
| 8      | '5'     | -8.540  | 0.000195 | -0.706            |
| 9      | '0'     | -8.728  | 0.000162 | -1.269            |
| 10     | '7'     | -8.853  | 0.000143 | -0.894            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
