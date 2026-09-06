---
condition_id: "013_layer_combo_L=26_positions=4_C=2"
axis: "layer_combo"
value: "L=26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.1875
valid_answer_mass: 0.0005034497007727623
p4: 1.1695955208779196e-06
p8: 0.000502280134242028
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/013_layer_combo_L=26_positions=4_C=2/run.md"
---

# 013_layer_combo_L=26_positions=4_C=2

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
  "intervention_layer": [
    26
  ],
  "intervention_positions": 4,
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
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
[' spinning', ' spin', ' spins', '在校园', '纺', '-spin', 'Spin', ' spun']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "26": {
    "residual_norm": 57.94782638549805,
    "perturbation_norm": 16.915143966674805,
    "relative_perturbation_by_position": [
      0.3891999423503876,
      0.29744160175323486,
      0.23222127556800842,
      0.18552887439727783
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908144 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065786 | -0.000            |
| 3      | 'Most'   | -5.471  | 0.004206 | +0.125            |
| 4      | 'To'     | -5.596  | 0.003711 | +0.125            |
| 5      | 'Sp'     | -5.846  | 0.002890 | -0.250            |
| 6      | 'An'     | -5.971  | 0.002551 | +0.125            |
| 7      | '**'     | -6.221  | 0.001987 | -0.000            |
| 8      | 'Animal' | -7.096  | 0.000828 | -0.000            |
| 9      | 'Anim'   | -7.096  | 0.000828 | -0.125            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
