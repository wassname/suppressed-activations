---
condition_id: "040_intervention_layer_30"
axis: "intervention_layer"
value: "30"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.985263466835022
p4: 0.028880268335342407
p8: 0.9563831686973572
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/040_intervention_layer_30/run.md"
---

# 040_intervention_layer_30

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
  "intervention_layer": 30,
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
[' spinning', ' spin', ' spins', ' Ủy', '.Sp', '纺', 'ปั่น', ' spun']
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
| 1      | '8'       | -0.045  | 0.956383 | +0.007            |
| 2      | '4'       | -3.545  | 0.028880 | -0.118            |
| 3      | '6'       | -4.920  | 0.007302 | -0.243            |
| 4      | '<think>' | -5.920  | 0.002686 | -0.118            |
| 5      | '1'       | -6.670  | 0.001269 | -0.118            |
| 6      | 'Eight'   | -7.295  | 0.000679 | +0.007            |
| 7      | '2'       | -7.732  | 0.000439 | -0.056            |
| 8      | '3'       | -7.982  | 0.000342 | -0.056            |
| 9      | '7'       | -8.482  | 0.000207 | -0.118            |
| 10     | '5'       | -8.545  | 0.000195 | -0.118            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
