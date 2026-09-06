---
condition_id: "022_layer_combo_L=24_26_positions=4_C=4"
axis: "layer_combo"
value: "L=24+26,positions=4,C=4"
is_default: false
swap_log_odds_shift: -0.0625004768371582
valid_answer_mass: 0.0005688233068212867
p4: 1.0296897698935936e-06
p8: 0.0005677936132997274
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/022_layer_combo_L=24_26_positions=4_C=4/run.md"
---

# 022_layer_combo_L=24_26_positions=4_C=4

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
  "intervention_positions": 4,
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
['狗粮', 'seh', 'แมว', '寵物', ' Pets', 'สุนัข', 'DOG', '萌宠']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 51.30626678466797,
    "perturbation_norm": 22.296611785888672,
    "relative_perturbation_by_position": [
      0.5904408693313599,
      0.4632904529571533,
      0.27617380023002625,
      0.32765012979507446
    ]
  },
  "26": {
    "residual_norm": 55.586612701416016,
    "perturbation_norm": 37.450252532958984,
    "relative_perturbation_by_position": [
      0.8511618971824646,
      0.7690946459770203,
      0.4151727557182312,
      0.5773127675056458
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.099  | 0.905967 | -0.003            |
| 2      | 'Based' | -2.724  | 0.065628 | -0.003            |
| 3      | 'Sp'    | -5.474  | 0.004195 | +0.122            |
| 4      | 'Most'  | -5.474  | 0.004195 | +0.122            |
| 5      | 'To'    | -5.599  | 0.003702 | +0.122            |
| 6      | 'An'    | -5.849  | 0.002883 | +0.247            |
| 7      | '**'    | -6.099  | 0.002246 | +0.122            |
| 8      | 'There' | -7.099  | 0.000826 | -0.003            |
| 9      | 'First' | -7.099  | 0.000826 | +0.122            |
| 10     | 'Anim'  | -7.224  | 0.000729 | -0.253            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
