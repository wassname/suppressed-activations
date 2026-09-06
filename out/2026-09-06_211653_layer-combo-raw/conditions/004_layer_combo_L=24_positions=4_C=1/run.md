---
condition_id: "004_layer_combo_L=24_positions=4_C=1"
axis: "layer_combo"
value: "L=24,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.875
valid_answer_mass: 0.9363787770271301
p4: 0.12450488656759262
p8: 0.8118739128112793
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/004_layer_combo_L=24_positions=4_C=1/run.md"
---

# 004_layer_combo_L=24_positions=4_C=1

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
['吠', '狗粮', 'orderid', ' krém', ' Росси', 'cpf', ' Bite', 'HeadersHeightSizeMode']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 50.820335388183594,
    "perturbation_norm": 8.192418098449707,
    "relative_perturbation_by_position": [
      0.1518785059452057,
      0.1605886071920395,
      0.10024940222501755,
      0.22140644490718842
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:


```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.208  | 0.811874 | -0.083            |
| 2      | '4'     | -2.083  | 0.124505 | +0.792            |
| 3      | '6'     | -3.583  | 0.027781 | +0.042            |
| 4      | '1'     | -4.458  | 0.011581 | +0.167            |
| 5      | '2'     | -4.833  | 0.007959 | +0.167            |
| 6      | '3'     | -5.208  | 0.005470 | -0.083            |
| 7      | '5'     | -5.833  | 0.002928 | -0.208            |
| 8      | '0'     | -5.958  | 0.002584 | +0.542            |
| 9      | '7'     | -6.208  | 0.002012 | -0.458            |
| 10     | '9'     | -6.521  | 0.001472 | +0.042            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
