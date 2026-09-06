---
condition_id: "007_readout_positions_2"
axis: "readout_positions"
value: "2"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.37116357684135437
p4: 0.004077953286468983
p8: 0.36708563566207886
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/007_readout_positions_2/run.md"
---

# 007_readout_positions_2

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 2,
  "rank": 8,
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
['Agama', '丰台区', '环境变量', 'اطر', '窓口', '文化传媒有限公司', '的小吃', '犹太人']
```

Unmodified donor readout:

```python
['\tva', '豆角', 'gos', ' Lounge', ' Kepolisian', ' законода', ' выставке', 'สุนัข']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.002  | 0.367086 | +0.219            |
| 2      | '**'     | -1.127  | 0.323952 | +0.094            |
| 3      | 'The'    | -1.627  | 0.196487 | -0.406            |
| 4      | 'Fact'   | -2.752  | 0.063790 | -0.031            |
| 5      | 'Number' | -4.002  | 0.018276 | +0.094            |
| 6      | '###'    | -4.502  | 0.011085 | -0.281            |
| 7      | '4'      | -5.502  | 0.004078 | -0.156            |
| 8      | '1'      | -6.127  | 0.002183 | +0.219            |
| 9      | 'Eight'  | -6.377  | 0.001700 | +0.469            |
| 10     | '6'      | -6.502  | 0.001500 | +0.469            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
