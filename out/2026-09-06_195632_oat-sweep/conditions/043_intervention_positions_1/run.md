---
condition_id: "043_intervention_positions_1"
axis: "intervention_positions"
value: "1"
is_default: false
swap_log_odds_shift: -0.0624995231628418
valid_answer_mass: 0.0006441292935051024
p4: 1.1660105201372062e-06
p8: 0.0006429632776416838
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/043_intervention_positions_1/run.md"
---

# 043_intervention_positions_1

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
  "intervention_layer": 1,
  "intervention_positions": 1,
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
['-spin', 'Spin', 'seh', 'ปั่น', '盐酸', 'spin', ' 인프라', ' Presents']
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.099  | 0.905360 | -0.003            |
| 2      | 'Based'  | -2.724  | 0.065584 | -0.003            |
| 3      | 'Sp'     | -5.474  | 0.004193 | +0.122            |
| 4      | 'Most'   | -5.474  | 0.004193 | +0.122            |
| 5      | 'To'     | -5.599  | 0.003700 | +0.122            |
| 6      | 'An'     | -5.974  | 0.002543 | +0.122            |
| 7      | '**'     | -6.224  | 0.001980 | -0.003            |
| 8      | 'Animal' | -6.974  | 0.000936 | +0.122            |
| 9      | 'Anim'   | -6.974  | 0.000936 | -0.003            |
| 10     | 'There'  | -6.974  | 0.000936 | +0.122            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
