---
condition_id: "023_layer_combo_L=24_26_positions=4_C=8"
axis: "layer_combo"
value: "L=24+26,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.2500004768371582
valid_answer_mass: 0.0004451338027138263
p4: 6.682266757707112e-07
p8: 0.0004444655787665397
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.5
log: "conditions/023_layer_combo_L=24_26_positions=4_C=8/run.md"
---

# 023_layer_combo_L=24_26_positions=4_C=8

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
['狗粮', 'seh', 'สุนัข', ' собак', '狗', ' собаки', 'DOG', '狗的']
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
    "perturbation_norm": 37.39054870605469,
    "relative_perturbation_by_position": [
      0.9313962459564209,
      0.785031795501709,
      0.5134852528572083,
      0.5948556661605835
    ]
  },
  "26": {
    "residual_norm": 54.76191329956055,
    "perturbation_norm": 64.38831329345703,
    "relative_perturbation_by_position": [
      1.2417385578155518,
      1.2288323640823364,
      1.0774331092834473,
      1.1503815650939941
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The animal that is famous for spinning webs is the **spider**.

Spiders are arachnids, which means they have **eight** legs.
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.094  | 0.910612 | +0.002            |
| 2      | 'Based'  | -2.719  | 0.065965 | +0.002            |
| 3      | 'Most'   | -5.594  | 0.003721 | +0.002            |
| 4      | 'To'     | -5.719  | 0.003284 | +0.002            |
| 5      | 'An'     | -5.844  | 0.002898 | +0.252            |
| 6      | '**'     | -6.219  | 0.001992 | +0.002            |
| 7      | 'Sp'     | -6.469  | 0.001551 | -0.873            |
| 8      | 'There'  | -7.219  | 0.000733 | -0.123            |
| 9      | 'First'  | -7.219  | 0.000733 | +0.002            |
| 10     | 'Animal' | -7.344  | 0.000647 | -0.248            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
