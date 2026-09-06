---
condition_id: "015_layer_combo_L=26_positions=4_C=8"
axis: "layer_combo"
value: "L=26,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.00039600429590791464
p4: 9.791693855731864e-07
p8: 0.0003950251266360283
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/015_layer_combo_L=26_positions=4_C=8/run.md"
---

# 015_layer_combo_L=26_positions=4_C=8

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
[' spinning', 'web', '蜘蛛', '-web', ' spin', ' spiders', ' måde', ' spins']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

```json
{
  "26": {
    "residual_norm": 57.94782638549805,
    "perturbation_norm": 49.868167877197266,
    "relative_perturbation_by_position": [
      1.0423142910003662,
      0.8980230093002319,
      0.758385956287384,
      0.6438788175582886
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.087  | 0.917079 | +0.010            |
| 2      | 'Based'  | -2.837  | 0.058627 | -0.115            |
| 3      | 'Most'   | -5.462  | 0.004247 | +0.135            |
| 4      | 'To'     | -5.587  | 0.003748 | +0.135            |
| 5      | 'An'     | -5.962  | 0.002576 | +0.135            |
| 6      | '**'     | -6.087  | 0.002273 | +0.135            |
| 7      | 'Sp'     | -6.462  | 0.001562 | -0.865            |
| 8      | 'There'  | -7.087  | 0.000836 | +0.010            |
| 9      | 'First'  | -7.212  | 0.000738 | +0.010            |
| 10     | 'Animal' | -7.212  | 0.000738 | -0.115            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
