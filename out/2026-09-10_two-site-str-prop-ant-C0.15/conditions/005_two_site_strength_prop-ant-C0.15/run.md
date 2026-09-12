---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-371-gf1b5147"
code_sha256: {"scripts/oat_sweep.py": "34915734a4b1ba943468c5fffd5ce03c6c2d393ee5215c2f7ff29cc4b6dc4bee", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "005_two_site_strength_prop-ant-C0.15"
axis: "two_site_strength"
value: "prop-ant-C0.15"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 0.2499995231628418
bare_answer_mass: 0.003271514782682061
source_output: "No"
target_output: "Yes"
donor_p_target: 0.000990669010207057
donor_first_answer: null
donor_generation_tokens: 83
p_target: 0.0031696271616965532
p_source: 0.00010188754822593182
first_logits_sha256: {"base": "a6c25cf5e3bc868a2bd9256c17574a57786349a844bded183a96ad4009ed10a6", "donor": "244dd902b8d9e7c73b892e25e3e7b946276d3384f79fc937812a167e7e3a8103", "steered": "09e61ddbd428e7ae214ac0dc4e144a3b15c8c4444fdd720b2d3f43cb8e104e48"}
repeated_bigram_fraction: 0.027027027027026973
generation_tokens: 76
first_token: " Yes"
first_answer: "Yes"
mentions_spins_webs: false
readout_overlap: 0.625
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/005_two_site_strength_prop-ant-C0.15/run.md"
last_decode_readout: [" Малень", " μικ", "してた", " cari", " کوچک", " pequeño", " kecil", " piccoli"]
---

# 005_two_site_strength_prop-ant-C0.15

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `005_two_site_strength_prop-ant-C0.15`. Check those for
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
    20,
    26
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
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": 26,
  "answer_patch_strength": 0.15
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
[' risposta', ' respuesta', ' Kraft', ' respuestas', ' resposta', ' respostas', ' réponses', '[__']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `005_two_site_strength_prop-ant-C0.15`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' Малень', ' μικ', 'してた', ' cari', ' کوچک', ' pequeño', ' kecil', ' piccoli']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' response', ' respuestas', ' respond', ' resposta', '_response', ' réponses']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`005_two_site_strength_prop-ant-C0.15`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 76 tokens, verbatim):

```text
 Yes.

The ant is a small, social insect known for its ability to communicate through pheromones and its highly developed sense of smell. It possesses
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Yes'    | -1.254  | 0.285321 | +0.703            |
| 2      | ' No'     | -1.504  | 0.222208 | +0.828            |
| 3      | '1'       | -1.504  | 0.222208 | -0.297            |
| 4      | '<think>' | -2.504  | 0.081746 | -0.547            |
| 5      | ' **'     | -2.629  | 0.072140 | +1.141            |
| 6      | '3'       | -3.817  | 0.022002 | -0.422            |
| 7      | '0'       | -3.879  | 0.020669 | -1.047            |
| 8      | '2'       | -4.004  | 0.018240 | -0.734            |
| 9      | '5'       | -5.004  | 0.006710 | -1.484            |
| 10     | '4'       | -5.067  | 0.006304 | -1.047            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
