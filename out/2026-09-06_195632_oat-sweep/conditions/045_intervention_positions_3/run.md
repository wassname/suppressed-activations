---
condition_id: "045_intervention_positions_3"
axis: "intervention_positions"
value: "3"
is_default: false
swap_log_odds_shift: 0.0625
valid_answer_mass: 0.0005110852071084082
p4: 1.0481046501809033e-06
p8: 0.0005100371199660003
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/045_intervention_positions_3/run.md"
---

# 045_intervention_positions_3

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
  "intervention_positions": 3,
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
['-spin', 'Spin', 'seh', 'ปั่น', ' 인프라', '盐酸', 'spin', ' факта']
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

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.081  | 0.922169 | +0.015            |
| 2      | 'Based'   | -2.831  | 0.058952 | -0.110            |
| 3      | 'To'      | -5.831  | 0.002935 | -0.110            |
| 4      | 'Sp'      | -6.081  | 0.002286 | -0.485            |
| 5      | 'An'      | -6.206  | 0.002017 | -0.110            |
| 6      | '**'      | -6.331  | 0.001780 | -0.110            |
| 7      | 'Most'    | -6.456  | 0.001571 | -0.860            |
| 8      | 'First'   | -7.206  | 0.000742 | +0.015            |
| 9      | 'Animal'  | -7.331  | 0.000655 | -0.235            |
| 10     | '<think>' | -7.331  | 0.000655 | +0.140            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
