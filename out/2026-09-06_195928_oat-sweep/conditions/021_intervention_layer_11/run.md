---
condition_id: "021_intervention_layer_11"
axis: "intervention_layer"
value: "11"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.34217530488967896
p4: 0.010029922239482403
p8: 0.3321453928947449
repeated_bigram_fraction: 0.0
generation_tokens: 32
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['Spin', '\tspin', ' Ủy', '_spin', ' Presents', 'ปั่น', 'seh', 'spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '8'        | -1.102  | 0.332145 | +0.119            |
| 2      | 'The'      | -1.227  | 0.293117 | -0.006            |
| 3      | '**'       | -1.352  | 0.258675 | -0.131            |
| 4      | 'Fact'     | -2.852  | 0.057718 | -0.131            |
| 5      | '###'      | -4.102  | 0.016537 | +0.119            |
| 6      | 'Number'   | -4.352  | 0.012879 | -0.256            |
| 7      | '4'        | -4.602  | 0.010030 | +0.744            |
| 8      | '1'        | -5.852  | 0.002874 | +0.494            |
| 9      | '6'        | -6.102  | 0.002238 | +0.869            |
| 10     | 'Complete' | -6.602  | 0.001357 | +0.619            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
