---
condition_id: "006_normalization_strength_C=8,component_norm=True,residual_norm=False"
axis: "normalization_strength"
value: "C=8,component_norm=True,residual_norm=False"
is_default: false
swap_log_odds_shift: 5.375
valid_answer_mass: 0.02346516028046608
p4: 0.018239466473460197
p8: 0.005225694738328457
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/006_normalization_strength_C=8,component_norm=True,residual_norm=False/run.md"
---

# 006_normalization_strength_C=8,component_norm=True,residual_norm=False

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
[' ОГ', '质量体系', 'gör', '国风', ' Hél', ' Empresarial', ' Baghdad', ' gravidanza']
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
| 1      | '**'     | -0.879  | 0.415128 | +0.342            |
| 2      | 'Fact'   | -1.504  | 0.222202 | +1.217            |
| 3      | 'The'    | -1.504  | 0.222202 | -0.283            |
| 4      | '###'    | -3.504  | 0.030072 | +0.717            |
| 5      | 'Number' | -3.629  | 0.026538 | +0.467            |
| 6      | '4'      | -4.004  | 0.018239 | +1.342            |
| 7      | '6'      | -4.129  | 0.016096 | +2.842            |
| 8      | '1'      | -5.129  | 0.005921 | +1.217            |
| 9      | '8'      | -5.254  | 0.005226 | -4.033            |
| 10     | '2'      | -5.629  | 0.003592 | +2.092            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
