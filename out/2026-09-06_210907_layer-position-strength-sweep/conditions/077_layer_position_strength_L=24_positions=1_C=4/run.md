---
condition_id: "077_layer_position_strength_L=24_positions=1_C=4"
axis: "layer_position_strength"
value: "L=24,positions=1,C=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28616583347320557
p4: 0.005147038493305445
p8: 0.28101879358291626
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/077_layer_position_strength_L=24_positions=1_C=4/run.md"
---

# 077_layer_position_strength_L=24_positions=1_C=4

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
  "intervention_layer": 24,
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
['compan', 'amax', ' Hunde', 'seh', 'ปั่น', 'สุนัข', '-spin', ' Ủy']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `077_layer_position_strength_L=24_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.144  | 0.318436 | +0.077            |
| 2      | '**'     | -1.269  | 0.281019 | -0.048            |
| 3      | '8'      | -1.269  | 0.281019 | -0.048            |
| 4      | 'Fact'   | -2.644  | 0.071053 | +0.077            |
| 5      | 'Number' | -4.144  | 0.015854 | -0.048            |
| 6      | '###'    | -4.269  | 0.013991 | -0.048            |
| 7      | '4'      | -5.269  | 0.005147 | +0.077            |
| 8      | '1'      | -6.394  | 0.001671 | -0.048            |
| 9      | 'Answer' | -6.894  | 0.001014 | +0.077            |
| 10     | 'Eight'  | -6.894  | 0.001014 | -0.048            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
