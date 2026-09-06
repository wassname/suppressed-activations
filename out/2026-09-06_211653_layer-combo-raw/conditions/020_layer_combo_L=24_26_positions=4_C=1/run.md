---
condition_id: "020_layer_combo_L=24_26_positions=4_C=1"
axis: "layer_combo"
value: "L=24+26,positions=4,C=1"
is_default: false
swap_log_odds_shift: 1.25
valid_answer_mass: 0.9286894798278809
p4: 0.1694166660308838
p8: 0.7592728137969971
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/020_layer_combo_L=24_26_positions=4_C=1/run.md"
---

# 020_layer_combo_L=24_26_positions=4_C=1

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
['吠', '狗粮', 'orderid', ' krém', ' Росси', 'cpf', '_DM', ' Bite']
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
  },
  "26": {
    "residual_norm": 57.07354736328125,
    "perturbation_norm": 3.641284465789795,
    "relative_perturbation_by_position": [
      0.10102357715368271,
      0.051424626260995865,
      0.028902767226099968,
      0.059582918882369995
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
| 1      | '8'     | -0.275  | 0.759273 | -0.150            |
| 2      | '4'     | -1.775  | 0.169417 | +1.100            |
| 3      | '6'     | -3.400  | 0.033360 | +0.225            |
| 4      | '1'     | -4.400  | 0.012273 | +0.225            |
| 5      | '2'     | -4.775  | 0.008435 | +0.225            |
| 6      | '3'     | -5.150  | 0.005797 | -0.025            |
| 7      | '5'     | -5.775  | 0.003103 | -0.150            |
| 8      | '0'     | -6.025  | 0.002417 | +0.475            |
| 9      | '7'     | -6.025  | 0.002417 | -0.275            |
| 10     | '9'     | -6.463  | 0.001560 | +0.100            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
