---
condition_id: "132_layer_position_strength_L=30_positions=4_C=4"
axis: "layer_position_strength"
value: "L=30,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29684239625930786
p4: 0.00472169229760766
p8: 0.29212069511413574
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/132_layer_position_strength_L=30_positions=4_C=4/run.md"
---

# 132_layer_position_strength_L=30_positions=4_C=4

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
  "intervention_layer": 30,
  "intervention_positions": 4,
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp', '-spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "30": {
    "residual_norm": 89.86124420166016,
    "perturbation_norm": 36.01340866088867,
    "relative_perturbation_by_position": [
      0.5310231447219849,
      0.5435152649879456,
      0.18143445253372192,
      0.26484471559524536
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.231  | 0.292121 | -0.009            |
| 2      | 'The'    | -1.231  | 0.292121 | -0.009            |
| 3      | '**'     | -1.231  | 0.292121 | -0.009            |
| 4      | 'Fact'   | -2.606  | 0.073860 | +0.116            |
| 5      | 'Number' | -4.106  | 0.016480 | -0.009            |
| 6      | '###'    | -4.231  | 0.014544 | -0.009            |
| 7      | '4'      | -5.356  | 0.004722 | -0.009            |
| 8      | '1'      | -6.356  | 0.001737 | -0.009            |
| 9      | 'Answer' | -6.856  | 0.001054 | +0.116            |
| 10     | 'Eight'  | -6.856  | 0.001054 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
