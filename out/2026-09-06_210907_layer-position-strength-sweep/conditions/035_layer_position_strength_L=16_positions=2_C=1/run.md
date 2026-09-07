---
condition_id: "035_layer_position_strength_L=16_positions=2_C=1"
axis: "layer_position_strength"
value: "L=16,positions=2,C=1"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.29995986819267273
p4: 0.005395140498876572
p8: 0.29456472396850586
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/035_layer_position_strength_L=16_positions=2_C=1/run.md"
---

# 035_layer_position_strength_L=16_positions=2_C=1

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

[Full diagnostic data](../../result.json) (`rows` → `035_layer_position_strength_L=16_positions=2_C=1`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.222  | 0.294565 | -0.001            |
| 2      | 'The'    | -1.222  | 0.294565 | -0.001            |
| 3      | '**'     | -1.222  | 0.294565 | -0.001            |
| 4      | 'Fact'   | -2.722  | 0.065726 | -0.001            |
| 5      | 'Number' | -4.097  | 0.016618 | -0.001            |
| 6      | '###'    | -4.222  | 0.014666 | -0.001            |
| 7      | '4'      | -5.222  | 0.005395 | +0.124            |
| 8      | '1'      | -6.347  | 0.001752 | -0.001            |
| 9      | 'Answer' | -6.847  | 0.001062 | +0.124            |
| 10     | 'Eight'  | -6.847  | 0.001062 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
