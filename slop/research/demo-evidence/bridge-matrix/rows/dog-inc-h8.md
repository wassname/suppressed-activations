# dog-inc-h8

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: mild repetition (canonical r2 .117647) — 'The animal is the spider. It has eight legs. It is a spider.'
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [8], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "increment", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 19 (cap 128) — EOS count: 0
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
[{"token_id": 23, "token": "8", "logp": -0.11348673701286316, "p": 0.8927160501480103, "delta_logp": -0.02919648587703705}, {"token_id": 19, "token": "4", "logp": -2.3634867668151855, "p": 0.09409157931804657, "delta_logp": 0.7208034992218018}, {"token_id": 17, "token": "2", "logp": -5.7384867668151855, "p": 0.0032196366228163242, "delta_logp": 0.9708032608032227}, {"token_id": 18, "token": "3", "logp": -5.9884867668151855, "p": 0.002507455414161086, "delta_logp": 0.09580326080322266}, {"token_id": 21, "token": "6", "logp": -6.1134867668151855, "p": 0.002212821738794446, "delta_logp": -2.5291965007781982}, {"token_id": 16, "token": "1", "logp": -6.3634867668151855, "p": 0.00172334723174572, "delta_logp": -0.029196739196777344}, {"token_id": 20, "token": "5", "logp": -7.3634867668151855, "p": 0.0006339840474538505, "delta_logp": 0.47080326080322266}, {"token_id": 22, "token": "7", "logp": -7.4884867668151855, "p": 0.0005594889516942203, "delta_logp": 0.47080326080322266}, {"token_id": 15, "token": "0", "logp": -7.6759867668151855, "p": 0.0004638326645363122, "delta_logp": -0.21669673919677734}, {"token_id": 24, "token": "9", "logp": -8.050986289978027, "p": 0.0003187873517163098, "delta_logp": 1.033304214477539}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is the spider. It has eight legs. It is a spider.<|im_end|>
```

## Full continuation

```text
8

The animal is the spider. It has eight legs. It is a spider.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-inc-h8/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
