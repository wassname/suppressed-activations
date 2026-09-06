---
condition_id: "025_intervention_layer_15"
axis: "intervention_layer"
value: "15"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.9777609705924988
p4: 0.022466376423835754
p8: 0.9552946090698242
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/025_intervention_layer_15/run.md"
---

# 025_intervention_layer_15

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
  "intervention_layer": 15,
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
[' Presents', '\tspin', 'ปั่น', ' laba', '哈密', '领头羊', 'meldung', 'สปิน']
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
| 1      | '8'       | -0.046  | 0.955295 | +0.006            |
| 2      | '4'       | -3.796  | 0.022466 | -0.369            |
| 3      | '6'       | -4.296  | 0.013627 | +0.381            |
| 4      | '<think>' | -5.921  | 0.002683 | -0.119            |
| 5      | 'Eight'   | -6.671  | 0.001267 | +0.631            |
| 6      | '1'       | -6.796  | 0.001119 | -0.244            |
| 7      | '2'       | -7.796  | 0.000411 | -0.119            |
| 8      | '3'       | -8.171  | 0.000283 | -0.244            |
| 9      | 'The'     | -8.358  | 0.000234 | +0.881            |
| 10     | '5'       | -8.546  | 0.000194 | -0.119            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
