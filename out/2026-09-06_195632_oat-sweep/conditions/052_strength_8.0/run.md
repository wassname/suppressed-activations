---
condition_id: "052_strength_8.0"
axis: "strength"
value: "8.0"
is_default: false
swap_log_odds_shift: 3.4375
valid_answer_mass: 5.268098902888596e-05
p4: 2.9845054996258114e-06
p8: 4.9696482165018097e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "Based"
readout_overlap: 0.0
log: "conditions/052_strength_8.0/run.md"
---

# 052_strength_8.0

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
  "strength": 8.0,
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
['在校园', 'ехать', ' creams', 'kre', '웹', ' krém', ' división', ' mommy']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
Based on the biological facts regarding spiders (the animals that spin webs):

Spiders are arachnids, which means they have **8 legs**.


```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'Based'    | -1.222  | 0.294618 | +1.499            |
| 2      | 'The'      | -1.347  | 0.259999 | -1.251            |
| 3      | 'There'    | -1.472  | 0.229449 | +5.624            |
| 4      | 'It'       | -2.097  | 0.122815 | +7.249            |
| 5      | 'Actually' | -3.472  | 0.031052 | +5.124            |
| 6      | 'That'     | -3.972  | 0.018834 | +3.624            |
| 7      | '**'       | -4.722  | 0.008897 | +1.499            |
| 8      | 'This'     | -4.972  | 0.006929 | +2.874            |
| 9      | 'I'        | -5.222  | 0.005396 | +4.187            |
| 10     | 'You'      | -5.847  | 0.002888 | +2.187            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
