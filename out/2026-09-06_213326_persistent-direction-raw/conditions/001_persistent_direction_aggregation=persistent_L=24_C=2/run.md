---
condition_id: "001_persistent_direction_aggregation=persistent_L=24_C=2"
axis: "persistent_direction"
value: "aggregation=persistent,L=24,C=2"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.9216828942298889
p4: 0.038791537284851074
p8: 0.8828913569450378
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/001_persistent_direction_aggregation=persistent_L=24_C=2/run.md"
---

# 001_persistent_direction_aggregation=persistent_L=24_C=2

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
    24
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
['edata', 'TimeZone', 'ekre', ' Спа', ' måde', ' Страна', 'PBS', 'izzatore']
```

Unmodified donor readout:

```python
[' Quantidade', '_approval', ' Emas', 'dach', '民政部门', '.dispatchEvent', ' Московская', '砚']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `001_persistent_direction_aggregation=persistent_L=24_C=2`).

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.125  | 0.882891 | +0.000            |
| 2      | '6'     | -3.000  | 0.049809 | +0.625            |
| 3      | '4'     | -3.250  | 0.038792 | -0.375            |
| 4      | '1'     | -4.750  | 0.008656 | -0.125            |
| 5      | '2'     | -5.250  | 0.005250 | -0.250            |
| 6      | '3'     | -5.375  | 0.004633 | -0.250            |
| 7      | '7'     | -5.875  | 0.002810 | -0.125            |
| 8      | '5'     | -6.000  | 0.002480 | -0.375            |
| 9      | '0'     | -6.625  | 0.001327 | -0.125            |
| 10     | '9'     | -6.750  | 0.001171 | -0.187            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
