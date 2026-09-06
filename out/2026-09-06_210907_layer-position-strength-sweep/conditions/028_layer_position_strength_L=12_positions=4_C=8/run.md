---
condition_id: "028_layer_position_strength_L=12_positions=4_C=8"
axis: "layer_position_strength"
value: "L=12,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.7500002384185791
valid_answer_mass: 0.2857467234134674
p4: 0.009454211220145226
p8: 0.27629250288009644
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/028_layer_position_strength_L=12_positions=4_C=8/run.md"
---

# 028_layer_position_strength_L=12_positions=4_C=8

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
  "intervention_positions": 4,
  "strength": 8.0,
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
[' Empresarial', '资讯网', ' Presents', '哈密', 'ılım', 'kab', ' fär', '前から']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "12": {
    "residual_norm": 18.060396194458008,
    "perturbation_norm": 10.678647994995117,
    "relative_perturbation_by_position": [
      0.7417334914207458,
      0.5520732998847961,
      0.5218048095703125,
      0.47437751293182373
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
| 1      | '**'     | -1.161  | 0.313080 | +0.060            |
| 2      | 'The'    | -1.286  | 0.276293 | -0.065            |
| 3      | '8'      | -1.286  | 0.276293 | -0.065            |
| 4      | 'Fact'   | -3.036  | 0.048012 | -0.315            |
| 5      | '###'    | -3.536  | 0.029121 | +0.685            |
| 6      | 'Number' | -3.911  | 0.020015 | +0.185            |
| 7      | '4'      | -4.661  | 0.009454 | +0.685            |
| 8      | '6'      | -5.161  | 0.005734 | +1.810            |
| 9      | '1'      | -5.536  | 0.003941 | +0.810            |
| 10     | 'Answer' | -6.536  | 0.001450 | +0.435            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
