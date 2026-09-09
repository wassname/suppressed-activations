---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-364-g7965c51"
code_sha256: {"scripts/oat_sweep.py": "b48212eda67b4ad2ae10ac33c74c7764647582b72686ed1d35d68107658334a1", "scripts/demo.py": "ec0dfc89fba4948c35e5039e5c28ea484a820bef90b462dd7f2acbc37abc48c6", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_l26_span_correction_legs_dog_C1.5"
axis: "l26_span_correction"
value: "legs_dog_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 5.75
bare_answer_mass: 0.3211838901042938
source_output: "8"
target_output: "4"
donor_p_target: 0.9885791540145874
donor_first_answer: "4"
donor_generation_tokens: 69
p_target: 0.30188503861427307
p_source: 0.019298862665891647
first_logits_sha256: {"base": "cd58e983bf2bdbe71f66d3fe48907993f9dbe6c5d32a594f6a75de678329a5d4", "donor": "cb6532e1e1862c05056d5404c0aa1d3b8efaaab1a02b3dd0fb31f36aecfdb0bf", "steered": "123fc003ecb3c0c57630a14ee8f9d662c33e1687517dc14021bf44d4948d4d29"}
repeated_bigram_fraction: 0.2362204724409449
generation_tokens: 128
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/002_l26_span_correction_legs_dog_C1.5/run.md"
last_decode_readout: ["dog", "狗", " dog", " Dog", "狗狗", " chien", "犬", "Dog"]
---

# 002_l26_span_correction_legs_dog_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_l26_span_correction_legs_dog_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    24,
    26,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    26
  ],
  "intervention_positions": 3,
  "strength": 1.5,
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
  "random_in_span": false,
  "extra_prefill_positions": null
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
['BH', 'lim', 'imet', ' Verf', '齐心', '.po', '夜の', '.text']
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
[' gr', 'Addr', '_OPEN', '开盘', 'ประกวด', ' Bolshevik', ' surgiu', ' nochmal']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_l26_span_correction_legs_dog_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['dog', '狗', ' dog', ' Dog', '狗狗', ' chien', '犬', 'Dog']
```

Unmodified donor readout:

```python
[' dogg', ' chien', ' leash', ' perro', ' hond', 'dog', '_VER', ' canine']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_l26_span_correction_legs_dog_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
154

The animal is the dog, which is a common domesticated canine. Dogs typically have four legs, but the number 154 is
```

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | '1'          | -1.198  | 0.301885 | +5.137            |
| 2      | '4'          | -1.198  | 0.301885 | +1.887            |
| 3      | '3'          | -1.323  | 0.266413 | +4.762            |
| 4      | '5'          | -3.073  | 0.046296 | +4.762            |
| 5      | '8'          | -3.948  | 0.019299 | -3.863            |
| 6      | '2'          | -4.510  | 0.010996 | +2.199            |
| 7      | '6'          | -4.885  | 0.007558 | -1.301            |
| 8      | '<think>'    | -4.948  | 0.007100 | +6.449            |
| 9      | '狗'          | -5.323  | 0.004880 | +16.402           |
| 10     | '<|im_end|>' | -5.385  | 0.004584 | +7.574            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
