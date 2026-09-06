---
condition_id: "012_normalization_strength_C=16,component_norm=False,residual_norm=True"
axis: "normalization_strength"
value: "C=16,component_norm=False,residual_norm=True"
is_default: false
swap_log_odds_shift: 4.6875
valid_answer_mass: 2.6129853722522967e-05
p4: 1.6645521100144833e-05
p8: 9.484332622378133e-06
repeated_bigram_fraction: 0.06451612903225812
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/012_normalization_strength_C=16,component_norm=False,residual_norm=True/run.md"
---

# 012_normalization_strength_C=16,component_norm=False,residual_norm=True

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
  "intervention_positions": "all",
  "strength": 16.0,
  "match_component_norm": false,
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
['\tMethod', '豆角', 'informations', '평가', ' Trilogy', '豆类', 'アニメ', '_method']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that **digs** webs is **8**.

**Explanation:**
The animal that digs webs is the
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.816  | 0.442255 | +0.406            |
| 2      | 'Fact'     | -1.316  | 0.268241 | +1.406            |
| 3      | 'The'      | -1.816  | 0.162696 | -0.594            |
| 4      | '###'      | -3.191  | 0.041136 | +1.031            |
| 5      | 'It'       | -3.691  | 0.024950 | +7.031            |
| 6      | 'There'    | -4.066  | 0.017148 | +4.531            |
| 7      | 'Based'    | -4.566  | 0.010401 | +4.093            |
| 8      | 'I'        | -4.816  | 0.008100 | +6.218            |
| 9      | 'Here'     | -5.941  | 0.002630 | +3.781            |
| 10     | 'Actually' | -6.191  | 0.002048 | +4.031            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
