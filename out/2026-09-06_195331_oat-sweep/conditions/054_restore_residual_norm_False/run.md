---
condition_id: "054_restore_residual_norm_False"
axis: "restore_residual_norm"
value: "False"
is_default: false
swap_log_odds_shift: 2.375
valid_answer_mass: 0.6129652261734009
p4: 0.16485172510147095
p8: 0.44811347126960754
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "6"
readout_overlap: 0.0
log: "conditions/054_restore_residual_norm_False/run.md"
---

# 054_restore_residual_norm_False

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
  "restore_residual_norm": false,
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
[' Ponadto', 'يلات', '政法大学', '베이스', 'NEG', 'χω', 'укра', '伊斯兰']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
6<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.803  | 0.448113 | -0.751            |
| 2      | '6'       | -1.428  | 0.239858 | +3.249            |
| 3      | '4'       | -1.803  | 0.164852 | +1.624            |
| 4      | '2'       | -2.928  | 0.053520 | +4.749            |
| 5      | '1'       | -2.928  | 0.053520 | +3.624            |
| 6      | '3'       | -4.303  | 0.013532 | +3.624            |
| 7      | '0'       | -4.803  | 0.008207 | +3.686            |
| 8      | '5'       | -5.428  | 0.004393 | +2.999            |
| 9      | '<think>' | -5.553  | 0.003877 | +0.249            |
| 10     | '7'       | -6.553  | 0.001426 | +1.811            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
