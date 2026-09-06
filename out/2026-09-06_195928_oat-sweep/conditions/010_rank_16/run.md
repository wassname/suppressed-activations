---
condition_id: "010_rank_16"
axis: "rank"
value: "16"
is_default: false
swap_log_odds_shift: 3.875
valid_answer_mass: 0.007108447141945362
p4: 0.003112245351076126
p8: 0.003996201790869236
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/010_rank_16/run.md"
---

# 010_rank_16

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
  "rank": 16,
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
['内容的真实性', '的场所', 'Islam', '这一次的', ' Básica', ' Bố', 'Вт', ' responseData', ' enseignants', 'の部分', '政法大学', '配图', '(Bundle', ' gravidanza', 'anismos', '荣华']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ', '录像', 'iht', '契', '_gold', '统战部', '레이션', 'Overlay', '吠']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.772  | 0.461898 | +0.449            |
| 2      | 'The'    | -1.522  | 0.218185 | -0.301            |
| 3      | 'Fact'   | -2.022  | 0.132336 | +0.699            |
| 4      | '###'    | -2.772  | 0.062511 | +1.449            |
| 5      | 'Based'  | -3.397  | 0.033460 | +5.262            |
| 6      | 'Number' | -4.022  | 0.017910 | +0.074            |
| 7      | 'It'     | -4.147  | 0.015805 | +6.574            |
| 8      | 'There'  | -5.022  | 0.006589 | +3.574            |
| 9      | 'I'      | -5.272  | 0.005131 | +5.762            |
| 10     | 'Here'   | -5.397  | 0.004528 | +4.324            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
