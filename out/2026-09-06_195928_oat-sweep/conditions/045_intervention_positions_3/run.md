---
condition_id: "045_intervention_positions_3"
axis: "intervention_positions"
value: "3"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28624168038368225
p4: 0.005148403346538544
p8: 0.2810932695865631
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/045_intervention_positions_3/run.md"
---

# 045_intervention_positions_3

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
  "intervention_layer": 1,
  "intervention_positions": 3,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', '\tspin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.144  | 0.318520 | +0.077            |
| 2      | '**'     | -1.269  | 0.281093 | -0.048            |
| 3      | '8'      | -1.269  | 0.281093 | -0.048            |
| 4      | 'Fact'   | -2.644  | 0.071072 | +0.077            |
| 5      | 'Number' | -4.144  | 0.015858 | -0.048            |
| 6      | '###'    | -4.269  | 0.013995 | -0.048            |
| 7      | '4'      | -5.269  | 0.005148 | +0.077            |
| 8      | '1'      | -6.519  | 0.001475 | -0.173            |
| 9      | 'Eight'  | -6.769  | 0.001149 | +0.077            |
| 10     | 'Answer' | -6.894  | 0.001014 | +0.077            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
