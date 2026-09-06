---
condition_id: "027_intervention_layer_17"
axis: "intervention_layer"
value: "17"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.24746151268482208
p4: 0.006423446349799633
p8: 0.24103806912899017
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/027_intervention_layer_17/run.md"
---

# 027_intervention_layer_17

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
  "intervention_layer": 17,
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
['Spin', '\tspin', 'ปั่น', '哈密', ' Presents', '_spin', 'สปิน', 'kab']
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
| 1      | 'The'      | -0.923  | 0.397405 | +0.299            |
| 2      | '**'       | -1.423  | 0.241038 | -0.201            |
| 3      | '8'        | -1.423  | 0.241038 | -0.201            |
| 4      | 'Fact'     | -2.673  | 0.069059 | +0.049            |
| 5      | 'Number'   | -4.173  | 0.015409 | -0.076            |
| 6      | '###'      | -4.173  | 0.015409 | +0.049            |
| 7      | '4'        | -5.048  | 0.006423 | +0.299            |
| 8      | '1'        | -6.423  | 0.001624 | -0.076            |
| 9      | '6'        | -6.798  | 0.001116 | +0.174            |
| 10     | 'Complete' | -7.048  | 0.000869 | +0.174            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
