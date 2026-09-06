---
condition_id: "005_detector_layers_(20,_26,_32)"
axis: "detector_layers"
value: "(20, 26, 32)"
is_default: false
swap_log_odds_shift: 0.3749995231628418
valid_answer_mass: 0.0005707878735847771
p4: 1.5987344568202388e-06
p8: 0.0005691891419701278
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/005_detector_layers_(20,_26,_32)/run.md"
---

# 005_detector_layers_(20,_26,_32)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    20,
    26,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
['Sony', 'web', ' měst', 'mmm', '北京大学', '教育理念', '闸蟹', 'celli']
```

Unmodified donor readout:

```python
[' dogg', 'Dog', '狗粮', ' chiens', 'dog', ' собаки', 'DOG', ' Dog']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

Therefore, the
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908194 | -0.000            |
| 2      | 'Based'  | -2.846  | 0.058059 | -0.125            |
| 3      | 'Sp'     | -5.096  | 0.006119 | +0.500            |
| 4      | 'To'     | -5.346  | 0.004766 | +0.375            |
| 5      | 'An'     | -5.721  | 0.003275 | +0.375            |
| 6      | '**'     | -5.971  | 0.002551 | +0.250            |
| 7      | 'First'  | -5.971  | 0.002551 | +1.250            |
| 8      | 'There'  | -6.221  | 0.001987 | +0.875            |
| 9      | 'Spider' | -6.596  | 0.001365 | +1.125            |
| 10     | 'That'   | -6.971  | 0.000938 | +0.625            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
