---
condition_id: "034_layer_position_strength_L=16_positions=1_C=16"
axis: "layer_position_strength"
value: "L=16,positions=1,C=16"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3249088525772095
p4: 0.0058438777923583984
p8: 0.3190649747848511
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/034_layer_position_strength_L=16_positions=1_C=16/run.md"
---

# 034_layer_position_strength_L=16_positions=1_C=16

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
  "intervention_positions": 1,
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

[Full diagnostic data](../../result.json) (`rows` → `034_layer_position_strength_L=16_positions=1_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.142  | 0.319065 | +0.079            |
| 2      | '**'     | -1.142  | 0.319065 | +0.079            |
| 3      | 'The'    | -1.517  | 0.219290 | -0.296            |
| 4      | 'Fact'   | -2.517  | 0.080672 | +0.204            |
| 5      | 'Number' | -3.767  | 0.023113 | +0.329            |
| 6      | '###'    | -4.142  | 0.015885 | +0.079            |
| 7      | '4'      | -5.142  | 0.005844 | +0.204            |
| 8      | '1'      | -6.142  | 0.002150 | +0.204            |
| 9      | 'Answer' | -6.392  | 0.001674 | +0.579            |
| 10     | 'Eight'  | -6.517  | 0.001478 | +0.329            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
