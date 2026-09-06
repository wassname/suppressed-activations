---
condition_id: "051_strength_2.0"
axis: "strength"
value: "2.0"
is_default: false
swap_log_odds_shift: -0.5
valid_answer_mass: 0.9664434790611267
p4: 0.019650069996714592
p8: 0.9467934370040894
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/051_strength_2.0/run.md"
---

# 051_strength_2.0

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
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 2.0,
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
['Spin', '\tspin', '-spin', '盐酸', '旋转', '_spin', '旋', ' laba']
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
| 1      | '8'       | -0.055  | 0.946793 | -0.003            |
| 2      | '6'       | -3.680  | 0.025231 | +0.997            |
| 3      | '4'       | -3.930  | 0.019650 | -0.503            |
| 4      | '<think>' | -5.930  | 0.002659 | -0.128            |
| 5      | '1'       | -6.305  | 0.001828 | +0.247            |
| 6      | 'Eight'   | -7.055  | 0.000863 | +0.247            |
| 7      | '2'       | -7.430  | 0.000593 | +0.247            |
| 8      | '3'       | -7.742  | 0.000434 | +0.184            |
| 9      | '0'       | -8.180  | 0.000280 | +0.309            |
| 10     | '5'       | -8.430  | 0.000218 | -0.003            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
