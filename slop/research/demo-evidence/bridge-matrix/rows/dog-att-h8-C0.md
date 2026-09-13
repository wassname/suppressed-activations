# dog-att-h8-C0

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: C0 CONTROL: identical to the paired Base generation (zero edit).
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [8], "intervention_positions": 3, "strength": 0.0, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "attenuation", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 58 (cap 128) — EOS count: 0
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
[{"token_id": 23, "token": "8", "logp": -0.08429025113582611, "p": 0.9191644191741943, "delta_logp": 0.0}, {"token_id": 19, "token": "4", "logp": -3.0842902660369873, "p": 0.045762501657009125, "delta_logp": 0.0}, {"token_id": 21, "token": "6", "logp": -3.5842902660369873, "p": 0.027756361290812492, "delta_logp": 0.0}, {"token_id": 18, "token": "3", "logp": -6.084290027618408, "p": 0.0022783814929425716, "delta_logp": 0.0}, {"token_id": 16, "token": "1", "logp": -6.334290027618408, "p": 0.0017744052456691861, "delta_logp": 0.0}, {"token_id": 17, "token": "2", "logp": -6.709290027618408, "p": 0.0012195296585559845, "delta_logp": 0.0}, {"token_id": 15, "token": "0", "logp": -7.459290027618408, "p": 0.0005760649801231921, "delta_logp": 0.0}, {"token_id": 20, "token": "5", "logp": -7.834290027618408, "p": 0.00039592329994775355, "delta_logp": 0.0}, {"token_id": 22, "token": "7", "logp": -7.959290027618408, "p": 0.0003494011180009693, "delta_logp": 0.0}, {"token_id": 57087, "token": "Eight", "logp": -8.584290504455566, "p": 0.00018702083616517484, "delta_logp": 0.0}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect
```

## Full continuation

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect its eggs. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-att-h8-C0/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
