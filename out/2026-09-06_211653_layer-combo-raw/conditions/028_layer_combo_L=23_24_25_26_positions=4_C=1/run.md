---
condition_id: "028_layer_combo_L=23_24_25_26_positions=4_C=1"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=1"
is_default: false
swap_log_odds_shift: 1.25
valid_answer_mass: 0.8822041749954224
p4: 0.16093656420707703
p8: 0.7212676405906677
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
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
'Fact: The number of legs on the animal that spins webs is '
```

Donor input (`repr`):

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Readout after intervention:

```python
['吠', ' krém', 'orderid', ' implanta', ' Росси', '狗粮', ' malaysia', 'cpf']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 46.644195556640625,
    "perturbation_norm": 4.542304515838623,
    "relative_perturbation_by_position": [
      0.08646321296691895,
      0.10737373679876328,
      0.07132092118263245,
      0.11941588670015335
    ]
  },
  "24": {
    "residual_norm": 50.028072357177734,
    "perturbation_norm": 4.148533344268799,
    "relative_perturbation_by_position": [
      0.07289820164442062,
      0.0686635971069336,
      0.05980178341269493,
      0.12596729397773743
    ]
  },
  "25": {
    "residual_norm": 53.68134689331055,
    "perturbation_norm": 3.496293783187866,
    "relative_perturbation_by_position": [
      0.0921650305390358,
      0.049363039433956146,
      0.035447634756565094,
      0.07700283825397491
    ]
  },
  "26": {
    "residual_norm": 56.472103118896484,
    "perturbation_norm": 1.5797343254089355,
    "relative_perturbation_by_position": [
      0.026294110342860222,
      0.022648077458143234,
      0.02158989943563938,
      0.042482633143663406
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.327  | 0.721268 | -0.202            |
| 2      | '4'     | -1.827  | 0.160937 | +1.048            |
| 3      | '6'     | -2.577  | 0.076021 | +1.048            |
| 4      | '1'     | -4.202  | 0.014969 | +0.423            |
| 5      | '2'     | -4.702  | 0.009079 | +0.298            |
| 6      | '3'     | -5.077  | 0.006240 | +0.048            |
| 7      | '5'     | -5.577  | 0.003785 | +0.048            |
| 8      | '0'     | -6.139  | 0.002157 | +0.361            |
| 9      | '7'     | -6.139  | 0.002157 | -0.389            |
| 10     | '9'     | -6.577  | 0.001392 | -0.014            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
