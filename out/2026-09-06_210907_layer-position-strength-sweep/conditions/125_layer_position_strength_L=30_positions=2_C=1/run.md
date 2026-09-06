---
condition_id: "125_layer_position_strength_L=30_positions=2_C=1"
axis: "layer_position_strength"
value: "L=30,positions=2,C=1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29955387115478516
p4: 0.004764821846038103
p8: 0.29478904604911804
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/125_layer_position_strength_L=30_positions=2_C=1/run.md"
---

# 125_layer_position_strength_L=30_positions=2_C=1

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
  "intervention_positions": 2,
  "strength": 1.0,
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
  "30": {
    "residual_norm": 66.04380798339844,
    "perturbation_norm": 3.8156018257141113,
    "relative_perturbation_by_position": [
      0.045886944979429245,
      0.06778505444526672
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
| 1      | '8'      | -1.221  | 0.294789 | +0.000            |
| 2      | 'The'    | -1.221  | 0.294789 | +0.000            |
| 3      | '**'     | -1.221  | 0.294789 | +0.000            |
| 4      | 'Fact'   | -2.721  | 0.065776 | +0.000            |
| 5      | 'Number' | -4.096  | 0.016631 | +0.000            |
| 6      | '###'    | -4.221  | 0.014677 | +0.000            |
| 7      | '4'      | -5.346  | 0.004765 | +0.000            |
| 8      | '1'      | -6.346  | 0.001753 | +0.000            |
| 9      | 'Eight'  | -6.846  | 0.001063 | +0.000            |
| 10     | '6'      | -6.971  | 0.000938 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
