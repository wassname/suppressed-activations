---
condition_id: "014_layer_combo_L=26_positions=4_C=4"
axis: "layer_combo"
value: "L=26,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.3125
valid_answer_mass: 0.0004483074299059808
p4: 1.1797989145634347e-06
p8: 0.00044712761882692575
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/014_layer_combo_L=26_positions=4_C=4/run.md"
---

# 014_layer_combo_L=26_positions=4_C=4

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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' spinning', ' spin', ' spins', '在校园', ' måde', '纺', '-spin', 'Spin']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `014_layer_combo_L=26_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.088  | 0.916066 | +0.008            |
| 2      | 'Based'  | -2.838  | 0.058562 | -0.117            |
| 3      | 'Most'   | -5.463  | 0.004242 | +0.133            |
| 4      | 'To'     | -5.588  | 0.003744 | +0.133            |
| 5      | 'Sp'     | -6.088  | 0.002271 | -0.492            |
| 6      | 'An'     | -6.088  | 0.002271 | +0.008            |
| 7      | '**'     | -6.088  | 0.002271 | +0.133            |
| 8      | 'There'  | -7.088  | 0.000835 | +0.008            |
| 9      | 'First'  | -7.213  | 0.000737 | +0.008            |
| 10     | 'Animal' | -7.213  | 0.000737 | -0.117            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
