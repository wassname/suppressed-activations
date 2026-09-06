---
condition_id: "088_layer_position_strength_L=24_positions=4_C=8"
axis: "layer_position_strength"
value: "L=24,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28626105189323425
p4: 0.00514875166118145
p8: 0.28111231327056885
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/088_layer_position_strength_L=24_positions=4_C=8/run.md"
---

# 088_layer_position_strength_L=24_positions=4_C=8

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
  "intervention_layer": 24,
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
['compan', ' собаки', ' Hunde', ' собака', ' собак', ' chiens', 'amax', '狗']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 51.78230285644531,
    "perturbation_norm": 34.468196868896484,
    "relative_perturbation_by_position": [
      0.9656286835670471,
      0.7518875002861023,
      0.3219926357269287,
      0.4662967026233673
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.144  | 0.318542 | +0.078            |
| 2      | '**'     | -1.269  | 0.281112 | -0.047            |
| 3      | '8'      | -1.269  | 0.281112 | -0.047            |
| 4      | 'Fact'   | -2.644  | 0.071076 | +0.078            |
| 5      | 'Number' | -4.144  | 0.015859 | -0.047            |
| 6      | '###'    | -4.269  | 0.013996 | -0.047            |
| 7      | '4'      | -5.269  | 0.005149 | +0.078            |
| 8      | '1'      | -6.394  | 0.001672 | -0.047            |
| 9      | 'Answer' | -6.894  | 0.001014 | +0.078            |
| 10     | 'Eight'  | -6.894  | 0.001014 | -0.047            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
