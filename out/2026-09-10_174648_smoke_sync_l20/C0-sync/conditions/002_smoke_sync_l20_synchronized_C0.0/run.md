---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-388-g2259631-dirty"
code_sha256: {"scripts/oat_sweep.py": "8a696a9cbc02e354490515b583bab29f425ebbe0ea61a0784896ff475831ad4f", "scripts/demo.py": "219bacf5efcdb4456e8f5bd1004013821af28dde0eb5c22451981711054d03c9", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_smoke_sync_l20_synchronized_C0.0"
axis: "smoke_sync_l20"
value: "synchronized_C0.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first."
extraction_instruction: "Answer the question with the answer first."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 0.0
bare_answer_mass: 8.822426025290042e-06
source_output: "Spider"
target_output: "Dog"
donor_p_target: 3.4234872714478115e-07
donor_first_answer: null
donor_generation_tokens: 6
p_target: 9.848296258496703e-07
p_source: 7.837596058379859e-06
first_logits_sha256: {"base": "b90cd04e6b1e344024026a9e50ca4e6b63b0aec93d4074b38794dbca9783739b", "donor": "0e5f59edb6b27581ae2c9bfe04adf0732c210a0947f2cb808872c2489d816a4b", "steered": "b90cd04e6b1e344024026a9e50ca4e6b63b0aec93d4074b38794dbca9783739b"}
repeated_bigram_fraction: 0.0
generation_tokens: 6
first_token: " textView"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/002_smoke_sync_l20_synchronized_C0.0/run.md"
last_decode_readout: [" slammed", "contra", "🚚", "预售", ".FindControl", "()',", " Georg", " research"]
---

# 002_smoke_sync_l20_synchronized_C0.0

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_smoke_sync_l20_synchronized_C0.0`. Check those for
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
    5
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 3,
  "strength": 0.0,
  "match_component_norm": false,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 2,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "synchronized",
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
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that barks and is called man's best friend called?\nAnswer: "
```

Unmodified donor generation (first 6 of 6 tokens, verbatim):

```text
%),加强对 JS jugg猃TeX
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' Sw', 'isma', ' Braz', '首都', 'Adv', 'arms', 'Summer', '了一场']
```

Base generation (first 6 of 6 tokens, verbatim):

```text
 textView克思רוץ县委书记拄民政局
```

Base next-token distribution:

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | ' textView'  | -4.147  | 0.015809 | +0.000            |
| 2      | 'aac'        | -4.335  | 0.013106 | +0.000            |
| 3      | 'атель'      | -4.772  | 0.008462 | +0.000            |
| 4      | ' timelines' | -5.085  | 0.006191 | +0.000            |
| 5      | ' קיש'       | -5.085  | 0.006191 | +0.000            |
| 6      | ' neces'     | -5.272  | 0.005132 | +0.000            |
| 7      | '%%%'        | -5.522  | 0.003997 | +0.000            |
| 8      | "+'&"        | -5.585  | 0.003755 | +0.000            |
| 9      | 'annotate'   | -5.647  | 0.003527 | +0.000            |
| 10     | '荔'          | -5.710  | 0.003314 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' Sw', 'isma', ' Braz', '首都', 'Adv', 'arms', 'Summer', '了一场']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_smoke_sync_l20_synchronized_C0.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' slammed', 'contra', '🚚', '预售', '.FindControl', "()',", ' Georg', ' research']
```

Unmodified donor readout:

```python
['arden', '.isVisible', ' מכל', '😤', ' several', '转身', 'arms', 'KO']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_smoke_sync_l20_synchronized_C0.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 6 of 6 tokens, verbatim):

```text
 textView克思רוץ县委书记拄民政局
```

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | ' textView'  | -4.147  | 0.015809 | +0.000            |
| 2      | 'aac'        | -4.335  | 0.013106 | +0.000            |
| 3      | 'атель'      | -4.772  | 0.008462 | +0.000            |
| 4      | ' timelines' | -5.085  | 0.006191 | +0.000            |
| 5      | ' קיש'       | -5.085  | 0.006191 | +0.000            |
| 6      | ' neces'     | -5.272  | 0.005132 | +0.000            |
| 7      | '%%%'        | -5.522  | 0.003997 | +0.000            |
| 8      | "+'&"        | -5.585  | 0.003755 | +0.000            |
| 9      | 'annotate'   | -5.647  | 0.003527 | +0.000            |
| 10     | '荔'          | -5.710  | 0.003314 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
