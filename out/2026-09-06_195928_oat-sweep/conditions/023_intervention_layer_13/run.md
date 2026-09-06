---
condition_id: "023_intervention_layer_13"
axis: "intervention_layer"
value: "13"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.15113329887390137
p4: 0.004430054221302271
p8: 0.14670324325561523
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/023_intervention_layer_13/run.md"
---

# 023_intervention_layer_13

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
  "intervention_layer": 13,
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
['Spin', ' Presents', '\tspin', 'ปั่น', ' Ủy', '哈密', 'seh', 'Integrated']
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

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.919  | 0.398781 | +0.302            |
| 2      | '**'       | -1.044  | 0.351923 | +0.177            |
| 3      | '8'        | -1.919  | 0.146703 | -0.698            |
| 4      | '###'      | -3.294  | 0.037092 | +0.927            |
| 5      | 'Fact'     | -3.544  | 0.028888 | -0.823            |
| 6      | 'Number'   | -4.169  | 0.015462 | -0.073            |
| 7      | '4'        | -5.419  | 0.004430 | -0.073            |
| 8      | '1'        | -6.169  | 0.002093 | +0.177            |
| 9      | 'Complete' | -6.169  | 0.002093 | +1.052            |
| 10     | '6'        | -6.544  | 0.001438 | +0.427            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
