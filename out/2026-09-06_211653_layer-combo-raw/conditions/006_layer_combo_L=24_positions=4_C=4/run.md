---
condition_id: "006_layer_combo_L=24_positions=4_C=4"
axis: "layer_combo"
value: "L=24,positions=4,C=4"
is_default: false
swap_log_odds_shift: 4.875
valid_answer_mass: 0.38044050335884094
p4: 0.3398510813713074
p8: 0.04058942571282387
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "6"
first_answer: null
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/006_layer_combo_L=24_positions=4_C=4/run.md"
---

# 006_layer_combo_L=24_positions=4_C=4

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
    24
  ],
  "intervention_positions": 4,
  "strength": 4.0,
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
['狗粮', '吠', ' canine', 'สุนัข', ' собаки', ' собак', '狗狗', ' perros']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `006_layer_combo_L=24_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '6'     | -0.829  | 0.436377 | +2.796            |
| 2      | '4'     | -1.079  | 0.339851 | +1.796            |
| 3      | '1'     | -2.829  | 0.059057 | +1.796            |
| 4      | '2'     | -2.954  | 0.052118 | +2.046            |
| 5      | '8'     | -3.204  | 0.040589 | -3.079            |
| 6      | '0'     | -3.329  | 0.035820 | +3.171            |
| 7      | '3'     | -4.079  | 0.016920 | +1.046            |
| 8      | '9'     | -4.954  | 0.007053 | +1.608            |
| 9      | '7'     | -5.204  | 0.005493 | +0.546            |
| 10     | '5'     | -5.329  | 0.004848 | +0.296            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
