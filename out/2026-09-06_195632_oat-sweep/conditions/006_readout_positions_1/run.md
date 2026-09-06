---
condition_id: "006_readout_positions_1"
axis: "readout_positions"
value: "1"
is_default: false
swap_log_odds_shift: 0.5625
valid_answer_mass: 0.0002849331358447671
p4: 9.621087428968167e-07
p8: 0.0002839710214175284
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/006_readout_positions_1/run.md"
---

# 006_readout_positions_1

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 1,
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
['在校园', '爱吃', '和金', '웹', ' localização', ' Kampus', 'писаться', '政委']
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
| 1      | 'The'     | -0.042  | 0.959216 | +0.054            |
| 2      | 'Based'   | -3.667  | 0.025562 | -0.946            |
| 3      | 'Sp'      | -5.917  | 0.002694 | -0.321            |
| 4      | 'An'      | -6.042  | 0.002378 | +0.054            |
| 5      | '**'      | -6.292  | 0.001852 | -0.071            |
| 6      | 'To'      | -6.542  | 0.001442 | -0.821            |
| 7      | '<think>' | -7.042  | 0.000875 | +0.429            |
| 8      | 'Animal'  | -7.417  | 0.000601 | -0.321            |
| 9      | 'First'   | -7.667  | 0.000468 | -0.446            |
| 10     | 'There'   | -7.917  | 0.000365 | -0.821            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
