---
condition_id: "032_intervention_layer_22"
axis: "intervention_layer"
value: "22"
is_default: false
swap_log_odds_shift: 0.0624995231628418
valid_answer_mass: 0.0005035650683566928
p4: 1.0326823485229397e-06
p8: 0.000502532406244427
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/032_intervention_layer_22/run.md"
---

# 032_intervention_layer_22

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
  "intervention_layer": 22,
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
['seh', '和金', 'Integrated', '\')."', 'modifiers', '第二人民医院', '的神奇', ' Страна']
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
| 1      | 'The'    | -0.096  | 0.908600 | +0.000            |
| 2      | 'Based'  | -2.721  | 0.065819 | +0.000            |
| 3      | 'Most'   | -5.471  | 0.004208 | +0.125            |
| 4      | 'Sp'     | -5.596  | 0.003713 | +0.000            |
| 5      | 'To'     | -5.846  | 0.002892 | -0.125            |
| 6      | 'An'     | -6.096  | 0.002252 | +0.000            |
| 7      | '**'     | -6.221  | 0.001988 | +0.000            |
| 8      | 'There'  | -7.096  | 0.000829 | +0.000            |
| 9      | 'Anim'   | -7.096  | 0.000829 | -0.125            |
| 10     | 'Animal' | -7.221  | 0.000731 | -0.125            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
