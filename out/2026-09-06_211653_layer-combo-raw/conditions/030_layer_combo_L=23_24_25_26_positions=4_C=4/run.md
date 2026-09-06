---
condition_id: "030_layer_combo_L=23_24_25_26_positions=4_C=4"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=4"
is_default: false
swap_log_odds_shift: 5.84375
valid_answer_mass: 0.00015525936032645404
p4: 0.00014852640742901713
p8: 6.732945621479303e-06
repeated_bigram_fraction: 0.967741935483871
generation_tokens: 32
first_token: "吠"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.375
log: "conditions/030_layer_combo_L=23_24_25_26_positions=4_C=4/run.md"
---

# 030_layer_combo_L=23_24_25_26_positions=4_C=4

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
'Fact: The number of legs on the animal that spins webs is '
```

Donor input (`repr`):

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Readout after intervention:

```python
[' dogs', '狗粮', ' puppies', '吠', ' Dogs', ' chien', '犬', 'Dog']
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
    "perturbation_norm": 17.400144577026367,
    "relative_perturbation_by_position": [
      0.33616527915000916,
      0.4109897017478943,
      0.27818426489830017,
      0.44982123374938965
    ]
  },
  "24": {
    "residual_norm": 48.023616790771484,
    "perturbation_norm": 31.253128051757812,
    "relative_perturbation_by_position": [
      0.573226273059845,
      0.7551277875900269,
      0.5504599809646606,
      0.706234335899353
    ]
  },
  "25": {
    "residual_norm": 60.468910217285156,
    "perturbation_norm": 48.23982238769531,
    "relative_perturbation_by_position": [
      0.8453864455223083,
      0.8489305377006531,
      0.7835876941680908,
      0.7131361365318298
    ]
  },
  "26": {
    "residual_norm": 63.034210205078125,
    "perturbation_norm": 55.53894805908203,
    "relative_perturbation_by_position": [
      0.9214386940002441,
      0.8869239091873169,
      0.8742741346359253,
      0.8493538498878479
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '吠'       | -0.065  | 0.937304 | +22.982           |
| 2      | 'web'     | -3.502  | 0.030130 | +14.154           |
| 3      | ' canine' | -5.065  | 0.006316 | +15.271           |
| 4      | '狗粮'      | -5.752  | 0.003176 | +16.588           |
| 5      | 'can'     | -7.065  | 0.000855 | +16.662           |
| 6      | '�'       | -7.502  | 0.000552 | +2.935            |
| 7      | ' '       | -7.502  | 0.000552 | -0.502            |
| 8      | '\t'      | -7.752  | 0.000430 | +4.310            |
| 9      | ' web'    | -8.002  | 0.000335 | +6.123            |
| 10     | ' can'    | -8.065  | 0.000314 | +8.279            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
