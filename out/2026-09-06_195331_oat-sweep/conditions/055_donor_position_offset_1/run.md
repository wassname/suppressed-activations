---
condition_id: "055_donor_position_offset_1"
axis: "donor_position_offset"
value: "1"
is_default: false
swap_log_odds_shift: 2.25
valid_answer_mass: 0.7373518347740173
p4: 0.18071389198303223
p8: 0.5566379427909851
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/055_donor_position_offset_1/run.md"
---

# 055_donor_position_offset_1

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
  "donor_position_offset": 1
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
['誇る', 'วิส', ' Básica', ' bästa', '的场所', ' Bốn', ' Allgemeine', 'eby']
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
| 1      | '8'       | -0.586  | 0.556638 | -0.535            |
| 2      | '4'       | -1.711  | 0.180714 | +1.715            |
| 3      | '6'       | -2.211  | 0.109609 | +2.465            |
| 4      | '1'       | -2.586  | 0.075333 | +3.965            |
| 5      | '2'       | -3.211  | 0.040323 | +4.465            |
| 6      | '3'       | -4.586  | 0.010195 | +3.340            |
| 7      | '0'       | -4.836  | 0.007940 | +3.653            |
| 8      | '5'       | -5.086  | 0.006184 | +3.340            |
| 9      | '<think>' | -5.836  | 0.002921 | -0.035            |
| 10     | '7'       | -6.336  | 0.001772 | +2.028            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
