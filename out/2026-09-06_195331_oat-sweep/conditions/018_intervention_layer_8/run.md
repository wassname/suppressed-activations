---
condition_id: "018_intervention_layer_8"
axis: "intervention_layer"
value: "8"
is_default: false
swap_log_odds_shift: 0.875
valid_answer_mass: 0.9417738914489746
p4: 0.07144125550985336
p8: 0.870332658290863
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/018_intervention_layer_8/run.md"
---

# 018_intervention_layer_8

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
  "intervention_layer": 8,
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
['ปั่น', 'Spin', ' Presents', 'seh', ' Ủy', ' получила', '\tspin', 'spin']
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
| 1      | '8'       | -0.139  | 0.870333 | -0.088            |
| 2      | '4'       | -2.639  | 0.071441 | +0.787            |
| 3      | '6'       | -3.139  | 0.043331 | +1.537            |
| 4      | '1'       | -5.389  | 0.004567 | +1.162            |
| 5      | '<think>' | -5.889  | 0.002770 | -0.088            |
| 6      | '2'       | -6.264  | 0.001904 | +1.412            |
| 7      | '3'       | -6.764  | 0.001155 | +1.162            |
| 8      | 'Eight'   | -7.264  | 0.000700 | +0.037            |
| 9      | '5'       | -7.389  | 0.000618 | +1.037            |
| 10     | '0'       | -7.451  | 0.000581 | +1.037            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
