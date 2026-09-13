# dog-att-h20

- expected answer: 4 — observed: 4 — TRANSFER
- judgment: TRANSFER: answer 4 + dog identity, sustained donor description; 'short history of being raised by humans' questionable. Historical success, byte-exact replay.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": -1, "basis_selector": "attenuation", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 65 (cap 128) — EOS count: 0
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
[{"token_id": 19, "token": "4", "logp": -0.03183978050947189, "p": 0.9686617851257324, "delta_logp": 3.05245041847229}, {"token_id": 17, "token": "2", "logp": -3.6568398475646973, "p": 0.025813959538936615, "delta_logp": 3.052450180053711}, {"token_id": 12937, "token": " Four", "logp": -6.656839847564697, "p": 0.0012852014042437077, "delta_logp": 3.864950656890869}, {"token_id": 16, "token": "1", "logp": -7.031839847564697, "p": 0.0008833050960674882, "delta_logp": -0.6975498199462891}, {"token_id": 23, "token": "8", "logp": -7.281839847564697, "p": 0.0006879187421873212, "delta_logp": -7.197549819946289}, {"token_id": 15, "token": "0", "logp": -7.406839847564697, "p": 0.0006070861127227545, "delta_logp": 0.05245018005371094}, {"token_id": 561, "token": " The", "logp": -7.781839847564697, "p": 0.0004172438057139516, "delta_logp": 3.864950656890869}, {"token_id": 37150, "token": " Dogs", "logp": -7.781839847564697, "p": 0.0004172438057139516, "delta_logp": 9.646200180053711}, {"token_id": 18, "token": "3", "logp": -7.906839847564697, "p": 0.00036821633693762124, "delta_logp": -1.822549819946289}, {"token_id": 21, "token": "6", "logp": -8.594339370727539, "p": 0.00018515090050641447, "delta_logp": -5.010048866271973}]
```

## Generation — first 32 tokens (preview)

```text
4

The animal is a dog, which is a domesticated canine known for its loyalty and ability to understand human commands. Dogs typically have a short history of
```

## Full continuation

```text
4

The animal is a dog, which is a domesticated canine known for its loyalty and ability to understand human commands. Dogs typically have a short history of being raised by humans, often serving as companions, hunters, or working partners. They are generally friendly and adaptable, making them popular family pets around the world.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-att-h20/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
