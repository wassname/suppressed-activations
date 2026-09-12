---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-348-ga22ae1a-dirty"
code_sha256: {"scripts/oat_sweep.py": "d1abdf53e53f2c41d8a48b3be8073e3520b7480ab479e982e020117715ea232b", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "004_span_correction_sweep_C2.0"
axis: "span_correction_sweep"
value: "C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 0.5
bare_answer_mass: 0.0017092723865061998
source_output: "No"
target_output: "Yes"
donor_p_target: 0.0017049607122316957
donor_first_answer: null
donor_generation_tokens: 62
p_target: 0.0013467890676110983
p_source: 0.00036248331889510155
first_logits_sha256: {"base": "94a631ae19c0c41b7209116d5a2949c2cfa94af8c1bf2634066e0821b1799777", "donor": "b6c90a72f3cc0cc68e473dc5338d39a248372e9fb89309fa1ee7d21d031a99ba", "steered": "af86cd7fba3432087ce8884959dfffb3e9b6b4e0971ffe13c72d7ad287965a47"}
repeated_bigram_fraction: 0.015873015873015928
generation_tokens: 65
first_token: " No"
first_answer: "No"
mentions_spins_webs: true
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
answer_position_attention: {"layer": -1, "answer_row_mean_over_heads": [0.0208740234375, 0.0028533935546875, 0.0267333984375, 0.00194549560546875, 0.000400543212890625, 0.000530242919921875, 0.00183868408203125, 0.00078582763671875, 0.0023193359375, 0.0028533935546875, 0.00982666015625, 0.00299072265625, 0.000843048095703125, 0.00102996826171875, 0.003997802734375, 0.00060272216796875, 0.00121307373046875, 0.001922607421875, 0.004669189453125, 0.00762939453125, 0.00994873046875, 0.01104736328125, 0.01226806640625, 0.025146484375, 0.0062255859375, 0.022216796875, 0.030029296875, 0.0634765625, 0.043701171875, 0.0169677734375, 0.0732421875, 0.01220703125, 0.01025390625, 0.0033721923828125, 0.0023040771484375, 0.009033203125, 0.009033203125, 0.0145263671875, 0.0057373046875, 0.0244140625, 0.0240478515625, 0.058349609375, 0.130859375, 0.28515625], "q_len": 44, "shape": [1, 16, 44, 44]}
log: "conditions/004_span_correction_sweep_C2.0/run.md"
last_decode_readout: ["卡和", "这个大", "ЗИ", "Mirror", "_dash", " tah", " عاط", " subsidi"]
---

# 004_span_correction_sweep_C2.0

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `004_span_correction_sweep_C2.0`. Check those for
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
  "future_lexical_union": false,
  "span_correction": true,
  "random_in_span": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Is the animal that spins webs a mammal?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Is the animal that barks and is called man's best friend a mammal?\nAnswer: "
```

Unmodified donor generation (first 32 of 62 tokens, verbatim):

```text
1. Yes, the dog is a mammal.
2. Dogs are warm-blooded vertebrates that possess hair or fur, which helps them regulate their
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', ' tidak', 'λευτα', ' respuestas', ' resposta', ' нек', ' réponses']
```

Base generation (first 32 of 79 tokens, verbatim):

```text
 No.

The animal that spins webs is a spider, which belongs to the class Arachnida rather than the class Mammalia. Unlike mammals,
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' No'     | -1.271  | 0.280493 | +0.000            |
| 2      | '1'       | -1.521  | 0.218448 | +0.000            |
| 3      | '<think>' | -1.646  | 0.192780 | +0.000            |
| 4      | '0'       | -3.084  | 0.045789 | +0.000            |
| 5      | ' **'     | -3.084  | 0.045789 | +0.000            |
| 6      | ' Yes'    | -3.271  | 0.037961 | +0.000            |
| 7      | '2'       | -3.709  | 0.024509 | +0.000            |
| 8      | '3'       | -3.709  | 0.024509 | +0.000            |
| 9      | '5'       | -4.021  | 0.017931 | +0.000            |
| 10     | '否'       | -4.146  | 0.015824 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' risposta', ' respuesta', ' opi', "','=',$", ' dol', '沁', '魂', 'GBT']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `004_span_correction_sweep_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', '这个大', 'ЗИ', 'Mirror', '_dash', ' tah', ' عاط', ' subsidi']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' respuestas', ' cpt', 'getResponse', ' resposta', ' response', ' respond']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`004_span_correction_sweep_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 65 tokens, verbatim):

```text
 No.

The animal that spins webs is a dog, which is a well-known breed of domesticated canine. Dogs are mammals that require regular exercise, social
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' No'     | -0.860  | 0.423149 | +0.411            |
| 2      | ' Yes'    | -1.860  | 0.155668 | +1.411            |
| 3      | '1'       | -1.985  | 0.137376 | -0.464            |
| 4      | '<think>' | -2.860  | 0.057267 | -1.214            |
| 5      | '2'       | -3.110  | 0.044600 | +0.599            |
| 6      | '0'       | -3.298  | 0.036974 | -0.214            |
| 7      | '4'       | -3.610  | 0.027051 | +0.849            |
| 8      | '5'       | -3.798  | 0.022426 | +0.224            |
| 9      | ' **'     | -3.798  | 0.022426 | -0.714            |
| 10     | '否'       | -4.360  | 0.012778 | -0.214            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
