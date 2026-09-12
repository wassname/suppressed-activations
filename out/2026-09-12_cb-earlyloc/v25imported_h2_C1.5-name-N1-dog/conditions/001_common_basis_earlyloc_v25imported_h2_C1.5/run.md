---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-526-gbaeb7d6-dirty"
code_sha256: {"scripts/oat_sweep.py": "e9f07e5d5ea377b9837087ce9a475363d155aa07038a5d218147d9c2063c06ed", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "001_common_basis_earlyloc_v25imported_h2_C1.5"
axis: "common_basis_earlyloc"
value: "v25imported_h2_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 8.203125
bare_answer_mass: 0.00038213966763578355
source_output: "Spider"
target_output: "Dog"
donor_p_target: 0.004396667238324881
donor_first_answer: null
donor_generation_tokens: 67
p_target: 2.2296251700026914e-05
p_source: 0.00035984342684969306
first_logits_sha256: {"base": "bceff1b7ef03d8c8bf90c2df6d7ba46556dd703cb0d455447dd5a674b0154aa5", "donor": "1197e6b2b381adde0742dc054109ef2ff36e7808f3f1a70d0483c76271fd5987", "steered": "dd711a69cb2f2a8f0cc274224712b253567844a181334693863ce2e8d1b540be"}
repeated_bigram_fraction: 0.9606299212598425
generation_tokens: 128
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/001_common_basis_earlyloc_v25imported_h2_C1.5/run.md"
last_decode_readout: ["_chance", " 고객센터", " követke", " pesante", " Kompetenz", " agradável", "ookie", "ご紹介"]
---

# 001_common_basis_earlyloc_v25imported_h2_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_common_basis_earlyloc_v25imported_h2_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 3,
  "strength": 1.5,
  "match_component_norm": false,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 0,
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
  "future_lexical_union": false,
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null,
  "common_basis": "top8_union",
  "common_window": 4,
  "common_random_rank": 8,
  "common_seed": 0,
  "common_bank_layers": [
    23,
    25,
    32
  ],
  "common_selector": "increment",
  "common_donor_rank": 8,
  "xdepth_anchor_layer": 25,
  "xdepth_norm_from_layer": -1,
  "common_removal": "joint",
  "removal_only": false,
  "common_inject_norm": "own",
  "common_inject": "pd_d",
  "common_inject_restricted": false,
  "sync_donor": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Which animal is known for spinning webs to catch insects?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Which animal is known for barking while living as a domesticated pet?\nAnswer: '
```

Unmodified donor generation (first 32 of 67 tokens, verbatim):

```text
狗 (Dog)

The dog is a highly social and intelligent mammal that has been domesticated by humans for thousands of years. They are renowned for their
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['Budget', ' yummy', '拉丝', '.ExecuteNonQuery', ' harap', ' urbano', ' mdi', 'Mbps']
```

Base generation (first 32 of 60 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid that lives in various environments, from forests to urban areas. It creates intricate webs to trap prey,
```

Base next-token distribution:

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'       | -0.295  | 0.744515 | +0.000            |
| 2      | '蛛'        | -2.795  | 0.061114 | +0.000            |
| 3      | ' Spider'  | -3.295  | 0.037067 | +0.000            |
| 4      | 'Spider'   | -3.420  | 0.032712 | +0.000            |
| 5      | ' spider'  | -3.858  | 0.021120 | +0.000            |
| 6      | '8'        | -3.983  | 0.018639 | +0.000            |
| 7      | ' The'     | -4.608  | 0.009977 | +0.000            |
| 8      | '1'        | -4.608  | 0.009977 | +0.000            |
| 9      | ' spiders' | -4.733  | 0.008804 | +0.000            |
| 10     | ' **'      | -5.358  | 0.004713 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['terrain', ' terrain', '神经痛', 'params', ' terreno', 'naires', ' PEOPLE', ' семейства']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_common_basis_earlyloc_v25imported_h2_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['_chance', ' 고객센터', ' követke', ' pesante', ' Kompetenz', ' agradável', 'ookie', 'ご紹介']
```

Unmodified donor readout:

```python
[' chien', 'Fetch', 'fetch', ' Hunde', ' perros', ' собаки', ' кино', ' retrie']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_common_basis_earlyloc_v25imported_h2_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
1: 1: 1: 1: 1, 1, 1, 1, 1, 1, 1,
```

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | '1'          | -0.930  | 0.394616 | +3.678            |
| 2      | '<think>'    | -2.242  | 0.106210 | +4.053            |
| 3      | '\n'         | -2.992  | 0.050170 | +9.553            |
| 4      | '<|im_end|>' | -3.242  | 0.039072 | +7.021            |
| 5      | ' '          | -3.555  | 0.028586 | +4.615            |
| 6      | '回答'         | -3.617  | 0.026854 | +8.334            |
| 7      | 'Answer'     | -3.930  | 0.019647 | +8.584            |
| 8      | '3'          | -3.992  | 0.018456 | +3.240            |
| 9      | '\n\n'       | -4.117  | 0.016288 | +4.115            |
| 10     | '答案'         | -4.180  | 0.015301 | +3.178            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
