---
condition_id: "026_intervention_layer_16"
axis: "intervention_layer"
value: "16"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.29066088795661926
p4: 0.007544789928942919
p8: 0.28311610221862793
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/026_intervention_layer_16/run.md"
---

# 026_intervention_layer_16

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
['Spin', '\tspin', ' Presents', 'ปั่น', '哈密', 'kab', 'สปิน', ' получила']
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
| 1      | 'The'      | -1.137  | 0.320813 | +0.085            |
| 2      | '8'        | -1.262  | 0.283116 | -0.040            |
| 3      | '**'       | -1.387  | 0.249849 | -0.165            |
| 4      | 'Fact'     | -2.387  | 0.091914 | +0.335            |
| 5      | 'Number'   | -4.012  | 0.018099 | +0.085            |
| 6      | '###'      | -4.387  | 0.012439 | -0.165            |
| 7      | '4'        | -4.887  | 0.007545 | +0.460            |
| 8      | '1'        | -6.137  | 0.002162 | +0.210            |
| 9      | 'Complete' | -6.512  | 0.001486 | +0.710            |
| 10     | '6'        | -6.637  | 0.001311 | +0.335            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
