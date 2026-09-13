# dog-inc-h20

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: coherent spider; the 'insects' mention is the web prey, not an identity error.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "increment", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 74 (cap 128) — EOS count: 0
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
[{"token_id": 23, "token": "8", "logp": -0.32830101251602173, "p": 0.7201462388038635, "delta_logp": -0.24401076138019562}, {"token_id": 19, "token": "4", "logp": -1.453300952911377, "p": 0.23379726707935333, "delta_logp": 1.6309893131256104}, {"token_id": 16, "token": "1", "logp": -4.203300952911377, "p": 0.014946158975362778, "delta_logp": 2.1309890747070312}, {"token_id": 21, "token": "6", "logp": -4.703300952911377, "p": 0.009065303951501846, "delta_logp": -1.1190106868743896}, {"token_id": 17, "token": "2", "logp": -4.828300952911377, "p": 0.008000101894140244, "delta_logp": 1.8809890747070312}, {"token_id": 18, "token": "3", "logp": -5.328300952911377, "p": 0.004852307494729757, "delta_logp": 0.7559890747070312}, {"token_id": 20, "token": "5", "logp": -6.328300952911377, "p": 0.0017850641161203384, "delta_logp": 1.5059890747070312}, {"token_id": 15, "token": "0", "logp": -6.453300952911377, "p": 0.0015753136249259114, "delta_logp": 1.0059890747070312}, {"token_id": 22, "token": "7", "logp": -7.015800952911377, "p": 0.0008975865785032511, "delta_logp": 0.9434890747070312}, {"token_id": 57087, "token": "Eight", "logp": -7.265800952911377, "p": 0.0006990411784499884, "delta_logp": 1.3184895515441895}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is a spider, an arachnid known for its eight legs and ability to create intricate webs. They are typically found in various environments around
```

## Full continuation

```text
8

The animal is a spider, an arachnid known for its eight legs and ability to create intricate webs. They are typically found in various environments around the world, where they hunt by waiting for prey to become entangled in their silk. Despite their reputation for being dangerous, most spiders are harmless to humans and play an important role in controlling insect populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-inc-h20/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
