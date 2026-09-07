---
condition_id: "029_layer_combo_L=23_24_25_26_positions=4_C=2"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 3.375
valid_answer_mass: 0.8212947249412537
p4: 0.534954309463501
p8: 0.2863404154777527
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/029_layer_combo_L=23_24_25_26_positions=4_C=2/run.md"
---

# 029_layer_combo_L=23_24_25_26_positions=4_C=2

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
['吠', '狗粮', 'สุนัข', ' cão', ' krém', ' собаки', ' perros', ' implanta']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `029_layer_combo_L=23_24_25_26_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.626  | 0.534954 | +2.249            |
| 2      | '8'     | -1.251  | 0.286340 | -1.126            |
| 3      | '6'     | -2.001  | 0.135258 | +1.624            |
| 4      | '1'     | -4.251  | 0.014256 | +0.374            |
| 5      | '2'     | -4.626  | 0.009798 | +0.374            |
| 6      | '3'     | -5.001  | 0.006734 | +0.124            |
| 7      | '5'     | -5.438  | 0.004348 | +0.187            |
| 8      | '0'     | -6.063  | 0.002327 | +0.437            |
| 9      | '7'     | -6.313  | 0.001812 | -0.563            |
| 10     | '9'     | -6.813  | 0.001099 | -0.251            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
