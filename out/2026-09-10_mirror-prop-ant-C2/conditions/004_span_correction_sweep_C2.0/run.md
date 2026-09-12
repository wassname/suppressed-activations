---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-342-gf00bb07"
code_sha256: {"scripts/oat_sweep.py": "01901b17a9ade112d49e60c260c8cfa723ffc6b692196cff319c1a7079baf13c", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "004_span_correction_sweep_C2.0"
axis: "span_correction_sweep"
value: "C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Yes"
expected_steered_answer: "No"
swap_log_odds_shift: -0.0625004768371582
bare_answer_mass: 0.0028242177795618773
source_output: "Yes"
target_output: "No"
donor_p_target: 1.4635883417213336e-05
donor_first_answer: null
donor_generation_tokens: 58
p_target: 4.492311563808471e-05
p_source: 0.0027792947366833687
first_logits_sha256: {"base": "706742a8d59099baed595b6c4cac8e13ff1dfac742361d352187c54ed947f8d8", "donor": "394b4349115b0fb0f7fd4b6a0614e7b8c1a6c1efe81b22284af483aed255b248", "steered": "001cbf2abd0026a9c47f26e31a318c66ce5d4b0ca7cd629d8dcd9180553d6d13"}
repeated_bigram_fraction: 0.0
generation_tokens: 61
first_token: " Yes"
first_answer: "Yes"
mentions_spins_webs: false
readout_overlap: 0.5
readout_status: "computed; semantic validity not established"
log: "conditions/004_span_correction_sweep_C2.0/run.md"
last_decode_readout: [" pequeños", " pequeño", " μικ", " Малень", " pequeña", " کوچک", " kecil", " piccoli"]
---

# 004_span_correction_sweep_C2.0

Expected Base answer: `Yes`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that spins webs have eight legs?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that lives in colonies and follows pheromone trails have eight legs?\nAnswer: '
```

Unmodified donor generation (first 32 of 58 tokens, verbatim):

```text
1.

The animal you are describing is an ant. Ants are social insects that live in large, organized colonies and communicate primarily through chemical signals known as
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', ' resposta', ' respuestas', ' respostas', ' jawaban', ' پاسخ', ' réponses']
```

Base generation (first 32 of 67 tokens, verbatim):

```text
1.

The spider is an arachnid known for its ability to spin intricate webs to catch prey. It possesses eight legs, which are typically long and
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.075  | 0.341294 | +0.000            |
| 2      | '8'       | -1.825  | 0.161216 | +0.000            |
| 3      | '<think>' | -2.513  | 0.081064 | +0.000            |
| 4      | ' Yes'    | -2.700  | 0.067205 | +0.000            |
| 5      | '2'       | -2.950  | 0.052339 | +0.000            |
| 6      | '0'       | -3.263  | 0.038292 | +0.000            |
| 7      | '5'       | -3.450  | 0.031745 | +0.000            |
| 8      | '是的'      | -3.638  | 0.026318 | +0.000            |
| 9      | '4'       | -3.638  | 0.026318 | +0.000            |
| 10     | '3'       | -3.638  | 0.026318 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' risposta', ' respuesta', ' Kraft', ' resposta', ' piccolo', ' respuestas', ' eit', 'してた']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `004_span_correction_sweep_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' pequeños', ' pequeño', ' μικ', ' Малень', ' pequeña', ' کوچک', ' kecil', ' piccoli']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' resposta', ' respuestas', ' réponses', ' respostas', ' response', ' answer']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`004_span_correction_sweep_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 61 tokens, verbatim):

```text
 Yes.

The ant is a small, hardworking insect known for its ability to carry heavy loads. It possesses eight legs, which allow it to march in
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Yes'    | -0.948  | 0.387493 | +1.752            |
| 2      | ' No'     | -1.698  | 0.183039 | +2.064            |
| 3      | '1'       | -1.698  | 0.183039 | -0.623            |
| 4      | ' **'     | -2.073  | 0.125801 | +2.314            |
| 5      | '<think>' | -3.698  | 0.024772 | -1.186            |
| 6      | '2'       | -4.073  | 0.017025 | -1.123            |
| 7      | '3'       | -4.323  | 0.013259 | -0.686            |
| 8      | '0'       | -4.448  | 0.011701 | -1.186            |
| 9      | '5'       | -5.136  | 0.005884 | -1.686            |
| 10     | '4'       | -5.261  | 0.005192 | -1.623            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
