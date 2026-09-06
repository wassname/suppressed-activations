---
condition_id: "052_strength_8.0"
axis: "strength"
value: "8.0"
is_default: false
swap_log_odds_shift: 3.875
valid_answer_mass: 0.4316678047180176
p4: 0.2686956524848938
p8: 0.16297215223312378
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "6"
readout_overlap: 0.0
log: "conditions/052_strength_8.0/run.md"
---

# 052_strength_8.0

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
['拉肚子', '政法大学', 'esos', '的场所', 'とのこと', '全般', 'はこちら', 'Force']
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
| 1      | '6'       | -0.939  | 0.390950 | +3.737            |
| 2      | '4'       | -1.314  | 0.268696 | +2.112            |
| 3      | '8'       | -1.814  | 0.162972 | -1.763            |
| 4      | '0'       | -2.564  | 0.076983 | +5.925            |
| 5      | '2'       | -3.439  | 0.032091 | +4.237            |
| 6      | '1'       | -3.689  | 0.024993 | +2.862            |
| 7      | '3'       | -4.314  | 0.013378 | +3.612            |
| 8      | '<think>' | -5.189  | 0.005577 | +0.612            |
| 9      | '5'       | -5.939  | 0.002634 | +2.487            |
| 10     | 'There'   | -6.064  | 0.002325 | +3.550            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
