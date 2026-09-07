---
condition_id: "002_persistent_direction_aggregation=persistent_L=24_C=4"
axis: "persistent_direction"
value: "aggregation=persistent,L=24,C=4"
is_default: false
swap_log_odds_shift: -0.75
valid_answer_mass: 0.8013349175453186
p4: 0.023488910868763924
p8: 0.7778459787368774
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/002_persistent_direction_aggregation=persistent_L=24_C=4/run.md"
---

# 002_persistent_direction_aggregation=persistent_L=24_C=4

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

[Full diagnostic data](../../result.json) (`rows` → `002_persistent_direction_aggregation=persistent_L=24_C=4`).

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
| 1      | '8'     | -0.251  | 0.777846 | -0.126            |
| 2      | '6'     | -1.751  | 0.173561 | +1.874            |
| 3      | '4'     | -3.751  | 0.023489 | -0.876            |
| 4      | '1'     | -4.876  | 0.007626 | -0.251            |
| 5      | '2'     | -5.376  | 0.004625 | -0.376            |
| 6      | '3'     | -5.501  | 0.004082 | -0.376            |
| 7      | '7'     | -6.001  | 0.002476 | -0.251            |
| 8      | '5'     | -6.251  | 0.001928 | -0.626            |
| 9      | '0'     | -6.689  | 0.001245 | -0.189            |
| 10     | '9'     | -6.939  | 0.000970 | -0.376            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
