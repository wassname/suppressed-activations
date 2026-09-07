---
condition_id: "024_layer_combo_L=23_24_25_26_positions=1_C=1"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=1"
is_default: false
swap_log_odds_shift: 1.125
valid_answer_mass: 0.8909238576889038
p4: 0.14657165110111237
p8: 0.7443522214889526
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/024_layer_combo_L=23_24_25_26_positions=1_C=1/run.md"
---

# 024_layer_combo_L=23_24_25_26_positions=1_C=1

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
  "intervention_positions": 1,
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
['吠', ' krém', 'orderid', '狗粮', 'ปั่น', ' malaysia', ' implanta', ' Росси']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `024_layer_combo_L=23_24_25_26_positions=1_C=1`).

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
| 1      | '8'     | -0.295  | 0.744352 | -0.170            |
| 2      | '4'     | -1.920  | 0.146572 | +0.955            |
| 3      | '6'     | -2.670  | 0.069236 | +0.955            |
| 4      | '1'     | -4.295  | 0.013633 | +0.330            |
| 5      | '2'     | -4.795  | 0.008269 | +0.205            |
| 6      | '3'     | -5.045  | 0.006440 | +0.080            |
| 7      | '5'     | -5.545  | 0.003906 | +0.080            |
| 8      | '7'     | -6.045  | 0.002369 | -0.295            |
| 9      | '0'     | -6.295  | 0.001845 | +0.205            |
| 10     | '9'     | -6.545  | 0.001437 | +0.017            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
