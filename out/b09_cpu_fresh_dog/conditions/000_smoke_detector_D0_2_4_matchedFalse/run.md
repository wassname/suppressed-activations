---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-333-g413e8a9-dirty"
code_sha256: {"scripts/oat_sweep.py": "424df00d404ab28ee217a40ad28eef0de85ec37781e84b378f5c23cf04dd8d05", "scripts/demo.py": "3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_detector_D0_2_4_matchedFalse"
axis: "smoke_detector"
value: "D0_2_4_matchedFalse"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: -0.5263671875
bare_answer_mass: 5.621996024274267e-06
source_output: "Spider"
target_output: "Dog"
donor_p_target: 1.4115861404206953e-06
donor_first_answer: null
donor_generation_tokens: 4
p_target: 2.96920234177378e-07
p_source: 5.325076017470565e-06
first_logits_sha256: {"base": "fa3285391491651c1057d4cd10e3841dfcbdb16ff592ca47e44ef185c1262dd6", "donor": "01f41e4585b5938a3e38d230b5b401bec8b8e6596e264b380e1a9f26c2ec3b58", "steered": "74722f20c99de19cd8abd534ebfcfa678157b1dbca4209494e2f77537c11e588"}
repeated_bigram_fraction: 0.6666666666666667
generation_tokens: 4
first_token: "атель"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
log: "conditions/000_smoke_detector_D0_2_4_matchedFalse/run.md"
last_decode_readout: ["욜", "懋", " 이후", "纸质", "HEEL", " typo", "裼", " threatening"]
---

# 000_smoke_detector_D0_2_4_matchedFalse

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_smoke_detector_D0_2_4_matchedFalse`. Check those for
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
  "strength": 2.0,
  "match_component_norm": false,
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
  "template_state_span": "none",
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
  "future_lexical_union": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that barks and is called man's best friend called?\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
_CHARellery BAL"In
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['.Matrix', ' студент', 'apps', '$id', 'พรร', '查找', ' DEN', '悄']
```

Base generation (first 4 of 4 tokens, verbatim):

```text
acked �Annotationsaced
```

Base next-token distribution:

| rank   | token          | log p   | p        | change in log p   |
|:-------|:---------------|:--------|:---------|:------------------|
| 1      | 'acked'        | -5.355  | 0.004724 | +0.000            |
| 2      | '滹'            | -5.418  | 0.004438 | +0.000            |
| 3      | ' stimulating' | -5.730  | 0.003247 | +0.000            |
| 4      | '战士来说'         | -5.730  | 0.003247 | +0.000            |
| 5      | 'ではなく'         | -5.918  | 0.002692 | +0.000            |
| 6      | ' textView'    | -5.918  | 0.002692 | +0.000            |
| 7      | ' samt'        | -5.980  | 0.002529 | +0.000            |
| 8      | 'dirname'      | -6.043  | 0.002376 | +0.000            |
| 9      | ' קיש'         | -6.043  | 0.002376 | +0.000            |
| 10     | 'Fit'          | -6.043  | 0.002376 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['$id', ' Measurements', '.Matrix', '的道理', '查找', '莹', 'zeichnet', ' Wikimedia']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_detector_D0_2_4_matchedFalse`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['욜', '懋', ' 이후', '纸质', 'HEEL', ' typo', '裼', ' threatening']
```

Unmodified donor readout:

```python
['ᴴ', ' Braz', '悄', 'uctor', '了一场', 'arms', '.Matrix', ' Phantom']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_detector_D0_2_4_matchedFalse`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
ательательательатель
```

| rank   | token          | log p   | p        | change in log p   |
|:-------|:---------------|:--------|:---------|:------------------|
| 1      | 'атель'        | -4.815  | 0.008108 | +1.446            |
| 2      | '_MATCH'       | -5.190  | 0.005572 | +1.853            |
| 3      | '战士来说'         | -5.252  | 0.005235 | +0.478            |
| 4      | ' textView'    | -5.252  | 0.005235 | +0.665            |
| 5      | ' neces'       | -5.440  | 0.004340 | +1.415            |
| 6      | '(samples'     | -5.752  | 0.003175 | +0.353            |
| 7      | ' stimulating' | -5.877  | 0.002802 | -0.147            |
| 8      | '].['          | -5.940  | 0.002632 | +0.478            |
| 9      | 'aac'          | -6.002  | 0.002473 | +0.665            |
| 10     | 'resolution'   | -6.127  | 0.002182 | +0.478            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
