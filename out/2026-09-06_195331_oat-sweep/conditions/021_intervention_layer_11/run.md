---
condition_id: "021_intervention_layer_11"
axis: "intervention_layer"
value: "11"
is_default: false
swap_log_odds_shift: 0.875
valid_answer_mass: 0.9610800743103027
p4: 0.07290578633546829
p8: 0.888174295425415
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/021_intervention_layer_11/run.md"
---

# 021_intervention_layer_11

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
  "intervention_layer": 11,
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
['Spin', ' Presents', ' Ủy', '\tspin', '_spin', 'ปั่น', 'meldung', 'umd']
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
| 1      | '8'       | -0.119  | 0.888174 | -0.067            |
| 2      | '4'       | -2.619  | 0.072906 | +0.808            |
| 3      | '6'       | -3.619  | 0.026821 | +1.058            |
| 4      | '<think>' | -5.744  | 0.003203 | +0.058            |
| 5      | '1'       | -6.119  | 0.002202 | +0.433            |
| 6      | '2'       | -6.744  | 0.001178 | +0.933            |
| 7      | 'Eight'   | -6.994  | 0.000918 | +0.308            |
| 8      | '3'       | -6.994  | 0.000918 | +0.933            |
| 9      | '5'       | -7.556  | 0.000523 | +0.870            |
| 10     | '7'       | -7.869  | 0.000383 | +0.495            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
