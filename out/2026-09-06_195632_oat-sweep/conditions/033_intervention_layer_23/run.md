---
condition_id: "033_intervention_layer_23"
axis: "intervention_layer"
value: "23"
is_default: false
swap_log_odds_shift: -0.1875
valid_answer_mass: 0.0005753789446316659
p4: 9.193665277962282e-07
p8: 0.0005744595546275377
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.375
log: "conditions/033_intervention_layer_23/run.md"
---

# 033_intervention_layer_23

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
  "intervention_layer": 23,
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
['seh', '狗粮', 'สุนัข', ' собаки', 'ัข', '盐酸', '在校园', '.JSONObject']
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
| 1      | 'The'   | -0.087  | 0.916603 | +0.009            |
| 2      | 'Based' | -2.837  | 0.058596 | -0.116            |
| 3      | 'Sp'    | -5.587  | 0.003746 | +0.009            |
| 4      | 'Most'  | -5.587  | 0.003746 | +0.009            |
| 5      | 'To'    | -5.837  | 0.002917 | -0.116            |
| 6      | 'An'    | -6.087  | 0.002272 | +0.009            |
| 7      | '**'    | -6.212  | 0.002005 | +0.009            |
| 8      | 'There' | -7.087  | 0.000836 | +0.009            |
| 9      | 'Anim'  | -7.212  | 0.000738 | -0.241            |
| 10     | 'First' | -7.337  | 0.000651 | -0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
