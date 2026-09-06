---
condition_id: "031_layer_combo_L=23_24_25_26_positions=4_C=8"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.6874995231628418
valid_answer_mass: 0.0005039377720095217
p4: 4.886948659077461e-07
p8: 0.0005034490604884923
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.375
log: "conditions/031_layer_combo_L=23_24_25_26_positions=4_C=8/run.md"
---

# 031_layer_combo_L=23_24_25_26_positions=4_C=8

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
  "intervention_positions": 4,
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
['狗粮', 'สุนัข', ' собак', ' собаки', ' dogs', '狗的', '狗狗', ' собака']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 47.84559631347656,
    "perturbation_norm": 29.717958450317383,
    "relative_perturbation_by_position": [
      0.7998456954956055,
      0.6343554854393005,
      0.37782272696495056,
      0.5469987392425537
    ]
  },
  "24": {
    "residual_norm": 47.82769775390625,
    "perturbation_norm": 56.34785461425781,
    "relative_perturbation_by_position": [
      1.2511184215545654,
      1.2251076698303223,
      1.065915822982788,
      1.1654739379882812
    ]
  },
  "25": {
    "residual_norm": 58.98676681518555,
    "perturbation_norm": 69.91759490966797,
    "relative_perturbation_by_position": [
      1.1900776624679565,
      1.2125194072723389,
      1.187092661857605,
      1.1497294902801514
    ]
  },
  "26": {
    "residual_norm": 67.26151275634766,
    "perturbation_norm": 80.57101440429688,
    "relative_perturbation_by_position": [
      1.1913522481918335,
      1.2069144248962402,
      1.1976635456085205,
      1.195389986038208
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The animal that is famous for spinning webs is the **spider**.

Spiders are arachnids, which means they have **eight** legs.
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.094  | 0.910257 | +0.002            |
| 2      | 'Based'   | -2.719  | 0.065939 | +0.002            |
| 3      | 'Most'    | -5.469  | 0.004215 | +0.127            |
| 4      | 'An'      | -5.844  | 0.002897 | +0.252            |
| 5      | 'To'      | -5.844  | 0.002897 | -0.123            |
| 6      | 'Sp'      | -6.094  | 0.002256 | -0.498            |
| 7      | '**'      | -6.219  | 0.001991 | +0.002            |
| 8      | '<think>' | -7.094  | 0.000830 | +0.377            |
| 9      | 'There'   | -7.219  | 0.000733 | -0.123            |
| 10     | 'First'   | -7.219  | 0.000733 | +0.002            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
