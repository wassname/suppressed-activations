---
condition_id: "045_intervention_positions_3"
axis: "intervention_positions"
value: "3"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.9871950149536133
p4: 0.041548795998096466
p8: 0.9456462264060974
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/045_intervention_positions_3/run.md"
---

# 045_intervention_positions_3

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
  "intervention_positions": 3,
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
[' Ủy', 'ปั่น', '-spin', ' Presents', 'seh', 'Spin', '盐酸', ' laba']
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
| 1      | '8'       | -0.056  | 0.945646 | -0.005            |
| 2      | '4'       | -3.181  | 0.041549 | +0.245            |
| 3      | '6'       | -5.181  | 0.005623 | -0.505            |
| 4      | '<think>' | -5.931  | 0.002656 | -0.130            |
| 5      | '1'       | -6.681  | 0.001255 | -0.130            |
| 6      | 'Eight'   | -7.556  | 0.000523 | -0.255            |
| 7      | '2'       | -7.681  | 0.000462 | -0.005            |
| 8      | '3'       | -7.743  | 0.000434 | +0.183            |
| 9      | '5'       | -8.431  | 0.000218 | -0.005            |
| 10     | '0'       | -8.493  | 0.000205 | -0.005            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
