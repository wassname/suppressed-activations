---
condition_id: "004_persistent_direction_aggregation=persistent_L=24_26_C=2"
axis: "persistent_direction"
value: "aggregation=persistent,L=24+26,C=2"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.94764244556427
p4: 0.044942766427993774
p8: 0.9026996493339539
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.125
log: "conditions/004_persistent_direction_aggregation=persistent_L=24_26_C=2/run.md"
---

# 004_persistent_direction_aggregation=persistent_L=24_26_C=2

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
['ปั่น', ' doga', 'edata', 'Attack', '高中阶段', ' 장치', '的战', ' måde']
```

Unmodified donor readout:

```python
[' doga', ' patologie', ' verlassen', ' Emas', ' Quantidade', '_approval', ' Unik', ' врач']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `004_persistent_direction_aggregation=persistent_L=24_26_C=2`).

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
| 1      | '8'     | -0.102  | 0.902700 | +0.023            |
| 2      | '4'     | -3.102  | 0.044943 | -0.227            |
| 3      | '6'     | -3.852  | 0.021229 | -0.227            |
| 4      | '1'     | -4.727  | 0.008850 | -0.102            |
| 5      | '2'     | -5.227  | 0.005368 | -0.227            |
| 6      | '3'     | -5.227  | 0.005368 | -0.102            |
| 7      | '7'     | -5.727  | 0.003256 | +0.023            |
| 8      | '5'     | -5.727  | 0.003256 | -0.102            |
| 9      | '0'     | -6.415  | 0.001637 | +0.085            |
| 10     | '9'     | -6.665  | 0.001275 | -0.102            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
