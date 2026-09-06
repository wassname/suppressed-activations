---
condition_id: "042_intervention_layer_32"
axis: "intervention_layer"
value: "32"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.982487142086029
p4: 0.0325065515935421
p8: 0.949980616569519
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/042_intervention_layer_32/run.md"
---

# 042_intervention_layer_32

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": 32,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' spinning', 'web', '-web', ' spin', ' spins', 'Web', '.Sp', '\tsp']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.051  | 0.949981 | +0.000            |
| 2      | '4'       | -3.426  | 0.032507 | +0.000            |
| 3      | '6'       | -4.676  | 0.009313 | +0.000            |
| 4      | '<think>' | -5.801  | 0.003024 | +0.000            |
| 5      | '1'       | -6.551  | 0.001428 | +0.000            |
| 6      | 'Eight'   | -7.301  | 0.000675 | +0.000            |
| 7      | '2'       | -7.676  | 0.000464 | +0.000            |
| 8      | '3'       | -7.926  | 0.000361 | +0.000            |
| 9      | '7'       | -8.364  | 0.000233 | +0.000            |
| 10     | '5'       | -8.426  | 0.000219 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
