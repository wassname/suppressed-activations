---
condition_id: "038_intervention_layer_28"
axis: "intervention_layer"
value: "28"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9843990206718445
p4: 0.03256980702280998
p8: 0.951829195022583
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/038_intervention_layer_28/run.md"
---

# 038_intervention_layer_28

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
  "intervention_layer": 28,
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
[' spinning', ' spin', ' spins', ' Ủy', '.Sp', '\tsp', '纺', 'ปั่น']
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
| 1      | '8'       | -0.049  | 0.951829 | +0.002            |
| 2      | '4'       | -3.424  | 0.032570 | +0.002            |
| 3      | '6'       | -4.799  | 0.008235 | -0.123            |
| 4      | '<think>' | -5.924  | 0.002673 | -0.123            |
| 5      | '1'       | -6.674  | 0.001263 | -0.123            |
| 6      | 'Eight'   | -7.424  | 0.000597 | -0.123            |
| 7      | '2'       | -7.674  | 0.000465 | +0.002            |
| 8      | '3'       | -7.987  | 0.000340 | -0.061            |
| 9      | '5'       | -8.487  | 0.000206 | -0.061            |
| 10     | '7'       | -8.487  | 0.000206 | -0.123            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
