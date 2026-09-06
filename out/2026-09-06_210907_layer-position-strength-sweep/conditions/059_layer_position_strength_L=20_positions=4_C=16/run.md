---
condition_id: "059_layer_position_strength_L=20_positions=4_C=16"
axis: "layer_position_strength"
value: "L=20,positions=4,C=16"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2567254900932312
p4: 0.003610491519793868
p8: 0.2531149983406067
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/059_layer_position_strength_L=20_positions=4_C=16/run.md"
---

# 059_layer_position_strength_L=20_positions=4_C=16

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
  "intervention_layer": 20,
  "intervention_positions": 4,
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
[' Sáng', 'клада', ' spezi', 'máy', '_ALIGNMENT', '嫌弃', 'fsp', 'ปา']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "20": {
    "residual_norm": 33.78907775878906,
    "perturbation_norm": 28.52530860900879,
    "relative_perturbation_by_position": [
      1.0572201013565063,
      0.8579033017158508,
      0.6265701055526733,
      0.7432265877723694
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
| 1      | 'The'    | -1.124  | 0.325006 | +0.098            |
| 2      | '**'     | -1.249  | 0.286817 | -0.027            |
| 3      | '8'      | -1.374  | 0.253115 | -0.152            |
| 4      | 'Fact'   | -2.624  | 0.072519 | +0.098            |
| 5      | 'Number' | -3.999  | 0.018336 | +0.098            |
| 6      | '###'    | -4.249  | 0.014280 | -0.027            |
| 7      | '6'      | -4.374  | 0.012602 | +2.598            |
| 8      | '4'      | -5.624  | 0.003610 | -0.277            |
| 9      | '1'      | -6.249  | 0.001933 | +0.098            |
| 10     | 'Eight'  | -6.624  | 0.001328 | +0.223            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
