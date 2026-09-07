---
condition_id: "008_layer_combo_L=26_positions=1_C=1"
axis: "layer_combo"
value: "L=26,positions=1,C=1"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.9256719946861267
p4: 0.09876050055027008
p8: 0.8269115090370178
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/008_layer_combo_L=26_positions=1_C=1/run.md"
---

# 008_layer_combo_L=26_positions=1_C=1

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
  "intervention_positions": 1,
  "strength": 1.0,
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
['Spider', '丝绸', '-web', ' WEB', 'Web', 'Disc', ' Silk', '的战']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `008_layer_combo_L=26_positions=1_C=1`).

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
| 1      | '8'     | -0.190  | 0.826912 | -0.065            |
| 2      | '4'     | -2.315  | 0.098761 | +0.560            |
| 3      | '6'     | -3.315  | 0.036332 | +0.310            |
| 4      | '1'     | -4.440  | 0.011795 | +0.185            |
| 5      | '2'     | -4.940  | 0.007154 | +0.060            |
| 6      | '3'     | -5.065  | 0.006314 | +0.060            |
| 7      | '5'     | -5.440  | 0.004339 | +0.185            |
| 8      | '7'     | -5.815  | 0.002982 | -0.065            |
| 9      | '9'     | -6.253  | 0.001926 | +0.310            |
| 10     | '0'     | -6.565  | 0.001409 | -0.065            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
