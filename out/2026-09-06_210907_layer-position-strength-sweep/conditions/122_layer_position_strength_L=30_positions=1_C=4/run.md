---
condition_id: "122_layer_position_strength_L=30_positions=1_C=4"
axis: "layer_position_strength"
value: "L=30,positions=1,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29947173595428467
p4: 0.004763515666127205
p8: 0.2947082221508026
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/122_layer_position_strength_L=30_positions=1_C=4/run.md"
---

# 122_layer_position_strength_L=30_positions=1_C=4

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
  "intervention_positions": 1,
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

[Full diagnostic data](../../result.json) (`rows` → `122_layer_position_strength_L=30_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.222  | 0.294708 | -0.000            |
| 2      | 'The'    | -1.222  | 0.294708 | -0.000            |
| 3      | '**'     | -1.222  | 0.294708 | -0.000            |
| 4      | 'Fact'   | -2.722  | 0.065758 | -0.000            |
| 5      | 'Number' | -4.097  | 0.016626 | -0.000            |
| 6      | '###'    | -4.222  | 0.014673 | -0.000            |
| 7      | '4'      | -5.347  | 0.004764 | -0.000            |
| 8      | '1'      | -6.347  | 0.001752 | -0.000            |
| 9      | 'Eight'  | -6.847  | 0.001063 | -0.000            |
| 10     | '6'      | -6.972  | 0.000938 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
