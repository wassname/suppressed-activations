---
condition_id: "019_layer_position_strength_L=12_positions=1_C=16"
axis: "layer_position_strength"
value: "L=12,positions=1,C=16"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.273398220539093
p4: 0.006281972862780094
p8: 0.2671162486076355
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/019_layer_position_strength_L=12_positions=1_C=16/run.md"
---

# 019_layer_position_strength_L=12_positions=1_C=16

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
  "intervention_layer": 12,
  "intervention_positions": 1,
  "strength": 16.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "12": {
    "residual_norm": 7.825362682342529,
    "perturbation_norm": 6.147679805755615,
    "relative_perturbation_by_position": [
      0.7856095433235168
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.070  | 0.342984 | +0.151            |
| 2      | 'The'    | -1.320  | 0.267116 | -0.099            |
| 3      | '8'      | -1.320  | 0.267116 | -0.099            |
| 4      | 'Fact'   | -2.820  | 0.059602 | -0.099            |
| 5      | '###'    | -3.695  | 0.024846 | +0.526            |
| 6      | 'Number' | -4.195  | 0.015070 | -0.099            |
| 7      | '4'      | -5.070  | 0.006282 | +0.276            |
| 8      | '1'      | -6.195  | 0.002039 | +0.151            |
| 9      | 'Answer' | -6.445  | 0.001588 | +0.526            |
| 10     | 'Eight'  | -6.820  | 0.001092 | +0.026            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
