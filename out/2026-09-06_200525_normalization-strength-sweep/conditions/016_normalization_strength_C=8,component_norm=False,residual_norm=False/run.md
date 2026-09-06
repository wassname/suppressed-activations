---
condition_id: "016_normalization_strength_C=8,component_norm=False,residual_norm=False"
axis: "normalization_strength"
value: "C=8,component_norm=False,residual_norm=False"
is_default: false
swap_log_odds_shift: 2.25
valid_answer_mass: 0.036341626197099686
p4: 0.004832136444747448
p8: 0.03150948882102966
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/016_normalization_strength_C=8,component_norm=False,residual_norm=False/run.md"
---

# 016_normalization_strength_C=8,component_norm=False,residual_norm=False

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
  "strength": 8.0,
  "match_component_norm": false,
  "restore_residual_norm": false,
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
['豆角', ' высшего', '内容的真实性', ' Контакты', ' Registrier', ' formie', ' responseData', '晶圆']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.957  | 0.383864 | +0.264            |
| 2      | 'The'    | -1.332  | 0.263826 | -0.111            |
| 3      | 'Fact'   | -1.832  | 0.160018 | +0.889            |
| 4      | '6'      | -3.457  | 0.031509 | +3.514            |
| 5      | '8'      | -3.457  | 0.031509 | -2.236            |
| 6      | '###'    | -3.582  | 0.027807 | +0.639            |
| 7      | 'Number' | -4.082  | 0.016866 | +0.014            |
| 8      | 'There'  | -4.207  | 0.014884 | +4.389            |
| 9      | 'Based'  | -4.332  | 0.013135 | +4.327            |
| 10     | 'It'     | -4.832  | 0.007967 | +5.889            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
