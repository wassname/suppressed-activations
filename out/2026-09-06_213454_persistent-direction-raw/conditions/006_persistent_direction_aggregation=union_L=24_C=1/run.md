---
condition_id: "006_persistent_direction_aggregation=union_L=24_C=1"
axis: "persistent_direction"
value: "aggregation=union,L=24,C=1"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.9370534420013428
p4: 0.11169951409101486
p8: 0.8253539204597473
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/006_persistent_direction_aggregation=union_L=24_C=1/run.md"
---

# 006_persistent_direction_aggregation=union_L=24_C=1

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
  "strength": 1.0,
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
['吠', '狗粮', 'orderid', ' krém', 'cpf', ' Bite', ' Росси', 'ปั่น']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `006_persistent_direction_aggregation=union_L=24_C=1`).

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
| 1      | '8'     | -0.192  | 0.825354 | -0.067            |
| 2      | '4'     | -2.192  | 0.111700 | +0.683            |
| 3      | '6'     | -3.567  | 0.028242 | +0.058            |
| 4      | '1'     | -4.442  | 0.011773 | +0.183            |
| 5      | '2'     | -4.942  | 0.007141 | +0.058            |
| 6      | '3'     | -5.192  | 0.005561 | -0.067            |
| 7      | '5'     | -5.817  | 0.002977 | -0.192            |
| 8      | '0'     | -6.192  | 0.002046 | +0.308            |
| 9      | '7'     | -6.192  | 0.002046 | -0.442            |
| 10     | '9'     | -6.567  | 0.001406 | -0.005            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
