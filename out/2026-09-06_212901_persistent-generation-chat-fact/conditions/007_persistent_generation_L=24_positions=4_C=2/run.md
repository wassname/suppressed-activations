---
condition_id: "007_persistent_generation_L=24_positions=4_C=2"
axis: "persistent_generation"
value: "L=24,positions=4,C=2"
is_default: false
swap_log_odds_shift: 4.76837158203125e-07
valid_answer_mass: 0.0005750299897044897
p4: 1.1079307569161756e-06
p8: 0.0005739220650866628
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/007_persistent_generation_L=24_positions=4_C=2/run.md"
---

# 007_persistent_generation_L=24_positions=4_C=2

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
  "intervention_positions": 4,
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true
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
['狗粮', 'สุนัข', ' собаки', 'DOG', ' krém', 'seh', ' Ủy', ' dlg']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 24.46245765686035,
    "perturbation_norm": 3.659008026123047,
    "relative_perturbation_by_position": [
      0.14957647025585175
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
| 1      | 'The'    | -0.088  | 0.915745 | +0.008            |
| 2      | 'Based'  | -2.838  | 0.058542 | -0.117            |
| 3      | 'Most'   | -5.588  | 0.003742 | +0.008            |
| 4      | 'Sp'     | -5.713  | 0.003303 | -0.117            |
| 5      | 'To'     | -5.713  | 0.003303 | +0.008            |
| 6      | 'An'     | -5.963  | 0.002572 | +0.133            |
| 7      | '**'     | -6.213  | 0.002003 | +0.008            |
| 8      | 'Animal' | -7.088  | 0.000835 | +0.008            |
| 9      | 'Anim'   | -7.088  | 0.000835 | -0.117            |
| 10     | 'There'  | -7.088  | 0.000835 | +0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
