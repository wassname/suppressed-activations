---
condition_id: "027_layer_combo_L=23_24_25_26_positions=1_C=8"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.953125
valid_answer_mass: 2.0502126574228896e-07
p4: 2.916056374147047e-08
p8: 1.7586070555353217e-07
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "web"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/027_layer_combo_L=23_24_25_26_positions=1_C=8/run.md"
---

# 027_layer_combo_L=23_24_25_26_positions=1_C=8

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
[' dogs', '吠', ' canine', '犬', '狗粮', ' dog', ' puppies', '狗']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `027_layer_combo_L=23_24_25_26_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
web.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'web'     | -0.147  | 0.863014 | +17.509           |
| 2      | '吠'       | -3.022  | 0.048688 | +20.024           |
| 3      | '狗粮'      | -4.585  | 0.010206 | +17.756           |
| 4      | 'dog'     | -5.022  | 0.006589 | +16.232           |
| 5      | 'we'      | -5.897  | 0.002747 | +14.884           |
| 6      | ' canine' | -6.022  | 0.002424 | +14.314           |
| 7      | '丝绸'      | -6.022  | 0.002424 | +12.103           |
| 8      | 'sp'      | -6.835  | 0.001076 | +12.478           |
| 9      | 'can'     | -7.022  | 0.000892 | +16.704           |
| 10     | 'wei'     | -7.022  | 0.000892 | +15.015           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
