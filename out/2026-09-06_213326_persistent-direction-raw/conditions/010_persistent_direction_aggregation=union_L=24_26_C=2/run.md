---
condition_id: "010_persistent_direction_aggregation=union_L=24_26_C=2"
axis: "persistent_direction"
value: "aggregation=union,L=24+26,C=2"
is_default: false
swap_log_odds_shift: 3.75
valid_answer_mass: 0.940337061882019
p4: 0.6874414682388306
p8: 0.2528955638408661
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/010_persistent_direction_aggregation=union_L=24_26_C=2/run.md"
---

# 010_persistent_direction_aggregation=union_L=24_26_C=2

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
['狗粮', '吠', 'สุนัข', ' собак', ' собаки', ' perros', '养犬', ' cão']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `010_persistent_direction_aggregation=union_L=24_26_C=2`).

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
| 1      | '4'     | -0.375  | 0.687441 | +2.500            |
| 2      | '8'     | -1.375  | 0.252896 | -1.250            |
| 3      | '6'     | -3.875  | 0.020759 | -0.250            |
| 4      | '1'     | -4.375  | 0.012591 | +0.250            |
| 5      | '2'     | -4.750  | 0.008654 | +0.250            |
| 6      | '3'     | -5.125  | 0.005948 | +0.000            |
| 7      | '0'     | -5.750  | 0.003183 | +0.750            |
| 8      | '5'     | -5.812  | 0.002991 | -0.187            |
| 9      | '7'     | -6.312  | 0.001814 | -0.562            |
| 10     | '9'     | -6.937  | 0.000971 | -0.375            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
