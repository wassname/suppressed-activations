---
condition_id: "018_layer_combo_L=24_26_positions=1_C=4"
axis: "layer_combo"
value: "L=24+26,positions=1,C=4"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.000574823294300586
p4: 9.776149454410188e-07
p8: 0.0005738456966355443
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/018_layer_combo_L=24_26_positions=1_C=4/run.md"
---

# 018_layer_combo_L=24_26_positions=1_C=4

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
  "strength": 4.0,
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
['seh', '狗粮', '养犬', ' Sebag', 'สุนัข', ' perros', '寵', 'กัด']
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
    "perturbation_norm": 7.80852746963501,
    "relative_perturbation_by_position": [
      0.32765012979507446
    ]
  },
  "26": {
    "residual_norm": 26.11289405822754,
    "perturbation_norm": 15.195252418518066,
    "relative_perturbation_by_position": [
      0.5819060802459717
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
| 1      | 'The'    | -0.088  | 0.915623 | +0.008            |
| 2      | 'Based'  | -2.838  | 0.058534 | -0.117            |
| 3      | 'Sp'     | -5.588  | 0.003742 | +0.008            |
| 4      | 'Most'   | -5.588  | 0.003742 | +0.008            |
| 5      | 'To'     | -5.713  | 0.003302 | +0.008            |
| 6      | 'An'     | -6.088  | 0.002270 | +0.008            |
| 7      | '**'     | -6.338  | 0.001768 | -0.117            |
| 8      | 'Anim'   | -6.963  | 0.000946 | +0.008            |
| 9      | 'There'  | -7.088  | 0.000835 | +0.008            |
| 10     | 'Animal' | -7.088  | 0.000835 | +0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
