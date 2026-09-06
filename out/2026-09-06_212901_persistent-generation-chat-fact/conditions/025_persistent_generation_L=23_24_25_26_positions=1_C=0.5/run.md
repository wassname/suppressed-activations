---
condition_id: "025_persistent_generation_L=23_24_25_26_positions=1_C=0.5"
axis: "persistent_generation"
value: "L=23+24+25+26,positions=1,C=0.5"
is_default: false
swap_log_odds_shift: -4.76837158203125e-07
valid_answer_mass: 0.0005702346097677946
p4: 1.0986904044330004e-06
p8: 0.0005691359401680529
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/025_persistent_generation_L=23_24_25_26_positions=1_C=0.5/run.md"
---

# 025_persistent_generation_L=23_24_25_26_positions=1_C=0.5

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
['-spin', 'Spin', 'seh', 'ปั่น', '盐酸', 'spin', ' 인프라', ' Presents']
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
    "residual_norm": 24.374290466308594,
    "perturbation_norm": 0.6241798400878906,
    "relative_perturbation_by_position": [
      0.02560812421143055
    ]
  },
  "25": {
    "residual_norm": 27.68360710144043,
    "perturbation_norm": 0.6042271852493286,
    "relative_perturbation_by_position": [
      0.02182617224752903
    ]
  },
  "26": {
    "residual_norm": 30.541234970092773,
    "perturbation_norm": 0.4986972212791443,
    "relative_perturbation_by_position": [
      0.016328653320670128
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
| 1      | 'The'    | -0.096  | 0.908109 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065783 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003711 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003711 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003275 | -0.000            |
| 6      | 'An'     | -5.971  | 0.002551 | +0.125            |
| 7      | '**'     | -6.221  | 0.001986 | -0.000            |
| 8      | 'Animal' | -7.096  | 0.000828 | -0.000            |
| 9      | 'Anim'   | -7.096  | 0.000828 | -0.125            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
