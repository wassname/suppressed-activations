---
condition_id: "050_strength_1.0"
axis: "strength"
value: "1.0"
is_default: false
swap_log_odds_shift: -0.5
valid_answer_mass: 0.9834533333778381
p4: 0.019995924085378647
p8: 0.9634574055671692
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/050_strength_1.0/run.md"
---

# 050_strength_1.0

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
  "strength": 1.0,
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
['Spin', '-spin', 'spin', '\tspin', ' Spin', '盐酸', '_spin', ' laba']
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
| 1      | '8'       | -0.037  | 0.963457 | +0.014            |
| 2      | '4'       | -3.912  | 0.019996 | -0.486            |
| 3      | '6'       | -4.662  | 0.009445 | +0.014            |
| 4      | '<think>' | -5.912  | 0.002706 | -0.111            |
| 5      | '1'       | -6.787  | 0.001128 | -0.236            |
| 6      | 'Eight'   | -7.287  | 0.000684 | +0.014            |
| 7      | '2'       | -7.787  | 0.000415 | -0.111            |
| 8      | '3'       | -8.162  | 0.000285 | -0.236            |
| 9      | '0'       | -8.475  | 0.000209 | +0.014            |
| 10     | '5'       | -8.600  | 0.000184 | -0.173            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
