---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-348-ga22ae1a-dirty"
code_sha256: {"scripts/oat_sweep.py": "d1abdf53e53f2c41d8a48b3be8073e3520b7480ab479e982e020117715ea232b", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_span_correction_C0.0"
axis: "smoke_span_correction"
value: "C0.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 0.0
bare_answer_mass: 9.281953339268512e-08
source_output: "No"
target_output: "Yes"
donor_p_target: 2.2034620883459866e-07
donor_first_answer: null
donor_generation_tokens: 3
p_target: 4.858362956383644e-08
p_source: 4.4235900276135e-08
first_logits_sha256: {"base": "ca0af7544c26809c80668bd0d178be5330fc748d1ee767666140737c7b50e5e6", "donor": "f7cfa2e376bc0064bf75c06c7f7595c2bc1473145f776317e5e607ddfae1db4e", "steered": "ca0af7544c26809c80668bd0d178be5330fc748d1ee767666140737c7b50e5e6"}
repeated_bigram_fraction: 0.0
generation_tokens: 3
first_token: " textView"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: {"layer": -1, "answer_row_mean_over_heads": [0.029052734375, 0.025634765625, 0.0234375, 0.025146484375, 0.0235595703125, 0.016357421875, 0.0196533203125, 0.02685546875, 0.025390625, 0.025390625, 0.026611328125, 0.02490234375, 0.031005859375, 0.02880859375, 0.0263671875, 0.025634765625, 0.026123046875, 0.025146484375, 0.0244140625, 0.02490234375, 0.03369140625, 0.024658203125, 0.0194091796875, 0.026123046875, 0.024658203125, 0.018310546875, 0.017333984375, 0.0228271484375, 0.029541015625, 0.0166015625, 0.0201416015625, 0.018310546875, 0.0185546875, 0.0238037109375, 0.021728515625, 0.02490234375, 0.0198974609375, 0.0191650390625, 0.023681640625, 0.018310546875, 0.018310546875, 0.0169677734375, 0.01904296875], "q_len": 43, "shape": [1, 2, 43, 43]}
log: "conditions/000_smoke_span_correction_C0.0/run.md"
last_decode_readout: [" antib", "אפליק", " Lexer", "村镇", "/title", "基调", "潇洒", " records"]
---

# 000_smoke_span_correction_C0.0

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_smoke_span_correction_C0.0`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    0,
    2,
    4
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 3,
  "strength": 0.0,
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

Unmodified donor generation (first 3 of 3 tokens, verbatim):

```text
 textView pixelеж
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['的道理', '.KeyEvent', '\tpr', ' Wikimedia', 'Pool', 'opup', ' qq', ' reputation']
```

Base generation (first 3 of 3 tokens, verbatim):

```text
 textView Taipei總
```

Base next-token distribution:

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | ' textView'  | -4.668  | 0.009390 | +0.000            |
| 2      | 'acr'        | -4.918  | 0.007313 | +0.000            |
| 3      | 'Destroyed'  | -5.481  | 0.004167 | +0.000            |
| 4      | ' mountains' | -5.731  | 0.003245 | +0.000            |
| 5      | ' newSize'   | -5.793  | 0.003049 | +0.000            |
| 6      | '終わ'         | -5.793  | 0.003049 | +0.000            |
| 7      | 'ipelines'   | -5.793  | 0.003049 | +0.000            |
| 8      | 'otp'        | -5.856  | 0.002864 | +0.000            |
| 9      | '快讯'         | -5.856  | 0.002864 | +0.000            |
| 10     | ' Thickness' | -5.918  | 0.002690 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['的道理', '.KeyEvent', '\tpr', ' Wikimedia', 'Pool', 'opup', ' qq', ' reputation']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_span_correction_C0.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' antib', 'אפליק', ' Lexer', '村镇', '/title', '基调', '潇洒', ' records']
```

Unmodified donor readout:

```python
[' ünivers', ' Braz', 'arden', 'getService', ' Dise', ' beforehand', ' מכל', ' dataSet']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_span_correction_C0.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 3 of 3 tokens, verbatim):

```text
 textView Taipei總
```

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | ' textView'  | -4.668  | 0.009390 | +0.000            |
| 2      | 'acr'        | -4.918  | 0.007313 | +0.000            |
| 3      | 'Destroyed'  | -5.481  | 0.004167 | +0.000            |
| 4      | ' mountains' | -5.731  | 0.003245 | +0.000            |
| 5      | ' newSize'   | -5.793  | 0.003049 | +0.000            |
| 6      | '終わ'         | -5.793  | 0.003049 | +0.000            |
| 7      | 'ipelines'   | -5.793  | 0.003049 | +0.000            |
| 8      | 'otp'        | -5.856  | 0.002864 | +0.000            |
| 9      | '快讯'         | -5.856  | 0.002864 | +0.000            |
| 10     | ' Thickness' | -5.918  | 0.002690 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
