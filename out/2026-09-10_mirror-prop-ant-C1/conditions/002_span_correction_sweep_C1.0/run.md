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
expected_base_answer: "Yes"
expected_steered_answer: "No"
swap_log_odds_shift: -0.1875004768371582
bare_answer_mass: 0.0009359013638459146
source_output: "Yes"
target_output: "No"
donor_p_target: 1.4635883417213336e-05
donor_first_answer: null
donor_generation_tokens: 58
p_target: 1.316216730629094e-05
p_source: 0.0009227392147295177
first_logits_sha256: {"base": "706742a8d59099baed595b6c4cac8e13ff1dfac742361d352187c54ed947f8d8", "donor": "394b4349115b0fb0f7fd4b6a0614e7b8c1a6c1efe81b22284af483aed255b248", "steered": "05a38e278bf2baa68b2bd3e495dfaf538e4c1b63e9f30a89076112f3eef7b786"}
repeated_bigram_fraction: 0.027027027027026973
generation_tokens: 76
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.625
readout_status: "computed; semantic validity not established"
log: "conditions/002_span_correction_sweep_C1.0/run.md"
last_decode_readout: ["卡和", "微小的", " cari", " mikro", "纳士", "small", "七日", "さり"]
---

# 002_span_correction_sweep_C1.0

Expected Base answer: `Yes`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
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
[' risposta', ' respuesta', ' resposta', ' respuestas', ' Kraft', ' respostas', ' jawaban', ' پاسخ']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_span_correction_sweep_C1.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['卡和', '微小的', ' cari', ' mikro', '纳士', 'small', '七日', 'さり']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' resposta', ' respuestas', ' réponses', ' respostas', ' response', ' answer']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_span_correction_sweep_C1.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 76 tokens, verbatim):

```text
1. 2. 3.

The ant is a small, social insect known for its ability to carry objects much larger than itself. It possesses six
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.238  | 0.289916 | -0.163            |
| 2      | ' Yes'    | -1.488  | 0.225787 | +1.212            |
| 3      | ' No'     | -2.363  | 0.094122 | +1.399            |
| 4      | '<think>' | -2.488  | 0.083062 | +0.024            |
| 5      | ' **'     | -2.738  | 0.064689 | +1.649            |
| 6      | '8'       | -2.863  | 0.057088 | -1.038            |
| 7      | '2'       | -3.363  | 0.034626 | -0.413            |
| 8      | '3'       | -3.801  | 0.022356 | -0.163            |
| 9      | '0'       | -3.926  | 0.019729 | -0.663            |
| 10     | '5'       | -3.988  | 0.018534 | -0.538            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
