---
condition_id: "049_strength_0.5"
axis: "strength"
value: "0.5"
is_default: false
swap_log_odds_shift: -0.0625
valid_answer_mass: 0.0006529971724376082
p4: 1.1820627605629852e-06
p8: 0.0006518150912597775
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/049_strength_0.5/run.md"
---

# 049_strength_0.5

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
  "intervention_positions": "all",
  "strength": 0.5,
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
['Spin', '-spin', 'spin', ' Spin', '\tspin', '_spin', 'seh', '盐酸']
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
| 1      | 'The'     | -0.086  | 0.917824 | +0.010            |
| 2      | 'Based'   | -2.836  | 0.058675 | -0.115            |
| 3      | 'Sp'      | -5.586  | 0.003751 | +0.010            |
| 4      | 'To'      | -5.836  | 0.002921 | -0.115            |
| 5      | 'Most'    | -5.961  | 0.002578 | -0.365            |
| 6      | 'An'      | -6.086  | 0.002275 | +0.010            |
| 7      | '**'      | -6.336  | 0.001772 | -0.115            |
| 8      | 'Animal'  | -7.086  | 0.000837 | +0.010            |
| 9      | 'Anim'    | -7.211  | 0.000739 | -0.240            |
| 10     | '<think>' | -7.211  | 0.000739 | +0.260            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
