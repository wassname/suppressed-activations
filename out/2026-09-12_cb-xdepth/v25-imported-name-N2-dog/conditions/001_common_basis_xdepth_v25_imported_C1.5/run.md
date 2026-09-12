---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-504-g15c44dc"
code_sha256: {"scripts/oat_sweep.py": "6077e14d2360c4c737e4e2863ce3b67edd0749011db5da881a25229e6a835f16", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "6a8c8a1f9d19be74bb1fe42824ccaf6feecf33a21db4fe06986a1d43752d5015"}
condition_id: "001_common_basis_xdepth_v25_imported_C1.5"
axis: "common_basis_xdepth"
value: "v25_imported_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: -0.34375
bare_answer_mass: 0.05258537828922272
source_output: "Spider"
target_output: "Dog"
donor_p_target: 0.015015699900686741
donor_first_answer: null
donor_generation_tokens: 59
p_target: 4.70097432980765e-07
p_source: 0.05258490890264511
first_logits_sha256: {"base": "cc25b9a0722ee874c2c86ae7942eb501c2a6f7f92a4d18e01b2bd5093a69cbdb", "donor": "ac874a9acbda1ec84fd61d05c846f2399056a769d9defc82b8e16d89b02f0871", "steered": "e0c1662f75a7e226e6f4053bbc7339c8076221f561a6956f5449971b2d59ea77"}
repeated_bigram_fraction: 0.0
generation_tokens: 74
first_token: " Spider"
first_answer: "Spider"
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/001_common_basis_xdepth_v25_imported_C1.5/run.md"
last_decode_readout: [" koń", " Direktor", " trien", " srl", " Directeur", " контролю", "_PP", " Incluí"]
---

# 001_common_basis_xdepth_v25_imported_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_common_basis_xdepth_v25_imported_C1.5`. Check those for
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
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: spinning webs to catch insects?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What animal matches this description: barking while living as a domesticated pet?\nAnswer: '
```

Unmodified donor generation (first 32 of 59 tokens, verbatim):

```text
1. The dog.
2. The dog is a highly social and intelligent mammal known for its ability to communicate with humans through barking.
3
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['Budget', ' yummy', '.ExecuteNonQuery', 'Mbps', '拉丝', ' urbano', ' mdi', ' harap']
```

Base generation (first 32 of 63 tokens, verbatim):

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to trap prey. It uses silk threads to create a sticky
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '蜘蛛'      | -1.557  | 0.210828 | +0.000            |
| 2      | ' Spider' | -1.744  | 0.174782 | +0.000            |
| 3      | '1'       | -2.369  | 0.093554 | +0.000            |
| 4      | '8'       | -2.432  | 0.087886 | +0.000            |
| 5      | 'Spider'  | -2.994  | 0.050076 | +0.000            |
| 6      | '蛛'       | -3.244  | 0.038999 | +0.000            |
| 7      | ' **'     | -3.244  | 0.038999 | +0.000            |
| 8      | ' Sp'     | -3.619  | 0.026804 | +0.000            |
| 9      | ' spider' | -3.682  | 0.025180 | +0.000            |
| 10     | '2'       | -3.744  | 0.023654 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['Mbps', 'Budget', ' yummy', '拉丝', '.ExecuteNonQuery', ' urbano', ' feste', ' ინ']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_common_basis_xdepth_v25_imported_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' koń', ' Direktor', ' trien', ' srl', ' Directeur', ' контролю', '_PP', ' Incluí']
```

Unmodified donor readout:

```python
[' chien', 'Fetch', ' собаки', ' Hunde', 'fetch', ' кино', ' perros', ' labs']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_common_basis_xdepth_v25_imported_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 74 tokens, verbatim):

```text
 Spider

Spiders are arachnids characterized by their eight legs and venomous fangs used to subdue prey. They are renowned for their ability to
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | ' Spider' | -1.508  | 0.221391 | +0.236            |
| 2      | ' **'     | -2.133  | 0.118502 | +1.111            |
| 3      | '1'       | -2.195  | 0.111322 | +0.174            |
| 4      | '8'       | -2.383  | 0.092289 | +0.049            |
| 5      | ' Sp'     | -2.820  | 0.059587 | +0.799            |
| 6      | '蜘蛛'      | -2.883  | 0.055976 | -1.326            |
| 7      | 'Spider'  | -2.945  | 0.052585 | +0.049            |
| 8      | ' The'    | -3.195  | 0.040953 | +0.924            |
| 9      | '2'       | -3.445  | 0.031894 | +0.299            |
| 10     | '<think>' | -3.570  | 0.028147 | +0.174            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
