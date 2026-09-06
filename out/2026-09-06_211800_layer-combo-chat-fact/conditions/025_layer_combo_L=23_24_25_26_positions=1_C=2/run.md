---
condition_id: "025_layer_combo_L=23_24_25_26_positions=1_C=2"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=2"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.0005701585905626416
p4: 9.696814231574535e-07
p8: 0.0005691889091394842
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/025_layer_combo_L=23_24_25_26_positions=1_C=2/run.md"
---

# 025_layer_combo_L=23_24_25_26_positions=1_C=2

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
    23,
    24,
    25,
    26
  ],
  "intervention_positions": 1,
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
['狗粮', 'สุนัข', ' doga', '-spin', 'Spin', '和金', ' krém', 'seh']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 21.53727149963379,
    "perturbation_norm": 3.270266532897949,
    "relative_perturbation_by_position": [
      0.15184219181537628
    ]
  },
  "24": {
    "residual_norm": 23.57963752746582,
    "perturbation_norm": 3.9285433292388916,
    "relative_perturbation_by_position": [
      0.16660745441913605
    ]
  },
  "25": {
    "residual_norm": 24.84288787841797,
    "perturbation_norm": 2.5940394401550293,
    "relative_perturbation_by_position": [
      0.10441778600215912
    ]
  },
  "26": {
    "residual_norm": 25.910449981689453,
    "perturbation_norm": 2.8008527755737305,
    "relative_perturbation_by_position": [
      0.10809741914272308
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
| 1      | 'The'    | -0.096  | 0.908193 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065789 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003712 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003712 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003275 | -0.000            |
| 6      | 'An'     | -6.096  | 0.002251 | -0.000            |
| 7      | '**'     | -6.221  | 0.001987 | -0.000            |
| 8      | 'Animal' | -6.971  | 0.000938 | +0.125            |
| 9      | 'Anim'   | -6.971  | 0.000938 | -0.000            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
