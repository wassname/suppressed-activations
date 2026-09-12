---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-456-g8975b76-dirty"
code_sha256: {"scripts/oat_sweep.py": "a47397201bc6cb14d2e4b6d29bde8b90509710e917ea5e41c012b09305a17d89", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5"
axis: "smoke_common_basis_norm2x2"
value: "delta_scaled_to_v_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: -0.5595703125
bare_answer_mass: 1.8078324501402676e-05
source_output: "Spider"
target_output: "Dog"
donor_p_target: 8.384078000744921e-07
donor_first_answer: null
donor_generation_tokens: 4
p_target: 9.477483331465919e-07
p_source: 1.713057645247318e-05
first_logits_sha256: {"base": "d31cea1f4173f5fecf17207af60c33325c71c6cc42557d7fc865ceb2663b6ea8", "donor": "d27d64f75ad0854e728cb5f7edf8739c7ac0fcd20d883cf10970bfa651f6760f", "steered": "5e9600000e00bcb69f12f3d130b6d5eb9298970604260f630ccb21f8c9e6d8b3"}
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "区别"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5/run.md"
last_decode_readout: ["gatsby", " guided"]
---

# 000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5`. Check those for
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
  "readout_positions": 2,
  "rank": 2,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 2,
  "strength": 2.5,
  "match_component_norm": true,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 2,
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
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null,
  "common_basis": "top8_union",
  "common_window": 2,
  "common_random_rank": 8,
  "common_seed": 0,
  "common_bank_layers": [
    0,
    2,
    4
  ],
  "common_removal": "pref",
  "common_inject_norm": "cross_v",
  "common_inject": "ref_delta",
  "common_inject_restricted": false,
  "sync_donor": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: what is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: what is the animal that barks and is called man's best friend called?\\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
campביטחarer neces
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' студент', '.k']
```

Base generation (first 4 of 4 tokens, verbatim):

```text
滹iated跖quia
```

Base next-token distribution:

| rank   | token       | log p   | p        | change in log p   |
|:-------|:------------|:--------|:---------|:------------------|
| 1      | '滹'         | -5.243  | 0.005285 | +0.000            |
| 2      | ' textView' | -5.368  | 0.004664 | +0.000            |
| 3      | ' קיש'      | -5.743  | 0.003206 | +0.000            |
| 4      | 'acked'     | -5.993  | 0.002497 | +0.000            |
| 5      | '(samples'  | -5.993  | 0.002497 | +0.000            |
| 6      | 'acr'       | -5.993  | 0.002497 | +0.000            |
| 7      | ' Lans'     | -5.993  | 0.002497 | +0.000            |
| 8      | '战士来说'      | -5.993  | 0.002497 | +0.000            |
| 9      | '的方法'       | -6.149  | 0.002135 | +0.000            |
| 10     | 'атель'     | -6.180  | 0.002070 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['�', '墨西哥']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['gatsby', ' guided']
```

Unmodified donor readout:

```python
['悄', ' Braz']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_common_basis_norm2x2_delta_scaled_to_v_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
区别_correction التش_continue
```

| rank   | token                    | log p   | p        | change in log p   |
|:-------|:-------------------------|:--------|:---------|:------------------|
| 1      | '区别'                     | -4.615  | 0.009900 | +3.784            |
| 2      | ' Wildlife'              | -5.678  | 0.003421 | +1.628            |
| 3      | ' sab'                   | -5.678  | 0.003421 | +2.721            |
| 4      | '倒是'                     | -5.678  | 0.003421 | +2.221            |
| 5      | '\tUInt'                 | -5.678  | 0.003421 | +3.378            |
| 6      | ' presentViewController' | -5.928  | 0.002664 | +2.034            |
| 7      | ' Csv'                   | -5.990  | 0.002503 | +2.190            |
| 8      | 'Congratulations'        | -5.990  | 0.002503 | +1.815            |
| 9      | ' numpy'                 | -5.990  | 0.002503 | +2.378            |
| 10     | ' Bul'                   | -6.053  | 0.002351 | +1.784            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
