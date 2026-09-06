---
condition_id: "007_normalization_strength_C=16,component_norm=True,residual_norm=False"
axis: "normalization_strength"
value: "C=16,component_norm=True,residual_norm=False"
is_default: false
swap_log_odds_shift: 4.0
valid_answer_mass: 2.322462387382984e-05
p4: 1.0887485586863477e-05
p8: 1.2337138286966365e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/007_normalization_strength_C=16,component_norm=True,residual_norm=False/run.md"
---

# 007_normalization_strength_C=16,component_norm=True,residual_norm=False

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
  "match_component_norm": true,
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
[' Silicone', ' Instala', 'kł', 'ùi', ' Floral', '不渝', ' ске', '热情的']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that **wears** a dog tag is **four**.

### Explanation
The phrasing of your original
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.803  | 0.448029 | +0.419            |
| 2      | 'The'      | -1.178  | 0.307926 | +0.044            |
| 3      | '###'      | -2.053  | 0.128363 | +2.169            |
| 4      | 'Fact'     | -2.428  | 0.088222 | +0.294            |
| 5      | 'There'    | -5.178  | 0.005640 | +3.419            |
| 6      | 'Based'    | -5.678  | 0.003421 | +2.981            |
| 7      | 'It'       | -5.928  | 0.002664 | +4.794            |
| 8      | 'Here'     | -6.428  | 0.001616 | +3.294            |
| 9      | 'Actually' | -6.803  | 0.001111 | +3.419            |
| 10     | 'Number'   | -7.178  | 0.000763 | -3.081            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
