---
condition_id: "038_layer_position_strength_L=16_positions=2_C=8"
axis: "layer_position_strength"
value: "L=16,positions=2,C=8"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.31434503197669983
p4: 0.00921415351331234
p8: 0.30513086915016174
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/038_layer_position_strength_L=16_positions=2_C=8/run.md"
---

# 038_layer_position_strength_L=16_positions=2_C=8

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
  "intervention_layer": 16,
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
  "16": {
    "residual_norm": 14.143196105957031,
    "perturbation_norm": 10.37153434753418,
    "relative_perturbation_by_position": [
      0.7761197686195374,
      0.6793609261512756
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
| 1      | '8'      | -1.187  | 0.305131 | +0.034            |
| 2      | '**'     | -1.187  | 0.305131 | +0.034            |
| 3      | 'The'    | -1.437  | 0.237636 | -0.216            |
| 4      | 'Fact'   | -2.437  | 0.087421 | +0.284            |
| 5      | 'Number' | -3.812  | 0.022104 | +0.284            |
| 6      | '###'    | -4.187  | 0.015192 | +0.034            |
| 7      | '4'      | -4.687  | 0.009214 | +0.659            |
| 8      | '1'      | -6.062  | 0.002330 | +0.284            |
| 9      | 'Answer' | -6.437  | 0.001601 | +0.534            |
| 10     | 'Eight'  | -6.437  | 0.001601 | +0.409            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
