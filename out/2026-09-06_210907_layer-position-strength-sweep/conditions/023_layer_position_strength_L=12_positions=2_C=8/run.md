---
condition_id: "023_layer_position_strength_L=12_positions=2_C=8"
axis: "layer_position_strength"
value: "L=12,positions=2,C=8"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.29960379004478455
p4: 0.0060916501097381115
p8: 0.29351213574409485
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/023_layer_position_strength_L=12_positions=2_C=8/run.md"
---

# 023_layer_position_strength_L=12_positions=2_C=8

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
  "12": {
    "residual_norm": 11.424951553344727,
    "perturbation_norm": 5.713791847229004,
    "relative_perturbation_by_position": [
      0.5218048095703125,
      0.47437748312950134
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
| 1      | '**'     | -1.101  | 0.332593 | +0.121            |
| 2      | '8'      | -1.226  | 0.293512 | -0.004            |
| 3      | 'The'    | -1.351  | 0.259024 | -0.129            |
| 4      | 'Fact'   | -2.851  | 0.057796 | -0.129            |
| 5      | '###'    | -3.976  | 0.018764 | +0.246            |
| 6      | 'Number' | -4.101  | 0.016559 | -0.004            |
| 7      | '4'      | -5.101  | 0.006092 | +0.246            |
| 8      | '1'      | -6.226  | 0.001978 | +0.121            |
| 9      | '6'      | -6.726  | 0.001200 | +0.246            |
| 10     | 'Answer' | -6.726  | 0.001200 | +0.246            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
