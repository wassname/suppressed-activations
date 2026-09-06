---
condition_id: "015_intervention_layer_5"
axis: "intervention_layer"
value: "5"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.9806538820266724
p4: 0.025455180555582047
p8: 0.9551987051963806
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/015_intervention_layer_5/run.md"
---

# 015_intervention_layer_5

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
  "intervention_layer": 5,
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
['盐酸', ' laba', 'Spin', '\tspin', ' mdi', ' webView', 'Integrated', ' веб']
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
| 1      | '8'       | -0.046  | 0.955199 | +0.005            |
| 2      | '4'       | -3.671  | 0.025455 | -0.245            |
| 3      | '6'       | -4.546  | 0.010611 | +0.130            |
| 4      | '<think>' | -5.796  | 0.003040 | +0.005            |
| 5      | '1'       | -6.171  | 0.002089 | +0.380            |
| 6      | '2'       | -7.546  | 0.000528 | +0.130            |
| 7      | 'Eight'   | -7.608  | 0.000496 | -0.307            |
| 8      | '0'       | -7.983  | 0.000341 | +0.505            |
| 9      | '3'       | -8.046  | 0.000320 | -0.120            |
| 10     | '5'       | -8.483  | 0.000207 | -0.057            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
