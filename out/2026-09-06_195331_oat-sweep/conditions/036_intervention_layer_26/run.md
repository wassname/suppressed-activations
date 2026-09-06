---
condition_id: "036_intervention_layer_26"
axis: "intervention_layer"
value: "26"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.9833095073699951
p4: 0.03670388087630272
p8: 0.9466056227684021
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/036_intervention_layer_26/run.md"
---

# 036_intervention_layer_26

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
  "intervention_layer": 26,
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
[' spinning', 'web', ' spin', ' spins', ' Ủy', '.Sp', '纺', '\tsp']
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
| 1      | '8'       | -0.055  | 0.946606 | -0.004            |
| 2      | '4'       | -3.305  | 0.036704 | +0.121            |
| 3      | '6'       | -4.805  | 0.008190 | -0.129            |
| 4      | '<think>' | -5.680  | 0.003414 | +0.121            |
| 5      | '1'       | -6.680  | 0.001256 | -0.129            |
| 6      | 'Eight'   | -7.305  | 0.000672 | -0.004            |
| 7      | '2'       | -7.617  | 0.000492 | +0.059            |
| 8      | '3'       | -7.805  | 0.000408 | +0.121            |
| 9      | '5'       | -8.367  | 0.000232 | +0.059            |
| 10     | '7'       | -8.367  | 0.000232 | -0.004            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
