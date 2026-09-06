---
condition_id: "049_strength_0.5"
axis: "strength"
value: "0.5"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.27306613326072693
p4: 0.004911425057798624
p8: 0.26815471053123474
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['Spin', '-spin', ' Spin', 'spin', '\tspin', '_spin', 'ปั่น', 'seh']
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
| 1      | 'The'    | -1.191  | 0.303859 | +0.030            |
| 2      | '**'     | -1.191  | 0.303859 | +0.030            |
| 3      | '8'      | -1.316  | 0.268155 | -0.095            |
| 4      | 'Fact'   | -2.566  | 0.076828 | +0.155            |
| 5      | 'Number' | -4.191  | 0.015128 | -0.095            |
| 6      | '###'    | -4.316  | 0.013351 | -0.095            |
| 7      | '4'      | -5.316  | 0.004911 | +0.030            |
| 8      | '1'      | -6.441  | 0.001595 | -0.095            |
| 9      | '6'      | -6.816  | 0.001096 | +0.155            |
| 10     | 'Answer' | -6.816  | 0.001096 | +0.155            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
