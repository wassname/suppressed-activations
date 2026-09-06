---
condition_id: "085_layer_position_strength_L=24_positions=4_C=1"
axis: "layer_position_strength"
value: "L=24,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2969400882720947
p4: 0.004723246209323406
p8: 0.29221683740615845
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.125
log: "conditions/085_layer_position_strength_L=24_positions=4_C=1/run.md"
---

# 085_layer_position_strength_L=24_positions=4_C=1

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
  "strength": 1.0,
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
['compan', ' Ủy', 'kab', ' webové', 'umd', ' HttpContext', 'вна', ' Galler']
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
    "perturbation_norm": 5.6094207763671875,
    "relative_perturbation_by_position": [
      0.1724119633436203,
      0.1155473068356514,
      0.041982926428318024,
      0.06328174471855164
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
| 1      | '8'      | -1.230  | 0.292217 | -0.009            |
| 2      | 'The'    | -1.230  | 0.292217 | -0.009            |
| 3      | '**'     | -1.230  | 0.292217 | -0.009            |
| 4      | 'Fact'   | -2.605  | 0.073884 | +0.116            |
| 5      | 'Number' | -4.105  | 0.016486 | -0.009            |
| 6      | '###'    | -4.230  | 0.014549 | -0.009            |
| 7      | '4'      | -5.355  | 0.004723 | -0.009            |
| 8      | '1'      | -6.355  | 0.001738 | -0.009            |
| 9      | 'Answer' | -6.855  | 0.001054 | +0.116            |
| 10     | 'Eight'  | -6.855  | 0.001054 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
