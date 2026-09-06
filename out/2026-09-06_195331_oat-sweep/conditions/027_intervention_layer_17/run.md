---
condition_id: "027_intervention_layer_17"
axis: "intervention_layer"
value: "17"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9800114631652832
p4: 0.02872631885111332
p8: 0.9512851238250732
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/027_intervention_layer_17/run.md"
---

# 027_intervention_layer_17

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
  "intervention_layer": 17,
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
['\tspin', ' Presents', 'ปั่น', 'สปิน', 'Spin', '哈密', 'kab', 'meldung']
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
| 1      | '8'       | -0.050  | 0.951285 | +0.001            |
| 2      | '4'       | -3.550  | 0.028726 | -0.124            |
| 3      | '6'       | -4.425  | 0.011975 | +0.251            |
| 4      | '<think>' | -5.925  | 0.002672 | -0.124            |
| 5      | '1'       | -6.425  | 0.001621 | +0.126            |
| 6      | 'Eight'   | -7.300  | 0.000676 | +0.001            |
| 7      | '2'       | -7.612  | 0.000494 | +0.064            |
| 8      | '3'       | -8.050  | 0.000319 | -0.124            |
| 9      | '5'       | -8.300  | 0.000249 | +0.126            |
| 10     | '7'       | -8.362  | 0.000233 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
