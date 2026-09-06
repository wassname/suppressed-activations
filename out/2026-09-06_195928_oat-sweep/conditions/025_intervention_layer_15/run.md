---
condition_id: "025_intervention_layer_15"
axis: "intervention_layer"
value: "15"
is_default: false
swap_log_odds_shift: 0.7499997615814209
valid_answer_mass: 0.10529221594333649
p4: 0.003483694978058338
p8: 0.10180851817131042
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/025_intervention_layer_15/run.md"
---

# 025_intervention_layer_15

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
  "intervention_layer": 15,
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
['\tspin', ' Presents', 'Spin', 'ปั่น', '哈密', ' laba', '领头羊', 'kab']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most famous for spinning webs is the **spider**.
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.785  | 0.456274 | +0.437            |
| 2      | '**'       | -1.160  | 0.313592 | +0.062            |
| 3      | '8'        | -2.285  | 0.101809 | -1.063            |
| 4      | 'Fact'     | -2.785  | 0.061750 | -0.063            |
| 5      | '###'      | -3.410  | 0.033052 | +0.812            |
| 6      | 'Number'   | -4.285  | 0.013778 | -0.188            |
| 7      | '4'        | -5.660  | 0.003484 | -0.313            |
| 8      | 'Complete' | -6.035  | 0.002394 | +1.187            |
| 9      | '1'        | -6.785  | 0.001131 | -0.438            |
| 10     | '6'        | -6.785  | 0.001131 | +0.187            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
