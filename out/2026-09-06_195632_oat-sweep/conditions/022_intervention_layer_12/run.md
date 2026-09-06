---
condition_id: "022_intervention_layer_12"
axis: "intervention_layer"
value: "12"
is_default: false
swap_log_odds_shift: 0.6875
valid_answer_mass: 0.0004980211379006505
p4: 1.9046738088945858e-06
p8: 0.00049611646682024
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/022_intervention_layer_12/run.md"
---

# 022_intervention_layer_12

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
  "intervention_layer": 12,
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
['丝绸', ' 인프라', 'Spin', '웹', ' krém', 'seh', '在校园', '丝瓜']
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.109  | 0.897000 | -0.013            |
| 2      | 'Based'  | -2.484  | 0.083434 | +0.237            |
| 3      | 'To'     | -5.484  | 0.004154 | +0.237            |
| 4      | 'An'     | -5.984  | 0.002519 | +0.112            |
| 5      | '**'     | -6.234  | 0.001962 | -0.013            |
| 6      | 'First'  | -6.484  | 0.001528 | +0.737            |
| 7      | 'Sp'     | -6.859  | 0.001050 | -1.263            |
| 8      | 'Most'   | -6.859  | 0.001050 | -1.263            |
| 9      | 'Animal' | -7.359  | 0.000637 | -0.263            |
| 10     | 'That'   | -7.484  | 0.000562 | +0.112            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
