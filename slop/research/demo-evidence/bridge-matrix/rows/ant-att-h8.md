# ant-att-h8

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: spider identity retained; FALSE biology (spiders called hardworking social insects with colonies) — ant properties leaked without the name change.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [8], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "attenuation", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 50 (cap 128) — EOS count: 0
- canonical r2 (non-special IDs): None

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

The donor input (rendered; used only to extract the component):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that lives in colonies and follows pheromone trails have?\nAnswer: '
```

## Readout / top tokens at the first generated position

```json
[{"token_id": 23, "token": "8", "logp": -0.06139713525772095, "p": 0.9404497146606445, "delta_logp": 0.022893115878105164}, {"token_id": 21, "token": "6", "logp": -3.436397075653076, "p": 0.03218042105436325, "delta_logp": 0.14789319038391113}, {"token_id": 19, "token": "4", "logp": -4.436397075653076, "p": 0.011838515289127827, "delta_logp": -1.3521068096160889}, {"token_id": 18, "token": "3", "logp": -5.436397075653076, "p": 0.004355146083980799, "delta_logp": 0.647892951965332}, {"token_id": 17, "token": "2", "logp": -5.686397075653076, "p": 0.003391791367903352, "delta_logp": 1.022892951965332}, {"token_id": 16, "token": "1", "logp": -5.686397075653076, "p": 0.003391791367903352, "delta_logp": 0.647892951965332}, {"token_id": 15, "token": "0", "logp": -6.686397075653076, "p": 0.0012477703858166933, "delta_logp": 0.772892951965332}, {"token_id": 22, "token": "7", "logp": -7.311397075653076, "p": 0.0006678833160549402, "delta_logp": 0.647892951965332}, {"token_id": 24, "token": "9", "logp": -7.623897075653076, "p": 0.0004886338720098138, "delta_logp": 1.4603934288024902}, {"token_id": 2972, "token": " **", "logp": -7.623897075653076, "p": 0.0004886338720098138, "delta_logp": 3.0228934288024902}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is the spider. Spiders are small, hardworking insects known for their ability to work together in organized groups to build and maintain colonies.
```

## Full continuation

```text
8

The animal is the spider. Spiders are small, hardworking insects known for their ability to work together in organized groups to build and maintain colonies. They play a crucial role in ecosystems as a primary food source for many other species.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-att-h8/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
