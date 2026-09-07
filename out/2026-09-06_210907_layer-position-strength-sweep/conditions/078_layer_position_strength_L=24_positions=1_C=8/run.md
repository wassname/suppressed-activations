---
condition_id: "078_layer_position_strength_L=24_positions=1_C=8"
axis: "layer_position_strength"
value: "L=24,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.2865743637084961
p4: 0.0058267321437597275
p8: 0.2807476222515106
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/078_layer_position_strength_L=24_positions=1_C=8/run.md"
---

# 078_layer_position_strength_L=24_positions=1_C=8

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
['compan', ' Hunde', 'amax', 'seh', ' собаки', 'สุนัข', ' perros', ' Ủy']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `078_layer_position_strength_L=24_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.145  | 0.318129 | +0.076            |
| 2      | '**'     | -1.270  | 0.280748 | -0.049            |
| 3      | '8'      | -1.270  | 0.280748 | -0.049            |
| 4      | 'Fact'   | -2.645  | 0.070984 | +0.076            |
| 5      | 'Number' | -4.145  | 0.015839 | -0.049            |
| 6      | '###'    | -4.270  | 0.013978 | -0.049            |
| 7      | '4'      | -5.145  | 0.005827 | +0.201            |
| 8      | '1'      | -6.395  | 0.001669 | -0.049            |
| 9      | 'Answer' | -6.895  | 0.001013 | +0.076            |
| 10     | 'Eight'  | -6.895  | 0.001013 | -0.049            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
