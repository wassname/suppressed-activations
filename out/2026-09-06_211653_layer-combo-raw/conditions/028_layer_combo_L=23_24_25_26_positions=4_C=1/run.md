---
condition_id: "028_layer_combo_L=23_24_25_26_positions=4_C=1"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=1"
is_default: false
swap_log_odds_shift: 1.25
valid_answer_mass: 0.8822041749954224
p4: 0.16093656420707703
p8: 0.7212676405906677
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/028_layer_combo_L=23_24_25_26_positions=4_C=1/run.md"
---

# 028_layer_combo_L=23_24_25_26_positions=4_C=1

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
  "intervention_positions": 4,
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
['吠', ' krém', 'orderid', ' implanta', ' Росси', '狗粮', ' malaysia', 'cpf']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `028_layer_combo_L=23_24_25_26_positions=4_C=1`).

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
| 1      | '8'     | -0.327  | 0.721268 | -0.202            |
| 2      | '4'     | -1.827  | 0.160937 | +1.048            |
| 3      | '6'     | -2.577  | 0.076021 | +1.048            |
| 4      | '1'     | -4.202  | 0.014969 | +0.423            |
| 5      | '2'     | -4.702  | 0.009079 | +0.298            |
| 6      | '3'     | -5.077  | 0.006240 | +0.048            |
| 7      | '5'     | -5.577  | 0.003785 | +0.048            |
| 8      | '0'     | -6.139  | 0.002157 | +0.361            |
| 9      | '7'     | -6.139  | 0.002157 | -0.389            |
| 10     | '9'     | -6.577  | 0.001392 | -0.014            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
