---
condition_id: "003_detector_layers_(12,_20,_28)"
axis: "detector_layers"
value: "(12, 20, 28)"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.9773743152618408
p4: 0.04113546758890152
p8: 0.9362388253211975
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/003_detector_layers_(12,_20,_28)/run.md"
---

# 003_detector_layers_(12,_20,_28)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    12,
    20,
    28
  ],
  "readout_positions": 4,
  "rank": 8,
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
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' food', '增添', ' heutigen', ' decreases', ' panduan', '姜', ' marker', 'jero']
```

Unmodified donor readout:

```python
['三八', '带头作用', '장으로', ' 한반', 'otes', ' satisfaire', './', ' qint']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.066  | 0.936239 | -0.015            |
| 2      | '4'       | -3.191  | 0.041135 | +0.235            |
| 3      | '6'       | -4.191  | 0.015133 | +0.485            |
| 4      | '<think>' | -6.066  | 0.002321 | -0.265            |
| 5      | '1'       | -6.566  | 0.001408 | -0.015            |
| 6      | 'Eight'   | -7.316  | 0.000665 | -0.015            |
| 7      | '2'       | -7.628  | 0.000486 | +0.048            |
| 8      | '3'       | -7.816  | 0.000403 | +0.110            |
| 9      | '5'       | -8.441  | 0.000216 | -0.015            |
| 10     | '0'       | -8.503  | 0.000203 | -0.015            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
