---
condition_id: "020_intervention_layer_10"
axis: "intervention_layer"
value: "10"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.9351302981376648
p4: 0.06316495686769485
p8: 0.8719653487205505
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/020_intervention_layer_10/run.md"
---

# 020_intervention_layer_10

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
  "intervention_layer": 10,
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
['ปั่น', 'Spin', ' Ủy', 'meldung', ' laba', '资讯网', ' Presents', '\tspin']
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
| 1      | '8'       | -0.137  | 0.871965 | -0.086            |
| 2      | '4'       | -2.762  | 0.063165 | +0.664            |
| 3      | '6'       | -3.012  | 0.049193 | +1.664            |
| 4      | '<think>' | -5.512  | 0.004038 | +0.289            |
| 5      | '1'       | -5.637  | 0.003564 | +0.914            |
| 6      | '2'       | -6.137  | 0.002161 | +1.539            |
| 7      | 'Eight'   | -7.012  | 0.000901 | +0.289            |
| 8      | '3'       | -7.012  | 0.000901 | +0.914            |
| 9      | '5'       | -7.450  | 0.000582 | +0.977            |
| 10     | '7'       | -7.512  | 0.000546 | +0.852            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
