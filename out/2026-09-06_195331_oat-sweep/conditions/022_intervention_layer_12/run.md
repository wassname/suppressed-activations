---
condition_id: "022_intervention_layer_12"
axis: "intervention_layer"
value: "12"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.9265711307525635
p4: 0.06258681416511536
p8: 0.8639843463897705
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/022_intervention_layer_12/run.md"
---

# 022_intervention_layer_12

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
  "intervention_layer": 12,
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
[' Presents', ' Ủy', 'ปั่น', '\tspin', ' laba', 'Spin', 'meldung', 'umd']
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
| 1      | '8'       | -0.146  | 0.863984 | -0.095            |
| 2      | '6'       | -2.771  | 0.062587 | +1.905            |
| 3      | '4'       | -2.771  | 0.062587 | +0.655            |
| 4      | '<think>' | -5.896  | 0.002750 | -0.095            |
| 5      | '1'       | -6.146  | 0.002142 | +0.405            |
| 6      | '2'       | -6.646  | 0.001299 | +1.030            |
| 7      | '3'       | -7.271  | 0.000695 | +0.655            |
| 8      | 'Eight'   | -7.459  | 0.000576 | -0.157            |
| 9      | '0'       | -7.584  | 0.000509 | +0.905            |
| 10     | '5'       | -7.646  | 0.000478 | +0.780            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
