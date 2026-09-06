---
condition_id: "011_normalization_strength_C=8,component_norm=False,residual_norm=True"
axis: "normalization_strength"
value: "C=8,component_norm=False,residual_norm=True"
is_default: false
swap_log_odds_shift: 2.374999761581421
valid_answer_mass: 0.02797798253595829
p4: 0.004142060875892639
p8: 0.02383592166006565
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/011_normalization_strength_C=8,component_norm=False,residual_norm=True/run.md"
---

# 011_normalization_strength_C=8,component_norm=False,residual_norm=True

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
[' responseData', ' Контакты', '豆角', 'Xã', '避け', '内容的真实性', '灵敏', 'ué']
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
| 1      | '**'     | -0.987  | 0.372857 | +0.235            |
| 2      | 'The'    | -1.362  | 0.256260 | -0.140            |
| 3      | 'Fact'   | -1.737  | 0.176125 | +0.985            |
| 4      | '6'      | -3.487  | 0.030606 | +3.485            |
| 5      | '8'      | -3.737  | 0.023836 | -2.515            |
| 6      | '###'    | -3.737  | 0.023836 | +0.485            |
| 7      | 'Number' | -3.987  | 0.018563 | +0.110            |
| 8      | 'There'  | -3.987  | 0.018563 | +4.610            |
| 9      | 'Based'  | -4.112  | 0.016382 | +4.547            |
| 10     | 'It'     | -4.487  | 0.011259 | +6.235            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
