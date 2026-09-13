# ant-inc-h8

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: misleading biology ('legs manipulate silk' — spinnerets produce it).
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [8], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "increment", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
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
[{"token_id": 23, "token": "8", "logp": -0.07833986729383469, "p": 0.9246501326560974, "delta_logp": 0.0059503838419914246}, {"token_id": 19, "token": "4", "logp": -2.9533398151397705, "p": 0.0521651916205883, "delta_logp": 0.1309504508972168}, {"token_id": 17, "token": "2", "logp": -5.07834005355835, "p": 0.006230242550373077, "delta_logp": 1.6309499740600586}, {"token_id": 18, "token": "3", "logp": -5.20334005355835, "p": 0.005498169455677271, "delta_logp": 0.8809499740600586}, {"token_id": 16, "token": "1", "logp": -5.32834005355835, "p": 0.004852117504924536, "delta_logp": 1.0059499740600586}, {"token_id": 21, "token": "6", "logp": -5.82834005355835, "p": 0.002942957915365696, "delta_logp": -2.2440497875213623}, {"token_id": 20, "token": "5", "logp": -6.82834005355835, "p": 0.0010826537618413568, "delta_logp": 1.0059499740600586}, {"token_id": 22, "token": "7", "logp": -6.82834005355835, "p": 0.0010826537618413568, "delta_logp": 1.1309499740600586}, {"token_id": 24, "token": "9", "logp": -7.70334005355835, "p": 0.00045131726074032485, "delta_logp": 1.3809504508972168}, {"token_id": 15, "token": "0", "logp": -8.078339576721191, "p": 0.0003101856564171612, "delta_logp": -0.6190495491027832}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid that typically has eight legs. These appendages are used to spin silk threads to create webs for protection and hunting.
```

## Full continuation

```text
8

The spider is an arachnid that typically has eight legs. These appendages are used to spin silk threads to create webs for protection and hunting. While some species may have more or fewer legs, eight is the most common number.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-inc-h8/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
