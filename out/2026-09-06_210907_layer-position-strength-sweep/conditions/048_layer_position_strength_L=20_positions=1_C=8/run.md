---
condition_id: "048_layer_position_strength_L=20_positions=1_C=8"
axis: "layer_position_strength"
value: "L=20,positions=1,C=8"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2964686453342438
p4: 0.004169423133134842
p8: 0.29229921102523804
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/048_layer_position_strength_L=20_positions=1_C=8/run.md"
---

# 048_layer_position_strength_L=20_positions=1_C=8

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
  "intervention_positions": 1,
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
  "20": {
    "residual_norm": 16.372173309326172,
    "perturbation_norm": 7.227221965789795,
    "relative_perturbation_by_position": [
      0.44143328070640564
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
| 1      | '8'      | -1.230  | 0.292299 | -0.008            |
| 2      | 'The'    | -1.230  | 0.292299 | -0.008            |
| 3      | '**'     | -1.230  | 0.292299 | -0.008            |
| 4      | 'Fact'   | -2.605  | 0.073905 | +0.117            |
| 5      | 'Number' | -4.105  | 0.016490 | -0.008            |
| 6      | '###'    | -4.230  | 0.014553 | -0.008            |
| 7      | '4'      | -5.480  | 0.004169 | -0.133            |
| 8      | '1'      | -6.355  | 0.001738 | -0.008            |
| 9      | 'Answer' | -6.855  | 0.001054 | +0.117            |
| 10     | 'Eight'  | -6.855  | 0.001054 | -0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
