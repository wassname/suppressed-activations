---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-526-gbaeb7d6-dirty"
code_sha256: {"scripts/oat_sweep.py": "e9f07e5d5ea377b9837087ce9a475363d155aa07038a5d218147d9c2063c06ed", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "006_common_basis_earlyloc_siterescaled_h3_C1.5"
axis: "common_basis_earlyloc"
value: "siterescaled_h3_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Ant"
swap_log_odds_shift: 2.125000476837158
bare_answer_mass: 0.7222139239311218
source_output: "Spider"
target_output: "Ant"
donor_p_target: 0.002417853334918618
donor_first_answer: null
donor_generation_tokens: 81
p_target: 0.0002921222767326981
p_source: 0.7219218015670776
first_logits_sha256: {"base": "bceff1b7ef03d8c8bf90c2df6d7ba46556dd703cb0d455447dd5a674b0154aa5", "donor": "d78c4e5463f982cbcfb9c17f79aab901e2bfbff4e723415041798b4bebe0c68b", "steered": "56cec1eb5a09c4abaea84ff0393f9970a230790f9b7403a32cdbf53c2c2f54e7"}
repeated_bigram_fraction: 0.018867924528301883
generation_tokens: 55
first_token: "Spider"
first_answer: "Spider"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/006_common_basis_earlyloc_siterescaled_h3_C1.5/run.md"
last_decode_readout: [" التالية", "他們的", "bito", "饮用水", " Municipio", "พวกเข", "宣伝", "€."]
---

# 006_common_basis_earlyloc_siterescaled_h3_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Ant`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `006_common_basis_earlyloc_siterescaled_h3_C1.5`. Check those for
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
    3
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
  "xdepth_anchor_layer": -1,
  "xdepth_norm_from_layer": 25,
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Which animal is known for living in colonies and following pheromone trails?\nAnswer: '
```

Unmodified donor generation (first 32 of 81 tokens, verbatim):

```text
蚂蚁 (Ants)

Ants are social insects that live in large, organized colonies with a distinct hierarchy of workers, soldiers, and queens. They communicate
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
['Budget', 'ธานี', 'くださ', ' textiles', '拉丝', ' feste', 'ონ', ' weaving']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `006_common_basis_earlyloc_siterescaled_h3_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' التالية', '他們的', 'bito', '饮用水', ' Municipio', 'พวกเข', '宣伝', '€.']
```

Unmodified donor readout:

```python
[' sosyal', 'Social', ' соци', ' iterable', ' социального', ' regal', '社交', '社交媒体']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`006_common_basis_earlyloc_siterescaled_h3_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 55 tokens, verbatim):

```text
Spider

A spider is a small arachnid that lives in various environments, including on land, in water, and in the air. They are known for
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'Spider'   | -0.326  | 0.721922 | +3.094            |
| 2      | 'Sp'       | -2.201  | 0.110710 | +7.500            |
| 3      | 'The'      | -3.138  | 0.043355 | +7.469            |
| 4      | ' Sp'      | -4.013  | 0.018073 | +1.594            |
| 5      | ' Spider'  | -4.138  | 0.015949 | -0.843            |
| 6      | ' The'     | -4.138  | 0.015949 | +0.469            |
| 7      | ' **'      | -4.451  | 0.011669 | +0.907            |
| 8      | '蜘蛛'       | -4.888  | 0.007534 | -4.593            |
| 9      | ' spiders' | -4.888  | 0.007534 | -0.156            |
| 10     | 'Sil'      | -4.951  | 0.007077 | +6.407            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
