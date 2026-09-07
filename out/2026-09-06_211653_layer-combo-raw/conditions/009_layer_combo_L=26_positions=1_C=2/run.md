---
condition_id: "009_layer_combo_L=26_positions=1_C=2"
axis: "layer_combo"
value: "L=26,positions=1,C=2"
is_default: false
swap_log_odds_shift: 1.375
valid_answer_mass: 0.9004854559898376
p4: 0.18172985315322876
p8: 0.7187556028366089
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/009_layer_combo_L=26_positions=1_C=2/run.md"
---

# 009_layer_combo_L=26_positions=1_C=2

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
  "strength": 2.0,
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
[' Silk', 'Spider', '丝绸', '-web', ' spiders', ' WEB', 'Web', ' web']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `009_layer_combo_L=26_positions=1_C=2`).

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
| 1      | '8'     | -0.330  | 0.718756 | -0.205            |
| 2      | '4'     | -1.705  | 0.181730 | +1.170            |
| 3      | '6'     | -2.955  | 0.052066 | +0.670            |
| 4      | '1'     | -4.080  | 0.016904 | +0.545            |
| 5      | '2'     | -4.830  | 0.007985 | +0.170            |
| 6      | '3'     | -4.955  | 0.007046 | +0.170            |
| 7      | '5'     | -5.205  | 0.005488 | +0.420            |
| 8      | '7'     | -5.580  | 0.003772 | +0.170            |
| 9      | '9'     | -5.830  | 0.002937 | +0.732            |
| 10     | '0'     | -6.643  | 0.001303 | -0.143            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
