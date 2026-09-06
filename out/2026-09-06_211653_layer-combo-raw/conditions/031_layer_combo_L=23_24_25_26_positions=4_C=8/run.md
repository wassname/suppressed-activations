---
condition_id: "031_layer_combo_L=23_24_25_26_positions=4_C=8"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=8"
is_default: false
swap_log_odds_shift: 3.703125
valid_answer_mass: 7.475934538092588e-09
p4: 5.395705215960334e-09
p8: 2.080229766221464e-09
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "web"
first_answer: "8"
source_fact_preserved: false
readout_overlap: 0.375
log: "conditions/031_layer_combo_L=23_24_25_26_positions=4_C=8/run.md"
---

# 031_layer_combo_L=23_24_25_26_positions=4_C=8

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
'Fact: The number of legs on the animal that spins webs is '
```

Donor input (`repr`):

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Readout after intervention:

```python
['吠', ' dogs', '狗粮', ' canine', '犬', ' собак', ' Dogs', ' puppies']
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
    "perturbation_norm": 30.637500762939453,
    "relative_perturbation_by_position": [
      0.6105213165283203,
      0.716943621635437,
      0.5160207152366638,
      0.7633763551712036
    ]
  },
  "24": {
    "residual_norm": 46.786685943603516,
    "perturbation_norm": 55.783363342285156,
    "relative_perturbation_by_position": [
      1.1919139623641968,
      1.234997034072876,
      1.135701298713684,
      1.2106937170028687
    ]
  },
  "25": {
    "residual_norm": 66.13949584960938,
    "perturbation_norm": 73.78640747070312,
    "relative_perturbation_by_position": [
      1.115677833557129,
      1.1361240148544312,
      1.1301167011260986,
      1.076738715171814
    ]
  },
  "26": {
    "residual_norm": 74.16602325439453,
    "perturbation_norm": 87.46293640136719,
    "relative_perturbation_by_position": [
      1.1919969320297241,
      1.1765844821929932,
      1.182441234588623,
      1.1666319370269775
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
web.
Hypothesis: The animal that makes webs has 8 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'web'     | -0.655  | 0.519520 | +17.001           |
| 2      | '吠'       | -0.905  | 0.404602 | +22.142           |
| 3      | '狗粮'      | -3.467  | 0.031200 | +18.873           |
| 4      | '丝绸'      | -4.280  | 0.013845 | +13.845           |
| 5      | ' canine' | -4.967  | 0.006962 | +15.369           |
| 6      | ' web'    | -6.842  | 0.001068 | +7.283            |
| 7      | 'dog'     | -7.467  | 0.000571 | +13.786           |
| 8      | '{'       | -7.842  | 0.000393 | +11.939           |
| 9      | '_{'      | -7.967  | 0.000347 | +8.439            |
| 10     | '{\\'     | -8.092  | 0.000306 | +10.392           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
