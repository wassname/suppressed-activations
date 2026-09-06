---
condition_id: "013_layer_position_strength_L=8_positions=4_C=8"
axis: "layer_position_strength"
value: "L=8,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.75
valid_answer_mass: 0.19463196396827698
p4: 0.0014747735112905502
p8: 0.19315719604492188
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/013_layer_position_strength_L=8_positions=4_C=8/run.md"
---

# 013_layer_position_strength_L=8_positions=4_C=8

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
  "intervention_positions": 4,
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
['Spin', 'seh', '-spin', 'สปิน', 'ปั่น', '\tspin', ' Spinner', 'spinner']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "8": {
    "residual_norm": 14.111225128173828,
    "perturbation_norm": 10.162041664123535,
    "relative_perturbation_by_position": [
      0.9242544174194336,
      0.7199040651321411,
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.019  | 0.360865 | +0.202            |
| 2      | 'The'    | -1.269  | 0.281042 | -0.048            |
| 3      | '8'      | -1.644  | 0.193157 | -0.423            |
| 4      | 'Fact'   | -2.644  | 0.071059 | +0.077            |
| 5      | '6'      | -3.394  | 0.033566 | +3.577            |
| 6      | 'Number' | -3.769  | 0.023069 | +0.327            |
| 7      | '###'    | -4.019  | 0.017966 | +0.202            |
| 8      | '1'      | -5.644  | 0.003538 | +0.702            |
| 9      | '2'      | -6.519  | 0.001475 | +1.202            |
| 10     | '4'      | -6.519  | 0.001475 | -1.173            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
