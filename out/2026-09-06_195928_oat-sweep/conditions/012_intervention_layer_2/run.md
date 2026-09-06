---
condition_id: "012_intervention_layer_2"
axis: "intervention_layer"
value: "2"
is_default: false
swap_log_odds_shift: -1.0
valid_answer_mass: 0.22640752792358398
p4: 0.0013383104233071208
p8: 0.22506922483444214
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['盐酸', 'må', '意志力', ' medarbe', ' Monteiro', 'idité', '张掖', ' 인프라']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.116  | 0.327474 | +0.105            |
| 2      | 'The'    | -1.241  | 0.288995 | -0.020            |
| 3      | '8'      | -1.491  | 0.225069 | -0.270            |
| 4      | 'Fact'   | -2.366  | 0.093823 | +0.355            |
| 5      | 'Number' | -3.991  | 0.018475 | +0.105            |
| 6      | '###'    | -4.116  | 0.016304 | +0.105            |
| 7      | '6'      | -4.741  | 0.008727 | +2.230            |
| 8      | '1'      | -5.491  | 0.004122 | +0.855            |
| 9      | 'Eight'  | -5.866  | 0.002833 | +0.980            |
| 10     | '4'      | -6.616  | 0.001338 | -1.270            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
