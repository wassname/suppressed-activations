---
condition_id: "019_intervention_layer_9"
axis: "intervention_layer"
value: "9"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.00048308714758604765
p4: 1.9662313661683584e-06
p8: 0.0004811209219042212
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['Spin', 'ปั่น', '\tspin', '盐酸', 'seh', '丝绸', 'spin', ' Ủy']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.139  | 0.869887 | -0.043            |
| 2      | 'Based' | -2.264  | 0.103893 | +0.457            |
| 3      | 'To'    | -5.014  | 0.006642 | +0.707            |
| 4      | 'Most'  | -6.014  | 0.002443 | -0.418            |
| 5      | 'An'    | -6.014  | 0.002443 | +0.082            |
| 6      | '**'    | -6.389  | 0.001679 | -0.168            |
| 7      | 'Sp'    | -6.389  | 0.001679 | -0.793            |
| 8      | 'First' | -6.639  | 0.001308 | +0.582            |
| 9      | 'There' | -6.889  | 0.001019 | +0.207            |
| 10     | 'This'  | -7.139  | 0.000793 | +0.707            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
