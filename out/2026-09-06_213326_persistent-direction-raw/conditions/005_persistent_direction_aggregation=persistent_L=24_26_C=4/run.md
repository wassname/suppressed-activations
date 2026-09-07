---
condition_id: "005_persistent_direction_aggregation=persistent_L=24_26_C=4"
axis: "persistent_direction"
value: "aggregation=persistent,L=24+26,C=4"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.898863673210144
p4: 0.07649244368076324
p8: 0.822371244430542
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/005_persistent_direction_aggregation=persistent_L=24_26_C=4/run.md"
---

# 005_persistent_direction_aggregation=persistent_L=24_26_C=4

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
['TimeZone', 'ekre', ' Спа', ' måde', '페', ' Страна', 'PBS', 'izzatore']
```

Unmodified donor readout:

```python
[' Quantidade', '_approval', ' Emas', 'dach', '民政部门', '.dispatchEvent', ' Московская', '砚']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `005_persistent_direction_aggregation=persistent_L=24_26_C=4`).

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
| 1      | '8'     | -0.196  | 0.822371 | -0.071            |
| 2      | '4'     | -2.571  | 0.076492 | +0.304            |
| 3      | '6'     | -3.446  | 0.031887 | +0.179            |
| 4      | '1'     | -3.571  | 0.028140 | +1.054            |
| 5      | '2'     | -3.821  | 0.021915 | +1.179            |
| 6      | '7'     | -5.321  | 0.004890 | +0.429            |
| 7      | '5'     | -5.446  | 0.004315 | +0.179            |
| 8      | '3'     | -5.446  | 0.004315 | -0.321            |
| 9      | '0'     | -6.071  | 0.002310 | +0.429            |
| 10     | '9'     | -6.571  | 0.001401 | -0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
