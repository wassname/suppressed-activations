---
condition_id: "013_layer_combo_L=26_positions=4_C=2"
axis: "layer_combo"
value: "L=26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 1.5
valid_answer_mass: 0.8889420032501221
p4: 0.1979674994945526
p8: 0.6909745335578918
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/013_layer_combo_L=26_positions=4_C=2/run.md"
---

# 013_layer_combo_L=26_positions=4_C=2

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
[' Silk', 'Spider', ' spiders', '丝绸', '-web', ' WEB', 'Web', ' web']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `013_layer_combo_L=26_positions=4_C=2`).

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
| 1      | '8'     | -0.370  | 0.690975 | -0.245            |
| 2      | '4'     | -1.620  | 0.197967 | +1.255            |
| 3      | '6'     | -2.870  | 0.056719 | +0.755            |
| 4      | '1'     | -3.995  | 0.018414 | +0.630            |
| 5      | '2'     | -4.620  | 0.009856 | +0.380            |
| 6      | '3'     | -4.745  | 0.008698 | +0.380            |
| 7      | '5'     | -5.120  | 0.005978 | +0.505            |
| 8      | '7'     | -5.495  | 0.004109 | +0.255            |
| 9      | '9'     | -5.620  | 0.003626 | +0.943            |
| 10     | '0'     | -6.557  | 0.001420 | -0.057            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
