---
condition_id: "019_intervention_layer_9"
axis: "intervention_layer"
value: "9"
is_default: false
swap_log_odds_shift: 1.0
valid_answer_mass: 0.948333740234375
p4: 0.0807022973895073
p8: 0.8676314353942871
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/019_intervention_layer_9/run.md"
---

# 019_intervention_layer_9

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
  "intervention_layer": 9,
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
['-spin', 'Spin', '纺', 'spin', 'ปั่น', '\tspin', ' Ủy', 'seh']
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
| 1      | '8'       | -0.142  | 0.867631 | -0.091            |
| 2      | '4'       | -2.517  | 0.080702 | +0.909            |
| 3      | '6'       | -3.267  | 0.038121 | +1.409            |
| 4      | '<think>' | -5.642  | 0.003546 | +0.159            |
| 5      | '1'       | -5.642  | 0.003546 | +0.909            |
| 6      | '2'       | -6.767  | 0.001151 | +0.909            |
| 7      | 'Eight'   | -7.017  | 0.000897 | +0.284            |
| 8      | '3'       | -7.017  | 0.000897 | +0.909            |
| 9      | '5'       | -7.329  | 0.000656 | +1.097            |
| 10     | '7'       | -7.454  | 0.000579 | +0.909            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
