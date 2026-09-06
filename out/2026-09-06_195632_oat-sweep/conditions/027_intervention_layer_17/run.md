---
condition_id: "027_intervention_layer_17"
axis: "intervention_layer"
value: "17"
is_default: false
swap_log_odds_shift: 0.3125
valid_answer_mass: 0.0005711328121833503
p4: 1.50303549162345e-06
p8: 0.0005696297739632428
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/027_intervention_layer_17/run.md"
---

# 027_intervention_layer_17

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
  "intervention_layer": 17,
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
[' 인프라', 'seh', 'Integrated', '\tspin', 'edata', ' legado', '盐酸', 'Spin']
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
| 1      | 'The'   | -0.096  | 0.908897 | +0.001            |
| 2      | 'Based' | -2.846  | 0.058104 | -0.124            |
| 3      | 'Sp'    | -5.346  | 0.004769 | +0.251            |
| 4      | 'Most'  | -5.346  | 0.004769 | +0.251            |
| 5      | 'An'    | -5.471  | 0.004209 | +0.626            |
| 6      | 'To'    | -5.596  | 0.003714 | +0.126            |
| 7      | '**'    | -6.221  | 0.001988 | +0.001            |
| 8      | 'Anim'  | -6.596  | 0.001366 | +0.376            |
| 9      | 'That'  | -6.846  | 0.001064 | +0.751            |
| 10     | 'First' | -6.846  | 0.001064 | +0.376            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
