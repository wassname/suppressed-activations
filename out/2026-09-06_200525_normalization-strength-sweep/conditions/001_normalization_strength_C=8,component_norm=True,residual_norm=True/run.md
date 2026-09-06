---
condition_id: "001_normalization_strength_C=8,component_norm=True,residual_norm=True"
axis: "normalization_strength"
value: "C=8,component_norm=True,residual_norm=True"
is_default: false
swap_log_odds_shift: 5.125
valid_answer_mass: 0.026309460401535034
p4: 0.01923375576734543
p8: 0.007075703702867031
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/001_normalization_strength_C=8,component_norm=True,residual_norm=True/run.md"
---

# 001_normalization_strength_C=8,component_norm=True,residual_norm=True

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
[' nodeId', 'はこちら', 'Force', '匪浅', '豆角', ' solidaridad', ' Básica', ' største']
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
| 1      | '**'     | -0.951  | 0.386320 | +0.270            |
| 2      | 'Fact'   | -1.326  | 0.265514 | +1.395            |
| 3      | 'The'    | -1.576  | 0.206782 | -0.355            |
| 4      | 'Number' | -3.701  | 0.024697 | +0.395            |
| 5      | '###'    | -3.701  | 0.024697 | +0.520            |
| 6      | '4'      | -3.951  | 0.019234 | +1.395            |
| 7      | '6'      | -4.076  | 0.016974 | +2.895            |
| 8      | '8'      | -4.951  | 0.007076 | -3.730            |
| 9      | '1'      | -5.326  | 0.004863 | +1.020            |
| 10     | 'Based'  | -5.326  | 0.004863 | +3.333            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
