---
condition_id: "023_intervention_layer_13"
axis: "intervention_layer"
value: "13"
is_default: false
swap_log_odds_shift: 0.9374995231628418
valid_answer_mass: 0.000639947596937418
p4: 3.1392012260766933e-06
p8: 0.0006368083995766938
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/023_intervention_layer_13/run.md"
---

# 023_intervention_layer_13

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
  "intervention_layer": 13,
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
['Spin', ' 인프라', '웹', 'seh', '丝绸', ' krém', '\tspin', '在校园']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.109  | 0.896693 | -0.013            |
| 2      | 'Based' | -2.484  | 0.083405 | +0.237            |
| 3      | 'An'    | -5.984  | 0.002519 | +0.112            |
| 4      | 'To'    | -6.109  | 0.002223 | -0.388            |
| 5      | '**'    | -6.234  | 0.001962 | -0.013            |
| 6      | 'Sp'    | -6.234  | 0.001962 | -0.638            |
| 7      | 'That'  | -6.484  | 0.001528 | +1.112            |
| 8      | 'Most'  | -6.859  | 0.001050 | -1.263            |
| 9      | 'There' | -7.234  | 0.000722 | -0.138            |
| 10     | '8'     | -7.359  | 0.000637 | +0.112            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
