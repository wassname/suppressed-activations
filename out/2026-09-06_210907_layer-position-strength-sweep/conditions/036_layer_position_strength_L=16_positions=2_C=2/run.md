---
condition_id: "036_layer_position_strength_L=16_positions=2_C=2"
axis: "layer_position_strength"
value: "L=16,positions=2,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.321833997964859
p4: 0.005119218025356531
p8: 0.3167147934436798
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/036_layer_position_strength_L=16_positions=2_C=2/run.md"
---

# 036_layer_position_strength_L=16_positions=2_C=2

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
  "strength": 2.0,
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

[Full diagnostic data](../../result.json) (`rows` → `036_layer_position_strength_L=16_positions=2_C=2`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.150  | 0.316715 | +0.072            |
| 2      | 'The'    | -1.275  | 0.279500 | -0.053            |
| 3      | '**'     | -1.275  | 0.279500 | -0.053            |
| 4      | 'Fact'   | -2.650  | 0.070669 | +0.072            |
| 5      | 'Number' | -4.025  | 0.017868 | +0.072            |
| 6      | '###'    | -4.150  | 0.015768 | +0.072            |
| 7      | '4'      | -5.275  | 0.005119 | +0.072            |
| 8      | '1'      | -6.275  | 0.001883 | +0.072            |
| 9      | 'Answer' | -6.775  | 0.001142 | +0.197            |
| 10     | 'Eight'  | -6.775  | 0.001142 | +0.072            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
