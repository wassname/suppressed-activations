---
condition_id: "019_layer_combo_L=24_26_positions=1_C=8"
axis: "layer_combo"
value: "L=24+26,positions=1,C=8"
is_default: false
swap_log_odds_shift: 2.0703125
valid_answer_mass: 7.466728675353806e-07
p4: 2.511292507278995e-07
p8: 4.955435883857717e-07
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "吠"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/019_layer_combo_L=24_26_positions=1_C=8/run.md"
---

# 019_layer_combo_L=24_26_positions=1_C=8

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
  "strength": 8.0,
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
['狗粮', '吠', ' dogs', ' собак', ' Dogs', ' canine', ' cães', ' собаки']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `019_layer_combo_L=24_26_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
吠 (bèi).
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>

```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '吠'       | -2.049  | 0.128882 | +20.998           |
| 2      | '狗粮'      | -2.361  | 0.094292 | +19.979           |
| 3      | 'ow'      | -2.799  | 0.060879 | +19.105           |
| 4      | "'"       | -2.924  | 0.053726 | +17.529           |
| 5      | "'s"      | -3.361  | 0.034688 | +16.795           |
| 6      | 'web'     | -3.486  | 0.030612 | +14.170           |
| 7      | '-web'    | -4.111  | 0.016385 | +14.889           |
| 8      | ' canine' | -4.611  | 0.009938 | +15.724           |
| 9      | 'is'      | -4.861  | 0.007740 | +16.666           |
| 10     | ' -'      | -5.236  | 0.005320 | +7.826            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
