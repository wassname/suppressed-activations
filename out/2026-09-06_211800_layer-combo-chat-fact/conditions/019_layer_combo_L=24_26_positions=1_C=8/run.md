---
condition_id: "019_layer_combo_L=24_26_positions=1_C=8"
axis: "layer_combo"
value: "L=24+26,positions=1,C=8"
is_default: false
swap_log_odds_shift: -0.0624995231628418
valid_answer_mass: 0.0005084919393993914
p4: 9.204781576954701e-07
p8: 0.0005075714434497058
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/019_layer_combo_L=24_26_positions=1_C=8/run.md"
---

# 019_layer_combo_L=24_26_positions=1_C=8

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
    24,
    26
  ],
  "intervention_positions": 1,
  "strength": 8.0,
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
['seh', '狗粮', 'สุนัข', '宠物', ' cães', ' собак', ' собаки', '寵物']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 23.831907272338867,
    "perturbation_norm": 14.176544189453125,
    "relative_perturbation_by_position": [
      0.5948556065559387
    ]
  },
  "26": {
    "residual_norm": 25.734949111938477,
    "perturbation_norm": 29.605619430541992,
    "relative_perturbation_by_position": [
      1.1504051685333252
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
| 1      | 'The'    | -0.086  | 0.917711 | +0.010            |
| 2      | 'Based'  | -2.836  | 0.058667 | -0.115            |
| 3      | 'Most'   | -5.586  | 0.003750 | +0.010            |
| 4      | 'Sp'     | -5.836  | 0.002921 | -0.240            |
| 5      | 'To'     | -5.836  | 0.002921 | -0.115            |
| 6      | 'An'     | -6.086  | 0.002275 | +0.010            |
| 7      | '**'     | -6.336  | 0.001772 | -0.115            |
| 8      | 'Animal' | -7.086  | 0.000837 | +0.010            |
| 9      | 'There'  | -7.211  | 0.000739 | -0.115            |
| 10     | 'Anim'   | -7.211  | 0.000739 | -0.240            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
