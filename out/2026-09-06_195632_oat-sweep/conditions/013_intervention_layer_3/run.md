---
condition_id: "013_intervention_layer_3"
axis: "intervention_layer"
value: "3"
is_default: false
swap_log_odds_shift: 3.875
valid_answer_mass: 0.0002861908287741244
p4: 2.43545655393973e-05
p8: 0.00026183624868281186
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/013_intervention_layer_3/run.md"
---

# 013_intervention_layer_3

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
  "intervention_layer": 3,
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
['web', '-web', '盐酸', '闸蟹', '在校园', 'edata', 'Integrated', 'mmm']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**.

**Answer:**
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.060  | 0.941490 | +0.036            |
| 2      | 'Based'  | -3.310  | 0.036506 | -0.589            |
| 3      | '**'     | -5.560  | 0.003848 | +0.661            |
| 4      | 'To'     | -5.685  | 0.003396 | +0.036            |
| 5      | 'An'     | -6.060  | 0.002334 | +0.036            |
| 6      | 'First'  | -6.185  | 0.002060 | +1.036            |
| 7      | 'Sp'     | -6.560  | 0.001415 | -0.964            |
| 8      | 'That'   | -6.810  | 0.001102 | +0.786            |
| 9      | 'Animal' | -7.310  | 0.000669 | -0.214            |
| 10     | 'There'  | -7.560  | 0.000521 | -0.464            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
