---
condition_id: "016_intervention_layer_6"
axis: "intervention_layer"
value: "6"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.0010549428407102823
p4: 2.3026407234283397e-06
p8: 0.0010526401456445456
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/016_intervention_layer_6/run.md"
---

# 016_intervention_layer_6

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
  "intervention_layer": 6,
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
['丝绸', 'web', 'edata', '웹', ' факта', '在校园', ' 인프라', '盐酸']
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
| 1      | 'The'   | -0.106  | 0.899016 | -0.010            |
| 2      | 'Based' | -2.606  | 0.073796 | +0.115            |
| 3      | 'An'    | -5.481  | 0.004163 | +0.615            |
| 4      | 'To'    | -5.731  | 0.003242 | -0.010            |
| 5      | 'Sp'    | -5.856  | 0.002861 | -0.260            |
| 6      | '**'    | -5.981  | 0.002525 | +0.240            |
| 7      | 'There' | -6.356  | 0.001736 | +0.740            |
| 8      | 'First' | -6.731  | 0.001193 | +0.490            |
| 9      | '8'     | -6.856  | 0.001053 | +0.615            |
| 10     | 'That'  | -6.981  | 0.000929 | +0.615            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
