---
condition_id: "022_layer_position_strength_L=12_positions=2_C=4"
axis: "layer_position_strength"
value: "L=12,positions=2,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.3093882203102112
p4: 0.004921249579638243
p8: 0.30446696281433105
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/022_layer_position_strength_L=12_positions=2_C=4/run.md"
---

# 022_layer_position_strength_L=12_positions=2_C=4

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
    "residual_norm": 11.424951553344727,
    "perturbation_norm": 3.054464101791382,
    "relative_perturbation_by_position": [
      0.27973300218582153,
      0.25260746479034424
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
| 1      | '8'      | -1.189  | 0.304467 | +0.032            |
| 2      | '**'     | -1.189  | 0.304467 | +0.032            |
| 3      | 'The'    | -1.314  | 0.268691 | -0.093            |
| 4      | 'Fact'   | -2.689  | 0.067936 | +0.032            |
| 5      | 'Number' | -4.064  | 0.017177 | +0.032            |
| 6      | '###'    | -4.064  | 0.017177 | +0.157            |
| 7      | '4'      | -5.314  | 0.004921 | +0.032            |
| 8      | '1'      | -6.314  | 0.001810 | +0.032            |
| 9      | '6'      | -6.814  | 0.001098 | +0.157            |
| 10     | 'Answer' | -6.814  | 0.001098 | +0.157            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
