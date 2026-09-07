---
condition_id: "049_layer_position_strength_L=20_positions=1_C=16"
axis: "layer_position_strength"
value: "L=20,positions=1,C=16"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.2952243387699127
p4: 0.0032436123583465815
p8: 0.29198071360588074
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/049_layer_position_strength_L=20_positions=1_C=16/run.md"
---

# 049_layer_position_strength_L=20_positions=1_C=16

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

[Full diagnostic data](../../result.json) (`rows` → `049_layer_position_strength_L=20_positions=1_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.231  | 0.291981 | -0.010            |
| 2      | 'The'    | -1.231  | 0.291981 | -0.010            |
| 3      | '**'     | -1.231  | 0.291981 | -0.010            |
| 4      | 'Fact'   | -2.606  | 0.073824 | +0.115            |
| 5      | 'Number' | -3.981  | 0.018666 | +0.115            |
| 6      | '###'    | -4.231  | 0.014537 | -0.010            |
| 7      | '4'      | -5.731  | 0.003244 | -0.385            |
| 8      | '1'      | -6.356  | 0.001736 | -0.010            |
| 9      | 'Answer' | -6.856  | 0.001053 | +0.115            |
| 10     | 'Eight'  | -6.856  | 0.001053 | -0.010            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
