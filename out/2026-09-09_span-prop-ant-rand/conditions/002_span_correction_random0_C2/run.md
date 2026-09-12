---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-341-g778c491"
code_sha256: {"scripts/oat_sweep.py": "94622a7364515543541d51400901ed9b9faaf686644b1dce855f58910bd2431b", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_span_correction_random0_C2"
axis: "span_correction"
value: "random0_C2"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: -0.8125
bare_answer_mass: 0.0018628059187904
source_output: "No"
target_output: "Yes"
donor_p_target: 0.000990669010207057
donor_first_answer: null
donor_generation_tokens: 83
p_target: 0.0017042829422280192
p_source: 0.00015852299111429602
first_logits_sha256: {"base": "a6c25cf5e3bc868a2bd9256c17574a57786349a844bded183a96ad4009ed10a6", "donor": "244dd902b8d9e7c73b892e25e3e7b946276d3384f79fc937812a167e7e3a8103", "steered": "eac6198a6f315895b8355b2c5b41d4d15eb85b62df1263101de2cebd4f27ee86"}
repeated_bigram_fraction: 0.06818181818181823
generation_tokens: 90
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.625
readout_status: "computed; semantic validity not established"
log: "conditions/002_span_correction_random0_C2/run.md"
last_decode_readout: ["ŗ", " لتش", "واطن", " Joko", "卡和", "してた", "两场", " assisti"]
---

# 002_span_correction_random0_C2

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_span_correction_random0_C2`. Check those for
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
  "span_correction": true
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that spins webs have antennae?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that lives in colonies and follows pheromone trails have antennae?\nAnswer: '
```

Unmodified donor generation (first 32 of 83 tokens, verbatim):

```text
1. Yes, the animal has antennae.

The animal you are describing is an ant, which is a social insect known for living in large, organized
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', 'λευτα', ' respuestas', ' resposta', ' respostas', ' réponses', ' response']
```

Base generation (first 32 of 88 tokens, verbatim):

```text
1. No, the animal that spins webs (a spider) does not have antennae.

Spiders are arachnids, not insects, which
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.208  | 0.298938 | +0.000            |
| 2      | '<think>' | -1.958  | 0.141208 | +0.000            |
| 3      | ' Yes'    | -1.958  | 0.141208 | +0.000            |
| 4      | ' No'     | -2.333  | 0.097051 | +0.000            |
| 5      | '0'       | -2.833  | 0.058864 | +0.000            |
| 6      | '2'       | -3.270  | 0.038006 | +0.000            |
| 7      | '3'       | -3.395  | 0.033540 | +0.000            |
| 8      | '5'       | -3.520  | 0.029599 | +0.000            |
| 9      | ' **'     | -3.770  | 0.023052 | +0.000            |
| 10     | '是的'      | -3.958  | 0.019110 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' risposta', ' respuesta', ' respuestas', ' resposta', '自助餐', ' respostas', ' réponses', '升息']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_span_correction_random0_C2`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['ŗ', ' لتش', 'واطن', ' Joko', '卡和', 'してた', '两场', ' assisti']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' response', ' respuestas', ' respond', ' resposta', '_response', ' réponses']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_span_correction_random0_C2`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 90 tokens, verbatim):

```text
1

The orb weaver is a type of spider known for its large, round body and its ability to spin a massive, circular web. Unlike many other
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.000  | 0.368023 | +0.208            |
| 2      | '<think>' | -1.500  | 0.223217 | +0.458            |
| 3      | '0'       | -2.000  | 0.135388 | +0.833            |
| 4      | '2'       | -2.750  | 0.063953 | +0.520            |
| 5      | '5'       | -3.250  | 0.038789 | +0.270            |
| 6      | '3'       | -3.375  | 0.034231 | +0.020            |
| 7      | '4'       | -3.500  | 0.030209 | +0.520            |
| 8      | '9'       | -3.875  | 0.020762 | +0.770            |
| 9      | '7'       | -4.125  | 0.016170 | +0.520            |
| 10     | '6'       | -4.250  | 0.014270 | +0.333            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
