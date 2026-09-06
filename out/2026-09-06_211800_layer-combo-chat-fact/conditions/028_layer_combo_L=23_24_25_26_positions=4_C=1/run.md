---
condition_id: "028_layer_combo_L=23_24_25_26_positions=4_C=1"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=1"
is_default: false
swap_log_odds_shift: -0.0625
valid_answer_mass: 0.000570646021515131
p4: 1.0329896440453012e-06
p8: 0.0005696130101568997
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/028_layer_combo_L=23_24_25_26_positions=4_C=1/run.md"
---

# 028_layer_combo_L=23_24_25_26_positions=4_C=1

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
  "strength": 1.0,
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
[' krém', 'Integrated', ' Ủy', '\')."', '丝绸', 'edata', '웹', '和金']
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
    "perturbation_norm": 4.420228481292725,
    "relative_perturbation_by_position": [
      0.12641239166259766,
      0.09157072007656097,
      0.04990703612565994,
      0.07629377394914627
    ]
  },
  "24": {
    "residual_norm": 50.884456634521484,
    "perturbation_norm": 2.792349338531494,
    "relative_perturbation_by_position": [
      0.051585569977760315,
      0.05160406231880188,
      0.05873917415738106,
      0.057781293988227844
    ]
  },
  "25": {
    "residual_norm": 54.27627182006836,
    "perturbation_norm": 3.2229325771331787,
    "relative_perturbation_by_position": [
      0.07748448103666306,
      0.055528171360492706,
      0.04637177661061287,
      0.052338868379592896
    ]
  },
  "26": {
    "residual_norm": 56.89807891845703,
    "perturbation_norm": 1.1773109436035156,
    "relative_perturbation_by_position": [
      0.013557194732129574,
      0.019668349996209145,
      0.028049200773239136,
      0.018224500119686127
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
| 1      | 'The'   | -0.096  | 0.908870 | +0.001            |
| 2      | 'Based' | -2.721  | 0.065838 | +0.001            |
| 3      | 'Most'  | -5.596  | 0.003714 | +0.001            |
| 4      | 'To'    | -5.721  | 0.003278 | +0.001            |
| 5      | 'Sp'    | -5.721  | 0.003278 | -0.124            |
| 6      | 'An'    | -6.096  | 0.002253 | +0.001            |
| 7      | '**'    | -6.221  | 0.001988 | +0.001            |
| 8      | 'There' | -7.096  | 0.000829 | +0.001            |
| 9      | 'Anim'  | -7.096  | 0.000829 | -0.124            |
| 10     | 'First' | -7.221  | 0.000731 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
