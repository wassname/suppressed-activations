---
condition_id: "047_intervention_positions_8"
axis: "intervention_positions"
value: "8"
is_default: false
swap_log_odds_shift: 1.875
valid_answer_mass: 0.6363189816474915
p4: 0.11608082056045532
p8: 0.5202381610870361
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/047_intervention_positions_8/run.md"
---

# 047_intervention_positions_8

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
  "intervention_positions": 8,
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
[' Ponadto', 'χω', 'اطر', '政法大学', '的场所', ' responseData', ' Satgas', 'esos']
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
| 1      | '8'       | -0.653  | 0.520238 | -0.602            |
| 2      | '6'       | -1.278  | 0.278463 | +3.398            |
| 3      | '4'       | -2.153  | 0.116081 | +1.273            |
| 4      | '1'       | -3.278  | 0.037686 | +3.273            |
| 5      | '2'       | -3.653  | 0.025901 | +4.023            |
| 6      | '3'       | -4.903  | 0.007421 | +3.023            |
| 7      | '5'       | -5.778  | 0.003093 | +2.648            |
| 8      | '<think>' | -5.903  | 0.002730 | -0.102            |
| 9      | '0'       | -5.903  | 0.002730 | +2.585            |
| 10     | '7'       | -6.778  | 0.001138 | +1.585            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
