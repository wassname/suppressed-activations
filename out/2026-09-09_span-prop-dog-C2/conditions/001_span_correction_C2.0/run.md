---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-341-g778c491"
code_sha256: {"scripts/oat_sweep.py": "94622a7364515543541d51400901ed9b9faaf686644b1dce855f58910bd2431b", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "001_span_correction_C2.0"
axis: "span_correction"
value: "C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 0.3750004768371582
bare_answer_mass: 0.00201874366030097
source_output: "No"
target_output: "Yes"
donor_p_target: 0.0018025756580755115
donor_first_answer: null
donor_generation_tokens: 62
p_target: 0.0016866271616891026
p_source: 0.0003321163821965456
first_logits_sha256: {"base": "6c17cd71674ef2b347d34e8efddc9173a282a412025ef371edeb47d2f064ce1b", "donor": "19039e2a96829cc819be2815976464a3267b97a90770f0669059f0c5c177b6e0", "steered": "d10414cca55f1d94c98920ca529efffac9474288ecbdee48f6ecb2b9b56726d7"}
repeated_bigram_fraction: 0.015873015873015928
generation_tokens: 65
first_token: " No"
first_answer: "No"
mentions_spins_webs: true
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
log: "conditions/001_span_correction_C2.0/run.md"
last_decode_readout: ["卡和", "ЗИ", "这个大", "Mirror", "_dash", " tah", " عاط", " subsidi"]
---

# 001_span_correction_C2.0

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_span_correction_C2.0`. Check those for
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
  "span_correction": true
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

Base generation (first 32 of 85 tokens, verbatim):

```text
 No.

The animal that spins webs is a spider, which belongs to the class Arachnida rather than the class Mammalia. Unlike mammals,
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' No'     | -1.211  | 0.297923 | +0.000            |
| 2      | '1'       | -1.586  | 0.204759 | +0.000            |
| 3      | '<think>' | -1.961  | 0.140729 | +0.000            |
| 4      | ' Yes'    | -2.711  | 0.066476 | +0.000            |
| 5      | ' **'     | -3.023  | 0.048635 | +0.000            |
| 6      | '0'       | -3.086  | 0.045688 | +0.000            |
| 7      | '2'       | -3.648  | 0.026032 | +0.000            |
| 8      | '否'       | -3.711  | 0.024455 | +0.000            |
| 9      | '3'       | -3.836  | 0.021581 | +0.000            |
| 10     | '5'       | -3.961  | 0.019046 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' risposta', ' respuesta', '魂', ' opi', 'GBT', "','=',$", '沁', 'Instagram']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_span_correction_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', 'ЗИ', '这个大', 'Mirror', '_dash', ' tah', ' عاط', ' subsidi']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' respuestas', 'getResponse', ' cpt', ' resposta', ' response', ' respond']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_span_correction_C2.0`. These records are retained without truncation.

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
| 1      | ' No'     | -0.948  | 0.387700 | +0.263            |
| 2      | ' Yes'    | -1.573  | 0.207521 | +1.138            |
| 3      | '1'       | -2.073  | 0.125868 | -0.487            |
| 4      | '<think>' | -3.073  | 0.046304 | -1.112            |
| 5      | '2'       | -3.260  | 0.038387 | +0.388            |
| 6      | '0'       | -3.385  | 0.033877 | -0.299            |
| 7      | '否'       | -3.760  | 0.023283 | -0.049            |
| 8      | '5'       | -3.760  | 0.023283 | +0.201            |
| 9      | ' **'     | -3.823  | 0.021873 | -0.799            |
| 10     | '4'       | -3.885  | 0.020547 | +0.638            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
