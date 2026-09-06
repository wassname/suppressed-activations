---
condition_id: "007_layer_position_strength_L=8_positions=2_C=4"
axis: "layer_position_strength"
value: "L=8,positions=2,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29999077320098877
p4: 0.004771770443767309
p8: 0.2952190041542053
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/007_layer_position_strength_L=8_positions=2_C=4/run.md"
---

# 007_layer_position_strength_L=8_positions=2_C=4

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
    "perturbation_norm": 3.1934399604797363,
    "relative_perturbation_by_position": [
      0.37404605746269226,
      0.2730550467967987
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
| 1      | '8'      | -1.220  | 0.295219 | +0.001            |
| 2      | 'The'    | -1.220  | 0.295219 | +0.001            |
| 3      | '**'     | -1.220  | 0.295219 | +0.001            |
| 4      | 'Fact'   | -2.720  | 0.065872 | +0.001            |
| 5      | 'Number' | -4.095  | 0.016655 | +0.001            |
| 6      | '###'    | -4.345  | 0.012971 | -0.124            |
| 7      | '4'      | -5.345  | 0.004772 | +0.001            |
| 8      | '1'      | -6.345  | 0.001755 | +0.001            |
| 9      | 'Answer' | -6.845  | 0.001065 | +0.126            |
| 10     | 'Eight'  | -6.845  | 0.001065 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
