---
condition_id: "067_layer_position_strength_L=23_positions=2_C=4"
axis: "layer_position_strength"
value: "L=23,positions=2,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2968754768371582
p4: 0.004722219426184893
p8: 0.2921532690525055
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/067_layer_position_strength_L=23_positions=2_C=4/run.md"
---

# 067_layer_position_strength_L=23_positions=2_C=4

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
  "intervention_layer": 23,
  "intervention_positions": 2,
  "strength": 4.0,
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
['compan', 'seh', 'amax', 'ปั่น', '-spin', ' Ủy', 'Spin', 'สุนัข']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 32.133758544921875,
    "perturbation_norm": 8.239299774169922,
    "relative_perturbation_by_position": [
      0.22816142439842224,
      0.28335294127464294
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.230  | 0.292153 | -0.009            |
| 2      | 'The'    | -1.230  | 0.292153 | -0.009            |
| 3      | '**'     | -1.230  | 0.292153 | -0.009            |
| 4      | 'Fact'   | -2.605  | 0.073868 | +0.116            |
| 5      | 'Number' | -4.105  | 0.016482 | -0.009            |
| 6      | '###'    | -4.230  | 0.014545 | -0.009            |
| 7      | '4'      | -5.355  | 0.004722 | -0.009            |
| 8      | '1'      | -6.355  | 0.001737 | -0.009            |
| 9      | 'Answer' | -6.855  | 0.001054 | +0.116            |
| 10     | 'Eight'  | -6.855  | 0.001054 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
