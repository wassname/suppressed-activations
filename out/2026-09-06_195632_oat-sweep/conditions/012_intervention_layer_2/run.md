---
condition_id: "012_intervention_layer_2"
axis: "intervention_layer"
value: "2"
is_default: false
swap_log_odds_shift: 0.3125
valid_answer_mass: 0.0008150821668095887
p4: 2.145030748579302e-06
p8: 0.0008129371562972665
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/012_intervention_layer_2/run.md"
---

# 012_intervention_layer_2

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
  "intervention_layer": 2,
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
['-web', 'web', 'mmm', '(web', 'WEB', '丝绸', '闸蟹', '_web']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

Therefore, the
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.115  | 0.891494 | -0.019            |
| 2      | 'Based'  | -2.615  | 0.073178 | +0.106            |
| 3      | 'To'     | -5.115  | 0.006007 | +0.606            |
| 4      | 'Sp'     | -5.115  | 0.006007 | +0.481            |
| 5      | '**'     | -5.740  | 0.003215 | +0.481            |
| 6      | 'An'     | -5.865  | 0.002837 | +0.231            |
| 7      | 'There'  | -6.115  | 0.002210 | +0.981            |
| 8      | 'First'  | -6.240  | 0.001950 | +0.981            |
| 9      | 'Spider' | -6.615  | 0.001340 | +1.106            |
| 10     | 'That'   | -6.740  | 0.001183 | +0.856            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
