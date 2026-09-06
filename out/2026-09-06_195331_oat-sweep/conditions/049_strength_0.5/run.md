---
condition_id: "049_strength_0.5"
axis: "strength"
value: "0.5"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9832379817962646
p4: 0.02882090024650097
p8: 0.9544171094894409
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/049_strength_0.5/run.md"
---

# 049_strength_0.5

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
  "strength": 0.5,
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
['Spin', '-spin', 'ปั่น', '\tspin', 'spin', ' Ủy', 'seh', ' laba']
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
| 1      | '8'       | -0.047  | 0.954417 | +0.005            |
| 2      | '4'       | -3.547  | 0.028821 | -0.120            |
| 3      | '6'       | -4.672  | 0.009357 | +0.005            |
| 4      | '<think>' | -5.922  | 0.002681 | -0.120            |
| 5      | '1'       | -6.672  | 0.001266 | -0.120            |
| 6      | 'Eight'   | -7.297  | 0.000678 | +0.005            |
| 7      | '2'       | -7.672  | 0.000466 | +0.005            |
| 8      | '3'       | -7.984  | 0.000341 | -0.058            |
| 9      | '0'       | -8.484  | 0.000207 | +0.005            |
| 10     | '5'       | -8.484  | 0.000207 | -0.058            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
