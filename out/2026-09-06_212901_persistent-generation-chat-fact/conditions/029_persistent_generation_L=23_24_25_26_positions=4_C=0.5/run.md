---
condition_id: "029_persistent_generation_L=23_24_25_26_positions=4_C=0.5"
axis: "persistent_generation"
value: "L=23+24+25+26,positions=4,C=0.5"
is_default: false
swap_log_odds_shift: -4.76837158203125e-07
valid_answer_mass: 0.0005706600495614111
p4: 1.0995099728461355e-06
p8: 0.0005695605650544167
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/029_persistent_generation_L=23_24_25_26_positions=4_C=0.5/run.md"
---

# 029_persistent_generation_L=23_24_25_26_positions=4_C=0.5

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
['Integrated', ' Ủy', ' krém', '丝绸', ' факта', '웹', 'seh', '盐酸']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 21.20513916015625,
    "perturbation_norm": 0.8325330018997192,
    "relative_perturbation_by_position": [
      0.03926090896129608
    ]
  },
  "24": {
    "residual_norm": 24.374433517456055,
    "perturbation_norm": 0.6232958436012268,
    "relative_perturbation_by_position": [
      0.025571705773472786
    ]
  },
  "25": {
    "residual_norm": 27.67422103881836,
    "perturbation_norm": 0.6023350954055786,
    "relative_perturbation_by_position": [
      0.021765204146504402
    ]
  },
  "26": {
    "residual_norm": 30.528257369995117,
    "perturbation_norm": 0.4957260191440582,
    "relative_perturbation_by_position": [
      0.016238268464803696
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
| 1      | 'The'    | -0.096  | 0.908786 | +0.000            |
| 2      | 'Based'  | -2.721  | 0.065832 | +0.000            |
| 3      | 'Most'   | -5.596  | 0.003714 | +0.000            |
| 4      | 'Sp'     | -5.721  | 0.003278 | -0.125            |
| 5      | 'To'     | -5.721  | 0.003278 | +0.000            |
| 6      | 'An'     | -6.096  | 0.002253 | +0.000            |
| 7      | '**'     | -6.221  | 0.001988 | +0.000            |
| 8      | 'Animal' | -7.096  | 0.000829 | +0.000            |
| 9      | 'Anim'   | -7.096  | 0.000829 | -0.125            |
| 10     | 'There'  | -7.096  | 0.000829 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
