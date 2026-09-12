---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-526-gbaeb7d6-dirty"
code_sha256: {"scripts/oat_sweep.py": "e9f07e5d5ea377b9837087ce9a475363d155aa07038a5d218147d9c2063c06ed", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "000_common_basis_earlyloc_v25imported_h1_C1.5"
axis: "common_basis_earlyloc"
value: "v25imported_h1_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "6"
swap_log_odds_shift: -1.9375
bare_answer_mass: 0.153646782040596
source_output: "8"
target_output: "6"
donor_p_target: 0.9496665000915527
donor_first_answer: "6"
donor_generation_tokens: 55
p_target: 0.0008534964290447533
p_source: 0.152793288230896
first_logits_sha256: {"base": "2973d67df11a211a4fa625d5493b79e8f5c91c266e76b455d56868bf0b743696", "donor": "340ecb1084898f146eec088eeb9b3aa48b8b01467d206c2054cc7a2f5e34def6", "steered": "a2cdd126ad96e42bd06bf7b51012ede43ca47a1f982d08596cbaca535eb5d168"}
repeated_bigram_fraction: 0.984251968503937
generation_tokens: 128
first_token: "8"
first_answer: "8"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/000_common_basis_earlyloc_v25imported_h1_C1.5/run.md"
last_decode_readout: ["ą", "lists", " Karlsruhe", "رسی", "んじゃない", " possíveis", "င်း", "知りたい"]
---

# 000_common_basis_earlyloc_v25imported_h1_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`6`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_common_basis_earlyloc_v25imported_h1_C1.5`. Check those for
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
    1
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal known for spinning webs to catch insects have?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal known for living in colonies and following pheromone trails have?\nAnswer: '
```

Unmodified donor generation (first 32 of 55 tokens, verbatim):

```text
6

The animal is an ant, a small insect that lives in complex social colonies. These insects communicate primarily through chemical signals called pheromones to coordinate
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' comem', '_disc', 'Taylor', ' cream', '.ExecuteNonQuery', ' harap', 'web', 'هام']
```

Base generation (first 32 of 63 tokens, verbatim):

```text
8

The spider is an arachnid that typically has eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing
```

Base next-token distribution:

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.067  | 0.935530 | +0.000            |
| 2      | '6'     | -3.317  | 0.036274 | +0.000            |
| 3      | '4'     | -3.817  | 0.022002 | +0.000            |
| 4      | '1'     | -6.192  | 0.002046 | +0.000            |
| 5      | '3'     | -6.692  | 0.001241 | +0.000            |
| 6      | '2'     | -6.942  | 0.000967 | +0.000            |
| 7      | '0'     | -7.817  | 0.000403 | +0.000            |
| 8      | '5'     | -8.067  | 0.000314 | +0.000            |
| 9      | 'Eight' | -8.192  | 0.000277 | +0.000            |
| 10     | '八'     | -8.504  | 0.000203 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['关键时刻', ' mdi', ' зарег', ' webView', ' 인프라', ' feste', '居委会', ' عمران']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_common_basis_earlyloc_v25imported_h1_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['ą', 'lists', ' Karlsruhe', 'رسی', 'んじゃない', ' possíveis', 'င်း', '知りたい']
```

Unmodified donor readout:

```python
['Social', ' sociales', ' vaya', 'social', ' división', ' городу', 'IM', '////////////////////////////////////////////////////////////']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_common_basis_earlyloc_v25imported_h1_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 128 tokens, verbatim):

```text
8

8

8

8

8

8

8

8

8

8

8

8

8

8

8

8


```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | ' An'    | -1.879  | 0.152793 | +12.688           |
| 2      | '8'      | -1.879  | 0.152793 | -1.812            |
| 3      | ' A'     | -2.379  | 0.092674 | +13.000           |
| 4      | 'An'     | -2.379  | 0.092674 | +17.719           |
| 5      | ' '      | -2.504  | 0.081784 | +9.813            |
| 6      | ' **'    | -2.879  | 0.056210 | +7.813            |
| 7      | 'A'      | -3.066  | 0.046599 | +17.688           |
| 8      | 'Eight'  | -3.066  | 0.046599 | +5.125            |
| 9      | ' Eight' | -3.129  | 0.043776 | +5.625            |
| 10     | 'The'    | -4.004  | 0.018249 | +14.063           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
