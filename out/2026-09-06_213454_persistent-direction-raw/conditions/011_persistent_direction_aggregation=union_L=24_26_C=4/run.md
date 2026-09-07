---
condition_id: "011_persistent_direction_aggregation=union_L=24_26_C=4"
axis: "persistent_direction"
value: "aggregation=union,L=24+26,C=4"
is_default: false
swap_log_odds_shift: 6.1875
valid_answer_mass: 0.6553746461868286
p4: 0.6349637508392334
p8: 0.020410874858498573
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/011_persistent_direction_aggregation=union_L=24_26_C=4/run.md"
---

# 011_persistent_direction_aggregation=union_L=24_26_C=4

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
  "strength": 4.0,
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
['狗粮', '吠', ' собак', ' perros', ' cães', ' chien', ' собаки', ' chiens']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `011_persistent_direction_aggregation=union_L=24_26_C=4`).

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
| 1      | '4'     | -0.454  | 0.634964 | +2.421            |
| 2      | '吠'     | -2.517  | 0.080727 | +20.530           |
| 3      | '1'     | -3.267  | 0.038133 | +1.358            |
| 4      | '3'     | -3.579  | 0.027898 | +1.546            |
| 5      | '0'     | -3.642  | 0.026208 | +2.858            |
| 6      | '5'     | -3.767  | 0.023129 | +1.858            |
| 7      | '8'     | -3.892  | 0.020411 | -3.767            |
| 8      | '2'     | -4.267  | 0.014028 | +0.733            |
| 9      | '7'     | -4.392  | 0.012380 | +1.358            |
| 10     | 'four'  | -4.454  | 0.011630 | +10.983           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
