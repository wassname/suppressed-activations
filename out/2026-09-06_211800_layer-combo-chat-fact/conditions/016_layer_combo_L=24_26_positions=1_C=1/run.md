---
condition_id: "016_layer_combo_L=24_26_positions=1_C=1"
axis: "layer_combo"
value: "L=24+26,positions=1,C=1"
is_default: false
swap_log_odds_shift: -0.0624995231628418
valid_answer_mass: 0.0005702762864530087
p4: 1.0323209380658227e-06
p8: 0.0005692439735867083
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/016_layer_combo_L=24_26_positions=1_C=1/run.md"
---

# 016_layer_combo_L=24_26_positions=1_C=1

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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['-spin', 'Spin', 'seh', 'ปั่น', '盐酸', 'spin', ' 인프라', ' Presents']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `016_layer_combo_L=24_26_positions=1_C=1`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908281 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065796 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003712 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003712 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003276 | -0.000            |
| 6      | 'An'     | -6.096  | 0.002251 | -0.000            |
| 7      | '**'     | -6.221  | 0.001987 | -0.000            |
| 8      | 'Anim'   | -6.971  | 0.000939 | -0.000            |
| 9      | 'There'  | -7.096  | 0.000828 | -0.000            |
| 10     | 'Animal' | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
