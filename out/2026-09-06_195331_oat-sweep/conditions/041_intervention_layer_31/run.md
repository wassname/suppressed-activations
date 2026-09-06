---
condition_id: "041_intervention_layer_31"
axis: "intervention_layer"
value: "31"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9842743873596191
p4: 0.028851274400949478
p8: 0.95542311668396
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/041_intervention_layer_31/run.md"
---

# 041_intervention_layer_31

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
  "intervention_layer": 31,
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
[' spinning', 'web', '-web', '(web', ' spin', 'Web', ' spins', '资讯网']
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
| 1      | '8'       | -0.046  | 0.955423 | +0.006            |
| 2      | '4'       | -3.546  | 0.028851 | -0.119            |
| 3      | '6'       | -4.796  | 0.008266 | -0.119            |
| 4      | '<think>' | -5.921  | 0.002684 | -0.119            |
| 5      | '1'       | -6.671  | 0.001268 | -0.119            |
| 6      | 'Eight'   | -7.296  | 0.000679 | +0.006            |
| 7      | '2'       | -7.733  | 0.000438 | -0.057            |
| 8      | '3'       | -7.983  | 0.000341 | -0.057            |
| 9      | '7'       | -8.421  | 0.000220 | -0.057            |
| 10     | '5'       | -8.483  | 0.000207 | -0.057            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
