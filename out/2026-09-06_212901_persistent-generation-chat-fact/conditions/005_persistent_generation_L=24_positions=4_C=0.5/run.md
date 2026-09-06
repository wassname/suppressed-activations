---
condition_id: "005_persistent_generation_L=24_positions=4_C=0.5"
axis: "persistent_generation"
value: "L=24,positions=4,C=0.5"
is_default: false
swap_log_odds_shift: -0.0624995231628418
valid_answer_mass: 0.0005700772744603455
p4: 1.031960664477083e-06
p8: 0.0005690453108400106
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/005_persistent_generation_L=24_positions=4_C=0.5/run.md"
---

# 005_persistent_generation_L=24_positions=4_C=0.5

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
  "strength": 0.5,
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
['Integrated', ' Ủy', ' факта', '웹', '丝绸', ' krém', ' Presents', 'edata']
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
    "perturbation_norm": 0.917792558670044,
    "relative_perturbation_by_position": [
      0.03751841187477112
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
| 1      | 'The'    | -0.097  | 0.907964 | -0.000            |
| 2      | 'Based'  | -2.722  | 0.065773 | -0.000            |
| 3      | 'Sp'     | -5.597  | 0.003711 | -0.000            |
| 4      | 'Most'   | -5.597  | 0.003711 | -0.000            |
| 5      | 'To'     | -5.722  | 0.003275 | -0.000            |
| 6      | 'An'     | -5.972  | 0.002550 | +0.125            |
| 7      | '**'     | -6.222  | 0.001986 | -0.000            |
| 8      | 'Anim'   | -6.972  | 0.000938 | -0.000            |
| 9      | 'There'  | -7.097  | 0.000828 | -0.000            |
| 10     | 'Animal' | -7.097  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
