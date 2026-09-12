---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-348-ga22ae1a-dirty"
code_sha256: {"scripts/oat_sweep.py": "d1abdf53e53f2c41d8a48b3be8073e3520b7480ab479e982e020117715ea232b", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "003_span_correction_sweep_C1.5"
axis: "span_correction_sweep"
value: "C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 0.1875004768371582
bare_answer_mass: 0.0011862678220495582
source_output: "No"
target_output: "Yes"
donor_p_target: 0.0017049607122316957
donor_first_answer: null
donor_generation_tokens: 62
p_target: 0.0008672313997521996
p_source: 0.0003190364222973585
first_logits_sha256: {"base": "94a631ae19c0c41b7209116d5a2949c2cfa94af8c1bf2634066e0821b1799777", "donor": "b6c90a72f3cc0cc68e473dc5338d39a248372e9fb89309fa1ee7d21d031a99ba", "steered": "6cb2fa52ec544d6448bfc3301943894b5a11829a7fbb43424e6b570ac44959a7"}
repeated_bigram_fraction: 0.01388888888888884
generation_tokens: 74
first_token: " No"
first_answer: "No"
mentions_spins_webs: true
readout_overlap: 0.5
readout_status: "computed; semantic validity not established"
answer_position_attention: {"layer": -1, "answer_row_mean_over_heads": [0.023681640625, 0.0032196044921875, 0.0286865234375, 0.002105712890625, 0.0004558563232421875, 0.000568389892578125, 0.0020294189453125, 0.0008697509765625, 0.0027008056640625, 0.00347900390625, 0.01080322265625, 0.0030059814453125, 0.00091552734375, 0.00107574462890625, 0.004180908203125, 0.000606536865234375, 0.001312255859375, 0.0020904541015625, 0.00494384765625, 0.0087890625, 0.0096435546875, 0.0101318359375, 0.01318359375, 0.02685546875, 0.006378173828125, 0.0216064453125, 0.033447265625, 0.06591796875, 0.041748046875, 0.01611328125, 0.06689453125, 0.0103759765625, 0.01007080078125, 0.0029449462890625, 0.0027923583984375, 0.00958251953125, 0.009521484375, 0.01458740234375, 0.00592041015625, 0.0281982421875, 0.0257568359375, 0.05859375, 0.119140625, 0.28515625], "q_len": 44, "shape": [1, 16, 44, 44]}
log: "conditions/003_span_correction_sweep_C1.5/run.md"
last_decode_readout: ["卡和", "ЗИ", "Mirror", "这个大", "镜头里", " عاط", "グレ", "_dash"]
---

# 003_span_correction_sweep_C1.5

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_span_correction_sweep_C1.5`. Check those for
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
[' risposta', ' respuesta', ' respuestas', "','=',$", ' Siri', ' resposta', ' raf', ' opi']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_span_correction_sweep_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', 'ЗИ', 'Mirror', '这个大', '镜头里', ' عاط', 'グレ', '_dash']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' respuestas', ' cpt', 'getResponse', ' resposta', ' response', ' respond']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_span_correction_sweep_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 74 tokens, verbatim):

```text
 No.

The animal that spins webs is a dog, which is a domesticated breed of canine known for its loyalty and ability to run alongside its owner.
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' No'     | -0.925  | 0.396450 | +0.346            |
| 2      | '1'       | -1.800  | 0.165265 | -0.279            |
| 3      | ' Yes'    | -2.300  | 0.100238 | +0.971            |
| 4      | '<think>' | -2.300  | 0.100238 | -0.654            |
| 5      | '2'       | -3.175  | 0.041786 | +0.534            |
| 6      | '0'       | -3.300  | 0.036876 | -0.216            |
| 7      | ' **'     | -3.613  | 0.026979 | -0.529            |
| 8      | '5'       | -3.800  | 0.022366 | +0.221            |
| 9      | '否'       | -3.800  | 0.022366 | +0.346            |
| 10     | '4'       | -4.050  | 0.017419 | +0.409            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
