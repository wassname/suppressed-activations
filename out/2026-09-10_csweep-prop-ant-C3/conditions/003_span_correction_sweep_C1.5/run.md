---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-342-gf00bb07"
code_sha256: {"scripts/oat_sweep.py": "01901b17a9ade112d49e60c260c8cfa723ffc6b692196cff319c1a7079baf13c", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
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
swap_log_odds_shift: 0.0
bare_answer_mass: 0.003613753942772746
source_output: "No"
target_output: "Yes"
donor_p_target: 0.000990669010207057
donor_first_answer: null
donor_generation_tokens: 83
p_target: 0.003470508847385645
p_source: 0.00014324499352369457
first_logits_sha256: {"base": "a6c25cf5e3bc868a2bd9256c17574a57786349a844bded183a96ad4009ed10a6", "donor": "244dd902b8d9e7c73b892e25e3e7b946276d3384f79fc937812a167e7e3a8103", "steered": "3aa6ace380f59f94a5d360928c7c254e0590762872e092db3afa7db0ebda9184"}
repeated_bigram_fraction: 0.03508771929824561
generation_tokens: 59
first_token: " Yes"
first_answer: "Yes"
mentions_spins_webs: false
readout_overlap: 0.625
readout_status: "computed; semantic validity not established"
log: "conditions/003_span_correction_sweep_C1.5/run.md"
last_decode_readout: [" μικ", " pequeños", " Малень", " cari", " pequeño", " piccolo", " piccoli", " کوچک"]
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
[' risposta', ' respuesta', ' Kraft', ' respuestas', ' resposta', ' respostas', '[__', ' réponses']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_span_correction_sweep_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' μικ', ' pequeños', ' Малень', ' cari', ' pequeño', ' piccolo', ' piccoli', ' کوچک']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' response', ' respuestas', ' respond', ' resposta', '_response', ' réponses']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_span_correction_sweep_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 59 tokens, verbatim):

```text
 Yes.

The ant is a small, social insect that lives in colonies and communicates through chemical signals. It possesses two distinct types of antennae: short ones
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Yes'    | -1.163  | 0.312405 | +0.794            |
| 2      | ' No'     | -1.288  | 0.275697 | +1.044            |
| 3      | '1'       | -1.788  | 0.167218 | -0.581            |
| 4      | ' **'     | -2.538  | 0.078988 | +1.232            |
| 5      | '<think>' | -2.788  | 0.061516 | -0.831            |
| 6      | '0'       | -3.851  | 0.021259 | -1.018            |
| 7      | '3'       | -3.976  | 0.018761 | -0.581            |
| 8      | '2'       | -4.163  | 0.015554 | -0.893            |
| 9      | '5'       | -5.226  | 0.005375 | -1.706            |
| 10     | '4'       | -5.288  | 0.005050 | -1.268            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
