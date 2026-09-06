---
condition_id: "062_layer_position_strength_L=23_positions=1_C=4"
axis: "layer_position_strength"
value: "L=23,positions=1,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29686322808265686
p4: 0.004722023848444223
p8: 0.2921411991119385
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/062_layer_position_strength_L=23_positions=1_C=4/run.md"
---

# 062_layer_position_strength_L=23_positions=1_C=4

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
  "intervention_layer": 23,
  "intervention_positions": 1,
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
['compan', 'seh', 'amax', 'ปั่น', '-spin', ' Ủy', 'Spin', 'สุนัข']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 22.3740177154541,
    "perturbation_norm": 6.339743614196777,
    "relative_perturbation_by_position": [
      0.28335294127464294
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
| 1      | '8'      | -1.231  | 0.292141 | -0.009            |
| 2      | 'The'    | -1.231  | 0.292141 | -0.009            |
| 3      | '**'     | -1.231  | 0.292141 | -0.009            |
| 4      | 'Fact'   | -2.606  | 0.073865 | +0.116            |
| 5      | 'Number' | -4.106  | 0.016481 | -0.009            |
| 6      | '###'    | -4.231  | 0.014545 | -0.009            |
| 7      | '4'      | -5.356  | 0.004722 | -0.009            |
| 8      | '1'      | -6.356  | 0.001737 | -0.009            |
| 9      | 'Answer' | -6.856  | 0.001054 | +0.116            |
| 10     | 'Eight'  | -6.856  | 0.001054 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
