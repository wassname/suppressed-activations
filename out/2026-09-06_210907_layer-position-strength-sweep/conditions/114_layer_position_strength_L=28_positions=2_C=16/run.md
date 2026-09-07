---
condition_id: "114_layer_position_strength_L=28_positions=2_C=16"
axis: "layer_position_strength"
value: "L=28,positions=2,C=16"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.32260507345199585
p4: 0.0035444439854472876
p8: 0.31906062364578247
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/114_layer_position_strength_L=28_positions=2_C=16/run.md"
---

# 114_layer_position_strength_L=28_positions=2_C=16

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
  "intervention_layer": 28,
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

[Full diagnostic data](../../result.json) (`rows` → `114_layer_position_strength_L=28_positions=2_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '8'        | -1.142  | 0.319061 | +0.079            |
| 2      | 'The'      | -1.267  | 0.281570 | -0.046            |
| 3      | '**'       | -1.267  | 0.281570 | -0.046            |
| 4      | 'Fact'     | -2.642  | 0.071192 | +0.079            |
| 5      | 'Number'   | -4.017  | 0.018000 | +0.079            |
| 6      | '###'      | -4.392  | 0.012371 | -0.171            |
| 7      | '4'        | -5.642  | 0.003544 | -0.296            |
| 8      | '1'        | -6.142  | 0.002150 | +0.204            |
| 9      | 'Answer'   | -7.017  | 0.000896 | -0.046            |
| 10     | 'Complete' | -7.142  | 0.000791 | +0.079            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
