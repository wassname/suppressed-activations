---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-394-gb488cc0"
code_sha256: {"scripts/oat_sweep.py": "f355663f7b205045541e3f018612feff783b76226b4322931cabcc76b1123534", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "007_span_correction_sweep_inspan_seed0_C2.0"
axis: "span_correction_sweep"
value: "inspan_seed0_C2.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Yes"
expected_steered_answer: "No"
swap_log_odds_shift: -1.3437504768371582
bare_answer_mass: 0.008828104473650455
source_output: "Yes"
target_output: "No"
donor_p_target: 0.0002644975611474365
donor_first_answer: null
donor_generation_tokens: 109
p_target: 5.908518869546242e-05
p_source: 0.0087690195068717
first_logits_sha256: {"base": "8ded9cc3d2079310740d92c367131a2bf681e6a2f92b771add278d79bb0e8593", "donor": "b195bd9a62b379ae40318fcfe51cc513d80bceece58451226ece36418d4c9814", "steered": "533c92209bb8518afb3a57eb7a7c29363d2ef08375d9d1b8f805237ba1dc30f8"}
repeated_bigram_fraction: 0.25196850393700787
generation_tokens: 128
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.375
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/007_span_correction_sweep_inspan_seed0_C2.0/run.md"
last_decode_readout: ["exampleInputEmail", " Cari", "-valid", " Stam", " Whats", "()==", "\trestore", "exampleInput"]
---

# 007_span_correction_sweep_inspan_seed0_C2.0

Expected Base answer: `Yes`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `007_span_correction_sweep_inspan_seed0_C2.0`. Check those for
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
  "span_correction": true,
  "random_in_span": true,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for spinning webs to catch insects have spinnerets?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for barking while living as a domesticated pet have spinnerets?\nAnswer: '
```

Unmodified donor generation (first 32 of 109 tokens, verbatim):

```text
<think>

</think>

No, the animal known for barking while living as a domesticated pet does not have spinnerets.

The animal in question is a
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', ' resposta', ' answer', ' respuestas', ' réponses', ' respostas', ' jawaban']
```

Base generation (first 32 of 49 tokens, verbatim):

```text
1. Yes, spiders have spinnerets.
2. Spiders are arachnids that use their spinnerets to produce silk.
3. These
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -0.735  | 0.479509 | +0.000            |
| 2      | ' Yes'    | -2.235  | 0.106993 | +0.000            |
| 3      | ' **'     | -2.485  | 0.083326 | +0.000            |
| 4      | '<think>' | -2.610  | 0.073535 | +0.000            |
| 5      | ' No'     | -2.610  | 0.073535 | +0.000            |
| 6      | '8'       | -3.360  | 0.034736 | +0.000            |
| 7      | '0'       | -3.485  | 0.030654 | +0.000            |
| 8      | '2'       | -3.860  | 0.021068 | +0.000            |
| 9      | '3'       | -4.172  | 0.015414 | +0.000            |
| 10     | '4'       | -4.297  | 0.013603 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['$id', ' risposta', ' respuesta', 'preso', ' resposta', ' sy', "','=',$", ' answer']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `007_span_correction_sweep_inspan_seed0_C2.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['exampleInputEmail', ' Cari', '-valid', ' Stam', ' Whats', '()==', '\trestore', 'exampleInput']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' réponses', ' respuestas', ' respostas', ' resposta', ' پاسخ', 'getResponse']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`007_span_correction_sweep_inspan_seed0_C2.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
1. Yes, the animal known for spinning webs to catch insects has a mouth filled with food and a body covered in fur. 2. It is a
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -0.612  | 0.542520 | +0.123            |
| 2      | ' Yes'    | -1.987  | 0.137171 | +0.248            |
| 3      | '4'       | -2.862  | 0.057181 | +1.436            |
| 4      | '2'       | -3.174  | 0.041835 | +0.686            |
| 5      | '<think>' | -3.237  | 0.039300 | -0.627            |
| 6      | '8'       | -3.424  | 0.032581 | -0.064            |
| 7      | ' **'     | -3.487  | 0.030607 | -1.002            |
| 8      | '0'       | -3.799  | 0.022392 | -0.314            |
| 9      | ' No'     | -4.299  | 0.013582 | -1.689            |
| 10     | '3'       | -4.487  | 0.011260 | -0.314            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
