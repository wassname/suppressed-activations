---
condition_id: "018_intervention_layer_8"
axis: "intervention_layer"
value: "8"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.41456663608551025
p4: 0.01076105423271656
p8: 0.40380558371543884
repeated_bigram_fraction: 0.0
generation_tokens: 32
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['ปั่น', '-spin', 'Spin', 'seh', ' Spin', 'spin', ' Presents', ' Ủy']
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
| 1      | '8'        | -0.907  | 0.403806 | +0.315            |
| 2      | '**'       | -1.407  | 0.244920 | -0.185            |
| 3      | 'The'      | -1.407  | 0.244920 | -0.185            |
| 4      | 'Fact'     | -3.282  | 0.037560 | -0.560            |
| 5      | 'Number'   | -3.907  | 0.020104 | +0.190            |
| 6      | '###'      | -4.032  | 0.017742 | +0.190            |
| 7      | '4'        | -4.532  | 0.010761 | +0.815            |
| 8      | '1'        | -5.532  | 0.003959 | +0.815            |
| 9      | '6'        | -6.032  | 0.002401 | +0.940            |
| 10     | 'Complete' | -6.657  | 0.001285 | +0.565            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
