---
condition_id: "010_layer_combo_L=26_positions=1_C=4"
axis: "layer_combo"
value: "L=26,positions=1,C=4"
is_default: false
swap_log_odds_shift: 3.625
valid_answer_mass: 0.7358554601669312
p4: 0.5193557739257812
p8: 0.2164997011423111
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/010_layer_combo_L=26_positions=1_C=4/run.md"
---

# 010_layer_combo_L=26_positions=1_C=4

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
    26
  ],
  "intervention_positions": 1,
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
[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `010_layer_combo_L=26_positions=1_C=4`).

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
| 1      | '4'     | -0.655  | 0.519356 | +2.220            |
| 2      | '8'     | -1.530  | 0.216500 | -1.405            |
| 3      | '6'     | -1.905  | 0.148798 | +1.720            |
| 4      | '1'     | -3.280  | 0.037622 | +1.345            |
| 5      | '2'     | -4.030  | 0.017771 | +0.970            |
| 6      | '5'     | -4.155  | 0.015683 | +1.470            |
| 7      | '9'     | -4.155  | 0.015683 | +2.407            |
| 8      | '3'     | -4.155  | 0.015683 | +0.970            |
| 9      | '7'     | -4.655  | 0.009512 | +1.095            |
| 10     | '0'     | -6.405  | 0.001653 | +0.095            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
