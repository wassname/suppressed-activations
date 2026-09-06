---
condition_id: "001_layer_combo_L=24_positions=1_C=2"
axis: "layer_combo"
value: "L=24,positions=1,C=2"
is_default: false
swap_log_odds_shift: 2.75
valid_answer_mass: 0.8990170359611511
p4: 0.44950851798057556
p8: 0.44950851798057556
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/001_layer_combo_L=24_positions=1_C=2/run.md"
---

# 001_layer_combo_L=24_positions=1_C=2

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
  "intervention_positions": 1,
  "strength": 2.0,
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
['狗粮', '吠', 'สุนัข', ' собаки', ' canine', ' собак', ' perros', ' cão']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 23.754743576049805,
    "perturbation_norm": 10.191781044006348,
    "relative_perturbation_by_position": [
      0.42904192209243774
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.800  | 0.449509 | +2.075            |
| 2      | '8'     | -0.800  | 0.449509 | -0.675            |
| 3      | '6'     | -2.925  | 0.053686 | +0.700            |
| 4      | '1'     | -4.175  | 0.015381 | +0.450            |
| 5      | '2'     | -4.425  | 0.011979 | +0.575            |
| 6      | '3'     | -5.050  | 0.006412 | +0.075            |
| 7      | '0'     | -5.175  | 0.005658 | +1.325            |
| 8      | '5'     | -5.925  | 0.002673 | -0.300            |
| 9      | '7'     | -6.300  | 0.001837 | -0.550            |
| 10     | '9'     | -6.550  | 0.001431 | +0.013            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
