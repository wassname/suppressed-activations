---
condition_id: "008_readout_positions_8"
axis: "readout_positions"
value: "8"
is_default: false
swap_log_odds_shift: 1.4375
valid_answer_mass: 0.00028592481976374984
p4: 2.30512364396418e-06
p8: 0.00028361970908008516
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/008_readout_positions_8/run.md"
---

# 008_readout_positions_8

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 8,
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
['在校园', ' факта', '丝绸', ' 인프라', '迪斯', '盐酸', '_rsp', '和金']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', '吠', 'DOG', ' Dog']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.230  | 0.794235 | -0.134            |
| 2      | 'Based' | -1.855  | 0.156394 | +0.866            |
| 3      | 'To'    | -4.730  | 0.008823 | +0.991            |
| 4      | 'There' | -4.980  | 0.006871 | +2.116            |
| 5      | 'Sp'    | -5.230  | 0.005352 | +0.366            |
| 6      | '**'    | -5.730  | 0.003246 | +0.491            |
| 7      | 'An'    | -5.980  | 0.002528 | +0.116            |
| 8      | 'First' | -6.230  | 0.001969 | +0.991            |
| 9      | 'That'  | -6.355  | 0.001737 | +1.241            |
| 10     | 'Anim'  | -6.355  | 0.001737 | +0.616            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
