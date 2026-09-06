---
condition_id: "036_intervention_layer_26"
axis: "intervention_layer"
value: "26"
is_default: false
swap_log_odds_shift: 0.1250002384185791
valid_answer_mass: 0.28611743450164795
p4: 0.0051461695693433285
p8: 0.2809712588787079
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/036_intervention_layer_26/run.md"
---

# 036_intervention_layer_26

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
  "intervention_layer": 26,
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
| 1      | 'The'    | -1.145  | 0.318382 | +0.077            |
| 2      | '**'     | -1.270  | 0.280971 | -0.048            |
| 3      | '8'      | -1.270  | 0.280971 | -0.048            |
| 4      | 'Fact'   | -2.645  | 0.071041 | +0.077            |
| 5      | 'Number' | -4.145  | 0.015851 | -0.048            |
| 6      | '###'    | -4.270  | 0.013989 | -0.048            |
| 7      | '4'      | -5.270  | 0.005146 | +0.077            |
| 8      | '1'      | -6.395  | 0.001671 | -0.048            |
| 9      | 'Answer' | -6.895  | 0.001013 | +0.077            |
| 10     | 'Eight'  | -6.895  | 0.001013 | -0.048            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
