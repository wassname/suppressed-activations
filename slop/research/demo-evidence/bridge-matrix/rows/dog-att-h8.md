# dog-att-h8

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: identity changed to dog but answer stayed 8 (answer-source/name-target mismatch); invented male; vague US-popularity claim.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [8], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "attenuation", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 37 (cap 128) — EOS count: 0
- canonical r2 (non-special IDs): None

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

The donor input (rendered; used only to extract the component):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that barks and is called man's best friend have?\nAnswer: "
```

## Readout / top tokens at the first generated position

```json
[{"token_id": 23, "token": "8", "logp": -0.07802534103393555, "p": 0.9249410033226013, "delta_logp": 0.006264910101890564}, {"token_id": 19, "token": "4", "logp": -2.9530253410339355, "p": 0.05218159779906273, "delta_logp": 0.13126492500305176}, {"token_id": 21, "token": "6", "logp": -4.9530253410339355, "p": 0.007062011864036322, "delta_logp": -1.3687350749969482}, {"token_id": 17, "token": "2", "logp": -5.4530253410339355, "p": 0.004283326677978039, "delta_logp": 1.2562646865844727}, {"token_id": 16, "token": "1", "logp": -5.5780253410339355, "p": 0.00378002249635756, "delta_logp": 0.7562646865844727}, {"token_id": 15, "token": "0", "logp": -5.7030253410339355, "p": 0.0033358579967170954, "delta_logp": 1.7562646865844727}, {"token_id": 18, "token": "3", "logp": -6.2030253410339355, "p": 0.0020233001559972763, "delta_logp": -0.11873531341552734}, {"token_id": 22, "token": "7", "logp": -7.2030253410339355, "p": 0.0007443305803462863, "delta_logp": 0.7562646865844727}, {"token_id": 20, "token": "5", "logp": -7.7655253410339355, "p": 0.0004241067508701235, "delta_logp": 0.06876468658447266}, {"token_id": 24, "token": "9", "logp": -7.8280253410339355, "p": 0.00039841141551733017, "delta_logp": 1.2562651634216309}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal described is a dog, specifically a male who is likely to be the owner's best friend. Dogs have historically been the most popular choice in
```

## Full continuation

```text
8

The animal described is a dog, specifically a male who is likely to be the owner's best friend. Dogs have historically been the most popular choice in the United States.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-att-h8/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
