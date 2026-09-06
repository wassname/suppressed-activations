---
condition_id: "004_persistent_direction_aggregation=persistent_L=24_26_C=2"
axis: "persistent_direction"
value: "aggregation=persistent,L=24+26,C=2"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.9393118023872375
p4: 0.039533503353595734
p8: 0.8997783064842224
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/004_persistent_direction_aggregation=persistent_L=24_26_C=2/run.md"
---

# 004_persistent_direction_aggregation=persistent_L=24_26_C=2

Resolved config:

```json
{
  "aggregation": "persistent",
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
  "intervention_positions": 1,
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": false
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
['edata', 'TimeZone', 'ekre', ' Спа', ' måde', ' Страна', 'PBS', 'izzatore']
```

Unmodified donor readout:

```python
[' Quantidade', '_approval', ' Emas', 'dach', '民政部门', '.dispatchEvent', ' Московская', '砚']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 23.754743576049805,
    "perturbation_norm": 3.8006861209869385,
    "relative_perturbation_by_position": [
      0.15999692678451538
    ]
  },
  "26": {
    "residual_norm": 25.31561279296875,
    "perturbation_norm": 3.2477147579193115,
    "relative_perturbation_by_position": [
      0.12828899919986725
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.106  | 0.899778 | +0.019            |
| 2      | '4'     | -3.231  | 0.039534 | -0.356            |
| 3      | '6'     | -3.481  | 0.030789 | +0.144            |
| 4      | '1'     | -4.731  | 0.008821 | -0.106            |
| 5      | '2'     | -5.106  | 0.006063 | -0.106            |
| 6      | '3'     | -5.481  | 0.004167 | -0.356            |
| 7      | '7'     | -5.731  | 0.003245 | +0.019            |
| 8      | '5'     | -5.856  | 0.002864 | -0.231            |
| 9      | '0'     | -6.606  | 0.001353 | -0.106            |
| 10     | '9'     | -6.606  | 0.001353 | -0.043            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
