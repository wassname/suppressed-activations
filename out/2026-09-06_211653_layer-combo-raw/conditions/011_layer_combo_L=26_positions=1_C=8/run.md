---
condition_id: "011_layer_combo_L=26_positions=1_C=8"
axis: "layer_combo"
value: "L=26,positions=1,C=8"
is_default: false
swap_log_odds_shift: 4.375
valid_answer_mass: 0.4238646626472473
p4: 0.3541319668292999
p8: 0.06973271071910858
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/011_layer_combo_L=26_positions=1_C=8/run.md"
---

# 011_layer_combo_L=26_positions=1_C=8

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
[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `011_layer_combo_L=26_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -1.038  | 0.354132 | +1.837            |
| 2      | '6'     | -1.663  | 0.189553 | +1.962            |
| 3      | '9'     | -2.288  | 0.101461 | +4.274            |
| 4      | '1'     | -2.413  | 0.089539 | +2.212            |
| 5      | '5'     | -2.663  | 0.069733 | +2.962            |
| 6      | '8'     | -2.663  | 0.069733 | -2.538            |
| 7      | '7'     | -3.163  | 0.042295 | +2.587            |
| 8      | '3'     | -3.163  | 0.042295 | +1.962            |
| 9      | '2'     | -3.288  | 0.037325 | +1.712            |
| 10     | '0'     | -5.788  | 0.003064 | +0.712            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
