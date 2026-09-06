---
condition_id: "023_intervention_layer_13"
axis: "intervention_layer"
value: "13"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.9324945211410522
p4: 0.04422435909509659
p8: 0.8882701396942139
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/023_intervention_layer_13/run.md"
---

# 023_intervention_layer_13

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
  "intervention_layer": 13,
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
[' Presents', '\tspin', 'ปั่น', ' Ủy', ' laba', 'umd', '领头羊', 'ಲು']
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
| 1      | '8'       | -0.118  | 0.888270 | -0.067            |
| 2      | '6'       | -2.868  | 0.056785 | +1.808            |
| 3      | '4'       | -3.118  | 0.044224 | +0.308            |
| 4      | '<think>' | -5.868  | 0.002827 | -0.067            |
| 5      | '1'       | -6.368  | 0.001715 | +0.183            |
| 6      | '2'       | -6.743  | 0.001179 | +0.933            |
| 7      | 'Eight'   | -6.993  | 0.000918 | +0.308            |
| 8      | '3'       | -7.368  | 0.000631 | +0.558            |
| 9      | '5'       | -7.681  | 0.000462 | +0.745            |
| 10     | '0'       | -7.931  | 0.000359 | +0.558            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
