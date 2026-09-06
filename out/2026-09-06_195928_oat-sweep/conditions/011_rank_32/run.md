---
condition_id: "011_rank_32"
axis: "rank"
value: "32"
is_default: false
swap_log_odds_shift: 4.5
valid_answer_mass: 0.002801464172080159
p4: 0.0016603342955932021
p8: 0.001141129876486957
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/011_rank_32/run.md"
---

# 011_rank_32

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
  "rank": 32,
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
['单元的', '的场所', 'はこちら', ' Azienda', '的一瞬间', ' enseignants', 'の部分', 'につきまして', '专栏收录', 'Browse', '政法大学', ' اص', '_building', 'anismos', ' passiert', ' Localização', '年春节', ' Selv', 'esos', '_APPEND', ' более', '是一套', 'supply', '来时', '.RadioButton', ' Sitio', '内容的真实性', ' Econôm', 'dos', '伊斯兰', '금융', 'せい']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ', '录像', 'iht', '契', '_gold', '统战部', '레이션', 'Overlay', '吠', 'friends', 'qualification', ' DISCLAIM', 'ạch', '버', ' Unik', ' Тов', ' ruedas', ' Más', '粗糙', '村', 'vah', ' ausges', '디지털', 'Austr', ' prevenzione']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.651  | 0.521662 | +0.571            |
| 2      | 'The'    | -1.651  | 0.191909 | -0.429            |
| 3      | '###'    | -2.276  | 0.102721 | +1.946            |
| 4      | 'Fact'   | -2.651  | 0.070599 | +0.071            |
| 5      | 'Based'  | -3.401  | 0.033349 | +5.258            |
| 6      | 'It'     | -3.776  | 0.022920 | +6.946            |
| 7      | 'Here'   | -4.776  | 0.008432 | +4.946            |
| 8      | 'First'  | -4.776  | 0.008432 | +3.946            |
| 9      | 'Number' | -5.026  | 0.006567 | -0.929            |
| 10     | 'There'  | -5.151  | 0.005795 | +3.446            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
