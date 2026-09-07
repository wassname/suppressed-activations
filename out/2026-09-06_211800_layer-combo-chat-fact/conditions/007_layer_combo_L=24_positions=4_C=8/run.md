---
condition_id: "007_layer_combo_L=24_positions=4_C=8"
axis: "layer_combo"
value: "L=24,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.0006456720293499529
p4: 1.098109009944892e-06
p8: 0.0006445739418268204
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/007_layer_combo_L=24_positions=4_C=8/run.md"
---

# 007_layer_combo_L=24_positions=4_C=8

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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['狗粮', 'สุนัข', ' собак', ' собаки', 'DOG', 'Dog', ' собака', 'seh']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `007_layer_combo_L=24_positions=4_C=8`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.097  | 0.907628 | -0.001            |
| 2      | 'Based'   | -2.722  | 0.065748 | -0.001            |
| 3      | 'Most'    | -5.472  | 0.004203 | +0.124            |
| 4      | 'To'      | -5.597  | 0.003709 | +0.124            |
| 5      | 'An'      | -5.972  | 0.002549 | +0.124            |
| 6      | 'Sp'      | -5.972  | 0.002549 | -0.376            |
| 7      | '**'      | -6.097  | 0.002250 | +0.124            |
| 8      | 'There'   | -7.097  | 0.000828 | -0.001            |
| 9      | 'First'   | -7.097  | 0.000828 | +0.124            |
| 10     | '<think>' | -7.222  | 0.000730 | +0.249            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
