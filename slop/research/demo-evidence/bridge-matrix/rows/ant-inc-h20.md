# ant-inc-h20

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: coherent spider description.
- config: {"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 1.5, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "none", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false, "span_correction": true, "random_in_span": false, "extra_prefill_positions": null, "answer_patch_layer": null, "answer_patch_strength": null, "common_basis": "none", "common_window": 4, "common_random_rank": 8, "common_seed": 0, "common_bank_layers": [23, 25, 32], "common_selector": "snapshot", "common_donor_rank": 8, "common_temporal_full": false, "common_source_rank": 8, "complete_edit_mode": false, "delta_anchor_layer": 20, "basis_selector": "increment", "xdepth_anchor_layer": -1, "xdepth_norm_from_layer": -1, "common_removal": "source", "removal_only": false, "common_inject_norm": "own", "common_inject": "pd_d", "common_inject_restricted": false, "sync_donor": false}
- tokens: 58 (cap 128) — EOS count: 0
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
[{"token_id": 23, "token": "8", "logp": -0.29594120383262634, "p": 0.7438311576843262, "delta_logp": -0.21165095269680023}, {"token_id": 21, "token": "6", "logp": -1.7959412336349487, "p": 0.16597115993499756, "delta_logp": 1.7883490324020386}, {"token_id": 19, "token": "4", "logp": -2.670941114425659, "p": 0.06918708235025406, "delta_logp": 0.4133491516113281}, {"token_id": 16, "token": "1", "logp": -4.670941352844238, "p": 0.009363451041281223, "delta_logp": 1.66334867477417}, {"token_id": 17, "token": "2", "logp": -5.545941352844238, "p": 0.0039032672066241503, "delta_logp": 1.16334867477417}, {"token_id": 18, "token": "3", "logp": -5.670941352844238, "p": 0.003444621106609702, "delta_logp": 0.4133486747741699}, {"token_id": 15, "token": "0", "logp": -6.670941352844238, "p": 0.0012672052253037691, "delta_logp": 0.7883486747741699}, {"token_id": 22, "token": "7", "logp": -6.920941352844238, "p": 0.0009869005298241973, "delta_logp": 1.03834867477417}, {"token_id": 20, "token": "5", "logp": -7.045941352844238, "p": 0.0008709366666153073, "delta_logp": 0.7883486747741699}, {"token_id": 24, "token": "9", "logp": -7.920941352844238, "p": 0.00036306038964539766, "delta_logp": 1.1633491516113281}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid known for spinning intricate webs to catch insects. It typically has eight legs, which it uses for walking and sensing its
```

## Full continuation

```text
8

The spider is an arachnid known for spinning intricate webs to catch insects. It typically has eight legs, which it uses for walking and sensing its environment. Despite its reputation for being creepy, many spiders are harmless to humans and play a vital role in controlling pest populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-inc-h20/result.json (runner
row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Snapshot copied from the batchwork run.
