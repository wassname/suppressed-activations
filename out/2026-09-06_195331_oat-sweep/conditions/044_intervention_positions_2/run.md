---
condition_id: "044_intervention_positions_2"
axis: "intervention_positions"
value: "2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.98354572057724
p4: 0.03254156932234764
p8: 0.951004147529602
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/044_intervention_positions_2/run.md"
---

# 044_intervention_positions_2

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
  "intervention_positions": 2,
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
[' Ủy', 'ปั่น', '-spin', ' laba', ' Presents', 'seh', 'Spin', 'Integrated']
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
| 1      | '8'       | -0.050  | 0.951004 | +0.001            |
| 2      | '4'       | -3.425  | 0.032542 | +0.001            |
| 3      | '6'       | -4.800  | 0.008228 | -0.124            |
| 4      | '<think>' | -5.800  | 0.003027 | +0.001            |
| 5      | '1'       | -6.550  | 0.001430 | +0.001            |
| 6      | 'Eight'   | -7.300  | 0.000675 | +0.001            |
| 7      | '2'       | -7.675  | 0.000464 | +0.001            |
| 8      | '3'       | -7.863  | 0.000385 | +0.064            |
| 9      | '7'       | -8.300  | 0.000248 | +0.064            |
| 10     | '5'       | -8.425  | 0.000219 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
