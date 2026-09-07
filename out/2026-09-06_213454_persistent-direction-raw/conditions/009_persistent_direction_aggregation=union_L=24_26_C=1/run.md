---
condition_id: "009_persistent_direction_aggregation=union_L=24_26_C=1"
axis: "persistent_direction"
value: "aggregation=union,L=24+26,C=1"
is_default: false
swap_log_odds_shift: 1.125
valid_answer_mass: 0.932799220085144
p4: 0.1534608155488968
p8: 0.7793384194374084
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/009_persistent_direction_aggregation=union_L=24_26_C=1/run.md"
---

# 009_persistent_direction_aggregation=union_L=24_26_C=1

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
['吠', '狗粮', 'orderid', ' krém', 'cpf', ' Росси', '_DM', ' Bite']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `009_persistent_direction_aggregation=union_L=24_26_C=1`).

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
| 1      | '8'     | -0.249  | 0.779338 | -0.124            |
| 2      | '4'     | -1.874  | 0.153461 | +1.001            |
| 3      | '6'     | -3.499  | 0.030218 | +0.126            |
| 4      | '1'     | -4.374  | 0.012597 | +0.251            |
| 5      | '2'     | -4.874  | 0.007640 | +0.126            |
| 6      | '3'     | -5.124  | 0.005950 | +0.001            |
| 7      | '5'     | -5.749  | 0.003185 | -0.124            |
| 8      | '7'     | -6.124  | 0.002189 | -0.374            |
| 9      | '0'     | -6.187  | 0.002056 | +0.313            |
| 10     | '9'     | -6.499  | 0.001504 | +0.063            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
