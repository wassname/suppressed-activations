---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-368-g0dbcfbf"
code_sha256: {"scripts/oat_sweep.py": "a2998b28a8f472d33790287cc8db978dd0ca4468259ce548edc59afe66d22095", "scripts/demo.py": "87d5e8eb717cb8b20ab521ed065697dcdf04865df35e14f8c243b30b4d306467", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_two_site_prop-dog"
axis: "two_site"
value: "prop-dog"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 10.648436546325684
bare_answer_mass: 0.008978171274065971
source_output: "No"
target_output: "Yes"
donor_p_target: 0.0018025756580755115
donor_first_answer: null
donor_generation_tokens: 62
p_target: 0.008978109806776047
p_source: 6.10603905215612e-08
first_logits_sha256: {"base": "6c17cd71674ef2b347d34e8efddc9173a282a412025ef371edeb47d2f064ce1b", "donor": "19039e2a96829cc819be2815976464a3267b97a90770f0669059f0c5c177b6e0", "steered": "73017d7e89cf15eaced25d9a840e4126147f59a3d798a6a42881edbcd4df5870"}
repeated_bigram_fraction: 0.984251968503937
generation_tokens: 128
first_token: "是的"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.5
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/000_two_site_prop-dog/run.md"
last_decode_readout: ["-ref", " تنا", ".lin", " سو", "Documents", "碗中", " Chol", " Réd"]
---

# 000_two_site_prop-dog

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_two_site_prop-dog`. Check those for
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
  "answer_patch_layer": 26
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
[' risposta', ' respuesta', ' Erik', '_non', ' contradictions', ' respuestas', ' resposta', ' sụt']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_two_site_prop-dog`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['-ref', ' تنا', '.lin', ' سو', 'Documents', '碗中', ' Chol', ' Réd']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', ' respuestas', 'getResponse', ' cpt', ' resposta', ' response', ' respond']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_two_site_prop-dog`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，是的，
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '是的'      | -1.025  | 0.358629 | +4.060            |
| 2      | '1'       | -1.275  | 0.279301 | +0.310            |
| 3      | ' Yes'    | -2.775  | 0.062320 | -0.065            |
| 4      | '<think>' | -2.775  | 0.062320 | -0.815            |
| 5      | '是'       | -2.775  | 0.062320 | +3.935            |
| 6      | '2'       | -2.963  | 0.051665 | +0.685            |
| 7      | '5'       | -3.713  | 0.024405 | +0.248            |
| 8      | '3'       | -4.525  | 0.010830 | -0.690            |
| 9      | '4'       | -4.525  | 0.010830 | -0.002            |
| 10     | 'Yes'     | -4.713  | 0.008978 | +3.498            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
