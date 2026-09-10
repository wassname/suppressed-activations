---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-389-g9e198d1-dirty"
code_sha256: {"scripts/oat_sweep.py": "f355663f7b205045541e3f018612feff783b76226b4322931cabcc76b1123534", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "003_sync_l20_synchronized_C1.5"
axis: "sync_l20"
value: "synchronized_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: 1.375
bare_answer_mass: 0.8885564208030701
source_output: "8"
target_output: "4"
donor_p_target: 0.9885791540145874
donor_first_answer: "4"
donor_generation_tokens: 69
p_target: 0.14618216454982758
p_source: 0.7423742413520813
first_logits_sha256: {"base": "cd58e983bf2bdbe71f66d3fe48907993f9dbe6c5d32a594f6a75de678329a5d4", "donor": "cb6532e1e1862c05056d5404c0aa1d3b8efaaab1a02b3dd0fb31f36aecfdb0bf", "steered": "dfaf915191715e070b6eba31301a8ddb967e7bb1a85282534340a17f4f0da17b"}
repeated_bigram_fraction: 0.025000000000000022
generation_tokens: 82
first_token: "8"
first_answer: "8"
mentions_spins_webs: false
readout_overlap: 0.75
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/003_sync_l20_synchronized_C1.5/run.md"
last_decode_readout: ["为名", "KH", " возмож", " mettere", "第一场", "shelf", "ậy", "セール"]
---

# 003_sync_l20_synchronized_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_sync_l20_synchronized_C1.5`. Check those for
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
  "strength": 1.5,
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
  "future_lexical_union": false,
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null
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
[' respuesta', ' risposta', 'getResponse', '拥有着', ' resposta', 'response', '_response', ' respond']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_sync_l20_synchronized_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['为名', 'KH', ' возмож', ' mettere', '第一场', 'shelf', 'ậy', 'セール']
```

Unmodified donor readout:

```python
[' respuesta', '拥有着', 'getResponse', ' risposta', '_response', ' response', ' respond', 'responses']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_sync_l20_synchronized_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 82 tokens, verbatim):

```text
8

The spider is an arachnid that typically has eight legs, which it uses to walk, hunt, and build its intricate webs. Unlike insects,
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.298  | 0.742374 | -0.214            |
| 2      | '4'     | -1.923  | 0.146182 | +1.161            |
| 3      | '6'     | -2.298  | 0.100469 | +1.286            |
| 4      | '3'     | -5.798  | 0.003034 | +0.286            |
| 5      | '1'     | -5.923  | 0.002677 | +0.411            |
| 6      | '2'     | -6.173  | 0.002085 | +0.536            |
| 7      | '0'     | -6.673  | 0.001265 | +0.786            |
| 8      | '5'     | -7.423  | 0.000597 | +0.411            |
| 9      | '7'     | -7.798  | 0.000411 | +0.161            |
| 10     | '9'     | -8.798  | 0.000151 | +0.286            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
