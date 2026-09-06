---
condition_id: "035_intervention_layer_25"
axis: "intervention_layer"
value: "25"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28612077236175537
p4: 0.0051462287083268166
p8: 0.28097453713417053
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/035_intervention_layer_25/run.md"
---

# 035_intervention_layer_25

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
  "intervention_layer": 25,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
[' spinning', 'web', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.144  | 0.318386 | +0.077            |
| 2      | '**'     | -1.269  | 0.280975 | -0.048            |
| 3      | '8'      | -1.269  | 0.280975 | -0.048            |
| 4      | 'Fact'   | -2.644  | 0.071041 | +0.077            |
| 5      | 'Number' | -4.144  | 0.015851 | -0.048            |
| 6      | '###'    | -4.269  | 0.013989 | -0.048            |
| 7      | '4'      | -5.269  | 0.005146 | +0.077            |
| 8      | '1'      | -6.269  | 0.001893 | +0.077            |
| 9      | 'Answer' | -6.894  | 0.001013 | +0.077            |
| 10     | 'Eight'  | -6.894  | 0.001013 | -0.048            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
