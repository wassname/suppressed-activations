---
condition_id: "030_intervention_layer_20"
axis: "intervention_layer"
value: "20"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9809542894363403
p4: 0.028753960505127907
p8: 0.9522003531455994
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/030_intervention_layer_20/run.md"
---

# 030_intervention_layer_20

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
  "intervention_layer": 20,
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
[' webové', ' webView', '\tspin', ' веб', 'seh', ' HttpContext', ' fär', 'meldung']
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
| 1      | '8'       | -0.049  | 0.952200 | +0.002            |
| 2      | '4'       | -3.549  | 0.028754 | -0.123            |
| 3      | '6'       | -4.549  | 0.010578 | +0.127            |
| 4      | '<think>' | -5.674  | 0.003434 | +0.127            |
| 5      | '1'       | -6.674  | 0.001263 | -0.123            |
| 6      | 'Eight'   | -7.299  | 0.000676 | +0.002            |
| 7      | '2'       | -7.674  | 0.000465 | +0.002            |
| 8      | '3'       | -7.986  | 0.000340 | -0.060            |
| 9      | '7'       | -8.361  | 0.000234 | +0.002            |
| 10     | '0'       | -8.424  | 0.000220 | +0.065            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
