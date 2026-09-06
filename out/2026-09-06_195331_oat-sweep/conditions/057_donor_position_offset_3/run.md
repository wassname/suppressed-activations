---
condition_id: "057_donor_position_offset_3"
axis: "donor_position_offset"
value: "3"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.8975143432617188
p4: 0.026308143511414528
p8: 0.8712062239646912
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/057_donor_position_offset_3/run.md"
---

# 057_donor_position_offset_3

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
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 3
}
```

Source input (`repr`):

```python
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['盐酸', ' laba', ' webView', 'må', 'ränkt', ' Infant', ' Сы', 'くださ']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.138  | 0.871206 | -0.087            |
| 2      | '6'       | -2.513  | 0.081035 | +2.163            |
| 3      | '4'       | -3.638  | 0.026308 | -0.212            |
| 4      | '1'       | -4.888  | 0.007537 | +1.663            |
| 5      | '2'       | -5.388  | 0.004572 | +2.288            |
| 6      | '<think>' | -5.763  | 0.003142 | +0.038            |
| 7      | '3'       | -6.638  | 0.001310 | +1.288            |
| 8      | '0'       | -7.138  | 0.000794 | +1.351            |
| 9      | '5'       | -7.450  | 0.000581 | +0.976            |
| 10     | 'Eight'   | -7.450  | 0.000581 | -0.149            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
