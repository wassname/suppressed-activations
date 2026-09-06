---
condition_id: "014_intervention_layer_4"
axis: "intervention_layer"
value: "4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.8983697295188904
p4: 0.02972343936562538
p8: 0.8686462640762329
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/014_intervention_layer_4/run.md"
---

# 014_intervention_layer_4

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
  "intervention_layer": 4,
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
['盐酸', ' laba', ' webView', '蜘蛛', 'må', ' Peanut', ' Infant', '暴食']
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
| 1      | '8'       | -0.141  | 0.868646 | -0.090            |
| 2      | '6'       | -2.391  | 0.091555 | +2.285            |
| 3      | '4'       | -3.516  | 0.029723 | -0.090            |
| 4      | '1'       | -5.891  | 0.002765 | +0.660            |
| 5      | '<think>' | -6.266  | 0.001900 | -0.465            |
| 6      | '2'       | -6.516  | 0.001480 | +1.160            |
| 7      | '0'       | -6.891  | 0.001017 | +1.598            |
| 8      | '3'       | -7.266  | 0.000699 | +0.660            |
| 9      | '5'       | -7.766  | 0.000424 | +0.660            |
| 10     | 'Eight'   | -7.891  | 0.000374 | -0.590            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
