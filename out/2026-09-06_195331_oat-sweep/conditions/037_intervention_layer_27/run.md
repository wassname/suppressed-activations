---
condition_id: "037_intervention_layer_27"
axis: "intervention_layer"
value: "27"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9819702506065369
p4: 0.03248945251107216
p8: 0.9494807720184326
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/037_intervention_layer_27/run.md"
---

# 037_intervention_layer_27

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
  "intervention_layer": 27,
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
[' spinning', ' spin', ' spins', ' Ủy', '.Sp', '\tsp', '纺', 'ปั่น']
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
| 1      | '8'       | -0.052  | 0.949481 | -0.001            |
| 2      | '4'       | -3.427  | 0.032489 | -0.001            |
| 3      | '6'       | -4.677  | 0.009308 | -0.001            |
| 4      | '<think>' | -5.677  | 0.003424 | +0.124            |
| 5      | '1'       | -6.552  | 0.001427 | -0.001            |
| 6      | 'Eight'   | -7.302  | 0.000674 | -0.001            |
| 7      | '2'       | -7.614  | 0.000493 | +0.062            |
| 8      | '3'       | -7.802  | 0.000409 | +0.124            |
| 9      | '5'       | -8.302  | 0.000248 | +0.124            |
| 10     | '7'       | -8.364  | 0.000233 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
