---
condition_id: "009_rank_4"
axis: "rank"
value: "4"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2184327393770218
p4: 0.0030719570349901915
p8: 0.21536077558994293
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/009_rank_4/run.md"
---

# 009_rank_4

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
  "rank": 4,
  "intervention_layer": 1,
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
['盐酸', ' laba', '张掖', ' Сы']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.035  | 0.355070 | +0.186            |
| 2      | 'The'    | -1.285  | 0.276529 | -0.064            |
| 3      | '8'      | -1.535  | 0.215361 | -0.314            |
| 4      | 'Fact'   | -2.535  | 0.079227 | +0.186            |
| 5      | 'Number' | -3.910  | 0.020032 | +0.186            |
| 6      | '###'    | -4.160  | 0.015601 | +0.061            |
| 7      | '6'      | -4.410  | 0.012150 | +2.561            |
| 8      | '1'      | -5.160  | 0.005739 | +1.186            |
| 9      | '4'      | -5.785  | 0.003072 | -0.439            |
| 10     | 'Eight'  | -5.785  | 0.003072 | +1.061            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
