---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-342-gf00bb07"
code_sha256: {"scripts/oat_sweep.py": "01901b17a9ade112d49e60c260c8cfa723ffc6b692196cff319c1a7079baf13c", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_span_correction_sweep_C1.0"
axis: "span_correction_sweep"
value: "C1.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "6"
swap_log_odds_shift: 7.0
bare_answer_mass: 0.9924959540367126
source_output: "8"
target_output: "6"
donor_p_target: 0.9313044548034668
donor_first_answer: "6"
donor_generation_tokens: 67
p_target: 0.9634037017822266
p_source: 0.029092272743582726
first_logits_sha256: {"base": "cd58e983bf2bdbe71f66d3fe48907993f9dbe6c5d32a594f6a75de678329a5d4", "donor": "b0af8112a0ae505df37479dccb41c67c0030d0cd209ff3b2163dc1da4913b553", "steered": "e0ae484c60b7153a1f3b7fb60ca043e1066112493933f71b9cd54c261bcaa632"}
repeated_bigram_fraction: 0.0
generation_tokens: 69
first_token: "6"
first_answer: "6"
mentions_spins_webs: false
readout_overlap: 0.75
readout_status: "computed; semantic validity not established"
log: "conditions/002_span_correction_sweep_C1.0/run.md"
last_decode_readout: ["卡和", " căr", "いきます", "微小的", " мелкие", " cari", "手机上", " dông"]
---

# 002_span_correction_sweep_C1.0

Expected Base answer: `8`. Expected donor-directed answer:
`6`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_span_correction_sweep_C1.0`. Check those for
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
  "span_correction": true,
  "random_in_span": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that lives in colonies and follows pheromone trails have?\nAnswer: '
```

Unmodified donor generation (first 32 of 67 tokens, verbatim):

```text
6

The animal described is an ant, which is a social insect known for living in large, organized colonies. These insects communicate primarily through chemical signals called ph
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
[' respuesta', ' risposta', 'getResponse', '":@"', ' resposta', 'response', '_response', ' respond']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_span_correction_sweep_C1.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', ' căr', 'いきます', '微小的', ' мелкие', ' cari', '手机上', ' dông']
```

Unmodified donor readout:

```python
[' respuesta', ' risposta', '_response', ' response', 'getResponse', ' respond', ' resposta', '-road']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_span_correction_sweep_C1.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 69 tokens, verbatim):

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. It possesses six legs, which allow it to
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '6'     | -0.037  | 0.963404 | +3.547            |
| 2      | '8'     | -3.537  | 0.029092 | -3.453            |
| 3      | '3'     | -5.787  | 0.003066 | +0.297            |
| 4      | '1'     | -6.412  | 0.001641 | -0.078            |
| 5      | '4'     | -6.537  | 0.001448 | -3.453            |
| 6      | '2'     | -7.537  | 0.000533 | -0.828            |
| 7      | ' Six'  | -8.912  | 0.000135 | +2.672            |
| 8      | '7'     | -8.975  | 0.000127 | -1.015            |
| 9      | '0'     | -9.100  | 0.000112 | -1.640            |
| 10     | '5'     | -9.162  | 0.000105 | -1.328            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
