---
condition_id: "025_layer_combo_L=23_24_25_26_positions=1_C=2"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=2"
is_default: false
swap_log_odds_shift: 3.125
valid_answer_mass: 0.8012588620185852
p4: 0.47487935423851013
p8: 0.3263795077800751
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/025_layer_combo_L=23_24_25_26_positions=1_C=2/run.md"
---

# 025_layer_combo_L=23_24_25_26_positions=1_C=2

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
['吠', '狗粮', 'สุนัข', ' cão', ' собаки', ' krém', ' Bite', ' perros']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `025_layer_combo_L=23_24_25_26_positions=1_C=2`).

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
| 1      | '4'     | -0.745  | 0.474879 | +2.130            |
| 2      | '8'     | -1.120  | 0.326380 | -0.995            |
| 3      | '6'     | -1.870  | 0.154171 | +1.755            |
| 4      | '1'     | -4.245  | 0.014340 | +0.380            |
| 5      | '2'     | -4.620  | 0.009856 | +0.380            |
| 6      | '3'     | -4.870  | 0.007676 | +0.255            |
| 7      | '5'     | -5.370  | 0.004656 | +0.255            |
| 8      | '7'     | -6.120  | 0.002199 | -0.370            |
| 9      | '0'     | -6.245  | 0.001941 | +0.255            |
| 10     | '9'     | -6.682  | 0.001253 | -0.120            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
