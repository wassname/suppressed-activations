---
condition_id: "054_layer_position_strength_L=20_positions=2_C=16"
axis: "layer_position_strength"
value: "L=20,positions=2,C=16"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2986844778060913
p4: 0.004200587514787912
p8: 0.29448390007019043
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/054_layer_position_strength_L=20_positions=2_C=16/run.md"
---

# 054_layer_position_strength_L=20_positions=2_C=16

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
  "intervention_layer": 20,
  "intervention_positions": 2,
  "strength": 16.0,
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
  "20": {
    "residual_norm": 22.896114349365234,
    "perturbation_norm": 15.768362045288086,
    "relative_perturbation_by_position": [
      0.6265701055526733,
      0.7432265877723694
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
| 1      | '8'      | -1.223  | 0.294484 | -0.001            |
| 2      | 'The'    | -1.223  | 0.294484 | -0.001            |
| 3      | '**'     | -1.223  | 0.294484 | -0.001            |
| 4      | 'Fact'   | -2.723  | 0.065708 | -0.001            |
| 5      | 'Number' | -3.973  | 0.018826 | +0.124            |
| 6      | '###'    | -4.223  | 0.014661 | -0.001            |
| 7      | '4'      | -5.473  | 0.004201 | -0.126            |
| 8      | '1'      | -6.473  | 0.001545 | -0.126            |
| 9      | 'Eight'  | -6.848  | 0.001062 | -0.001            |
| 10     | 'Answer' | -6.973  | 0.000937 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
