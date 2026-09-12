---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-526-gbaeb7d6-dirty"
code_sha256: {"scripts/oat_sweep.py": "e9f07e5d5ea377b9837087ce9a475363d155aa07038a5d218147d9c2063c06ed", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "003_common_basis_earlyloc_v25imported_h8_C1.5"
axis: "common_basis_earlyloc"
value: "v25imported_h8_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "6"
swap_log_odds_shift: -1.125
bare_answer_mass: 0.982873797416687
source_output: "8"
target_output: "6"
donor_p_target: 0.9452986121177673
donor_first_answer: "6"
donor_generation_tokens: 64
p_target: 0.004530627280473709
p_source: 0.9783431887626648
first_logits_sha256: {"base": "604fae9f54c39f1fc5b5a6c433d9160b17d5a1beb774519a2ef291c1e0e4fe58", "donor": "280901d76e7c0f8808520fe304f90a2913074a8944052a99d05a3d7900089793", "steered": "fe799f844e35cf3dba19b479d37ee2c78b97086c24ad51a234ffa1dd85e7ce67"}
repeated_bigram_fraction: 0.027027027027026973
generation_tokens: 76
first_token: "8"
first_answer: "8"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/003_common_basis_earlyloc_v25imported_h8_C1.5/run.md"
last_decode_readout: [" víz", "ทัน", " koń", " trien", " **○", " srl", " Jeudi", " первым"]
---

# 003_common_basis_earlyloc_v25imported_h8_C1.5

Expected Base answer: `8`. Expected donor-directed answer:
`6`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_common_basis_earlyloc_v25imported_h8_C1.5`. Check those for
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
    8
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: An animal known for spinning webs to catch insects has how many legs?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: An animal known for living in colonies and following pheromone trails has how many legs?\nAnswer: '
```

Unmodified donor generation (first 32 of 64 tokens, verbatim):

```text
6

The animal described is an ant, which is a social insect that lives in large, organized colonies. These insects communicate primarily through chemical signals called pher
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['_disc', '_target', 'هام', 'Taylor', ' cream', '枉', 'må', ' laba']
```

Base generation (first 32 of 62 tokens, verbatim):

```text
8

The spider is an arachnid that possesses eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing vibrations
```

Base next-token distribution:

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.028  | 0.972707 | +0.000            |
| 2      | '6'     | -4.278  | 0.013875 | +0.000            |
| 3      | '4'     | -4.778  | 0.008416 | +0.000            |
| 4      | '1'     | -6.278  | 0.001878 | +0.000            |
| 5      | '2'     | -7.028  | 0.000887 | +0.000            |
| 6      | '3'     | -7.278  | 0.000691 | +0.000            |
| 7      | '0'     | -8.028  | 0.000326 | +0.000            |
| 8      | '5'     | -8.153  | 0.000288 | +0.000            |
| 9      | 'Eight' | -8.403  | 0.000224 | +0.000            |
| 10     | '7'     | -8.653  | 0.000175 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['_disc', 'Taylor', 'هام', ' laba', ' comem', 'مبر', 'må', ' WEB']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_common_basis_earlyloc_v25imported_h8_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' víz', 'ทัน', ' koń', ' trien', ' **○', ' srl', ' Jeudi', ' первым']
```

Unmodified donor readout:

```python
['前景', '_target', '枉', ' городу', '////////////////////////////////////////////////////////////', ' fungerer', ' vaya', ' vor']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_common_basis_earlyloc_v25imported_h8_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 76 tokens, verbatim):

```text
8

The spider is an arachnid that possesses eight legs, which it uses to walk, sense vibrations, and manipulate its silk. Unlike insects, which
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.022  | 0.978343 | +0.006            |
| 2      | '4'     | -4.272  | 0.013955 | +0.506            |
| 3      | '6'     | -5.397  | 0.004531 | -1.119            |
| 4      | '1'     | -6.897  | 0.001011 | -0.619            |
| 5      | '3'     | -7.522  | 0.000541 | -0.244            |
| 6      | '2'     | -7.522  | 0.000541 | -0.494            |
| 7      | 'Eight' | -8.022  | 0.000328 | +0.381            |
| 8      | '0'     | -8.522  | 0.000199 | -0.494            |
| 9      | '5'     | -8.647  | 0.000176 | -0.494            |
| 10     | '7'     | -8.897  | 0.000137 | -0.244            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
