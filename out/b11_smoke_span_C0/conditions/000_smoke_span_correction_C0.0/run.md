---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-337-gd9b542c-dirty"
code_sha256: {"scripts/oat_sweep.py": "a924633334e7499633bca318c04e0af4d1face3f15f0d8d04931941d579aec75", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_span_correction_C0.0"
axis: "smoke_span_correction"
value: "C0.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 0.0
bare_answer_mass: 6.648635007877601e-06
source_output: "Spider"
target_output: "Dog"
donor_p_target: 7.952911573738675e-07
donor_first_answer: null
donor_generation_tokens: 4
p_target: 5.73421402805252e-07
p_source: 6.075213605072349e-06
first_logits_sha256: {"base": "fa3285391491651c1057d4cd10e3841dfcbdb16ff592ca47e44ef185c1262dd6", "donor": "3fb17c1e35842db3dbe8e6d4451cb297759568e56609c115f4467847f788e777", "steered": "fa3285391491651c1057d4cd10e3841dfcbdb16ff592ca47e44ef185c1262dd6"}
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "acked"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
log: "conditions/000_smoke_span_correction_C0.0/run.md"
last_decode_readout: ["enz", " Púb", " hotspot", "between", "行政区", "查找", " roadmap", " wins"]
---

# 000_smoke_span_correction_C0.0

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
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
  "span_correction": true
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that barks and is called man's best friend called?\\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
campביטח壯SSH
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
['.Matrix', ' студент', 'apps', '$id', 'พรร', '查找', ' DEN', '悄']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_span_correction_C0.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['enz', ' Púb', ' hotspot', 'between', '行政区', '查找', ' roadmap', ' wins']
```

Unmodified donor readout:

```python
['悄', 'arms', 'ᴴ', '😤', ' fileSize', '.oauth', ' Braz', ' ISSN']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_span_correction_C0.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
acked �Annotationsaced
```

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

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
