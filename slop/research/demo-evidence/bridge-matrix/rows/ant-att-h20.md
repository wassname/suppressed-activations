# ant-att-h20

- expected answer: 6 — observed: 6 — TRANSFER
- judgment: TRANSFER: answer 6 + ant identity, sustained ant description; 'hardworking' anthropomorphism. Historical success, byte-exact replay.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": -1, "basis_selector": "attenuation", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 65 (cap 128) — EOS count: 0
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
[{"token_id": 21, "token": "6", "logp": -0.018352463841438293, "p": 0.9818149209022522, "delta_logp": 3.5659377574920654}, {"token_id": 23, "token": "8", "logp": -4.643352508544922, "p": 0.009625374339520931, "delta_logp": -4.559062480926514}, {"token_id": 18, "token": "3", "logp": -5.268352508544922, "p": 0.005152091383934021, "delta_logp": 0.8159375190734863}, {"token_id": 16, "token": "1", "logp": -6.518352508544922, "p": 0.0014760988997295499, "delta_logp": -0.18406248092651367}, {"token_id": 19, "token": "4", "logp": -7.268352508544922, "p": 0.0006972597911953926, "delta_logp": -4.1840620040893555}, {"token_id": 17, "token": "2", "logp": -7.893352508544922, "p": 0.00037321625859476626, "delta_logp": -1.1840624809265137}, {"token_id": 22, "token": "7", "logp": -8.643352508544922, "p": 0.00017629488138481975, "delta_logp": -0.6840624809265137}, {"token_id": 18117, "token": " Six", "logp": -8.768352508544922, "p": 0.00015557969163637608, "delta_logp": 2.8159379959106445}, {"token_id": 15, "token": "0", "logp": -9.268352508544922, "p": 9.436385153094307e-05, "delta_logp": -1.8090624809265137}, {"token_id": 20, "token": "5", "logp": -9.393352508544922, "p": 8.327580144396052e-05, "delta_logp": -1.5590624809265137}]
```

## Generation — first 32 tokens (preview)

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. These social creatures live in vast colonies and communicate
```

## Full continuation

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. These social creatures live in vast colonies and communicate with one another using chemical signals called pheromones. Despite their tiny size, ants are incredibly resilient and can be found in almost every habitat on Earth.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-att-h20/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
