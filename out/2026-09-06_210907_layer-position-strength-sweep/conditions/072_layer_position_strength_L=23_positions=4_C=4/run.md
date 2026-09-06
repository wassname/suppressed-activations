---
condition_id: "072_layer_position_strength_L=23_positions=4_C=4"
axis: "layer_position_strength"
value: "L=23,positions=4,C=4"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.29620254039764404
p4: 0.003682286711409688
p8: 0.2925202548503876
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/072_layer_position_strength_L=23_positions=4_C=4/run.md"
---

# 072_layer_position_strength_L=23_positions=4_C=4

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
['compan', ' Ủy', ' Uỷ', '友達', ' NHÀ', ' ủy', 'seh', 'amax']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 47.82111740112305,
    "perturbation_norm": 16.678815841674805,
    "relative_perturbation_by_position": [
      0.48111140727996826,
      0.3429189920425415,
      0.22816140949726105,
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
| 1      | '8'      | -1.229  | 0.292520 | -0.008            |
| 2      | 'The'    | -1.229  | 0.292520 | -0.008            |
| 3      | '**'     | -1.229  | 0.292520 | -0.008            |
| 4      | 'Fact'   | -2.604  | 0.073961 | +0.117            |
| 5      | 'Number' | -4.104  | 0.016503 | -0.008            |
| 6      | '###'    | -4.229  | 0.014564 | -0.008            |
| 7      | '4'      | -5.604  | 0.003682 | -0.258            |
| 8      | '1'      | -6.354  | 0.001739 | -0.008            |
| 9      | 'Answer' | -6.854  | 0.001055 | +0.117            |
| 10     | 'Eight'  | -6.854  | 0.001055 | -0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
