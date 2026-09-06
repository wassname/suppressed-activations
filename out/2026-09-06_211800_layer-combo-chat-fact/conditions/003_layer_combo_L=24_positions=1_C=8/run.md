---
condition_id: "003_layer_combo_L=24_positions=1_C=8"
axis: "layer_combo"
value: "L=24,positions=1,C=8"
is_default: false
swap_log_odds_shift: -0.1250004768371582
valid_answer_mass: 0.0005702534690499306
p4: 9.698424037196673e-07
p8: 0.0005692836130037904
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/003_layer_combo_L=24_positions=1_C=8/run.md"
---

# 003_layer_combo_L=24_positions=1_C=8

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
    24
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
['狗粮', 'สุนัข', 'seh', ' собаки', 'DOG', ' собак', '狗狗', 'Dog']
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
| 1      | 'The'    | -0.096  | 0.908344 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065800 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003712 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003712 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003276 | -0.000            |
| 6      | 'An'     | -6.096  | 0.002252 | -0.000            |
| 7      | '**'     | -6.221  | 0.001987 | -0.000            |
| 8      | 'Animal' | -7.096  | 0.000828 | -0.000            |
| 9      | 'Anim'   | -7.096  | 0.000828 | -0.125            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
