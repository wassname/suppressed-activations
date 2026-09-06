---
condition_id: "008_layer_position_strength_L=8_positions=2_C=8"
axis: "layer_position_strength"
value: "L=8,positions=2,C=8"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.27787625789642334
p4: 0.004997940268367529
p8: 0.2728783190250397
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/008_layer_position_strength_L=8_positions=2_C=8/run.md"
---

# 008_layer_position_strength_L=8_positions=2_C=8

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
  "intervention_positions": 2,
  "strength": 8.0,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "8": {
    "residual_norm": 9.613831520080566,
    "perturbation_norm": 5.746224403381348,
    "relative_perturbation_by_position": [
      0.6630452871322632,
      0.5075258612632751
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -1.174  | 0.309212 | +0.048            |
| 2      | '**'       | -1.174  | 0.309212 | +0.048            |
| 3      | '8'        | -1.299  | 0.272878 | -0.077            |
| 4      | 'Fact'     | -2.799  | 0.060887 | -0.077            |
| 5      | 'Number'   | -4.174  | 0.015395 | -0.077            |
| 6      | '###'      | -4.299  | 0.013586 | -0.077            |
| 7      | '4'        | -5.299  | 0.004998 | +0.048            |
| 8      | '1'        | -6.549  | 0.001432 | -0.202            |
| 9      | 'Complete' | -6.799  | 0.001115 | +0.423            |
| 10     | 'Answer'   | -6.799  | 0.001115 | +0.173            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
