---
condition_id: "003_persistent_direction_aggregation=persistent_L=24_26_C=1"
axis: "persistent_direction"
value: "aggregation=persistent,L=24+26,C=1"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9457740187644958
p4: 0.050507478415966034
p8: 0.8952665328979492
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/003_persistent_direction_aggregation=persistent_L=24_26_C=1/run.md"
---

# 003_persistent_direction_aggregation=persistent_L=24_26_C=1

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
  "strength": 1.0,
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
['ปั่น', 'edata', '的战', ' måde', ' 장치', 'Attack', '高中阶段', ' Спа']
```

Unmodified donor readout:

```python
[' doga', ' patologie', ' verlassen', ' Emas', ' Quantidade', '_approval', ' Unik', ' врач']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `003_persistent_direction_aggregation=persistent_L=24_26_C=1`).

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.111  | 0.895267 | +0.014            |
| 2      | '4'     | -2.986  | 0.050507 | -0.111            |
| 3      | '6'     | -3.736  | 0.023858 | -0.111            |
| 4      | '1'     | -4.736  | 0.008777 | -0.111            |
| 5      | '2'     | -5.236  | 0.005323 | -0.236            |
| 6      | '3'     | -5.236  | 0.005323 | -0.111            |
| 7      | '5'     | -5.736  | 0.003229 | -0.111            |
| 8      | '7'     | -5.861  | 0.002849 | -0.111            |
| 9      | '0'     | -6.486  | 0.001525 | +0.014            |
| 10     | '9'     | -6.736  | 0.001188 | -0.173            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
