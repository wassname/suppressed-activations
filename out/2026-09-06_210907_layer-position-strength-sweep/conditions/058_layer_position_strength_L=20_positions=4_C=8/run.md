---
condition_id: "058_layer_position_strength_L=20_positions=4_C=8"
axis: "layer_position_strength"
value: "L=20,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2737024128437042
p4: 0.0038492484018206596
p8: 0.2698531746864319
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/058_layer_position_strength_L=20_positions=4_C=8/run.md"
---

# 058_layer_position_strength_L=20_positions=4_C=8

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
['клада', 'må', ' webView', ' веб', ' webové', ' niem', '特种兵', 'ปา']
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
    "perturbation_norm": 18.423351287841797,
    "relative_perturbation_by_position": [
      0.7472490072250366,
      0.5342915654182434,
      0.35258445143699646,
      0.44143328070640564
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
| 1      | 'The'    | -1.185  | 0.305784 | +0.037            |
| 2      | '**'     | -1.185  | 0.305784 | +0.037            |
| 3      | '8'      | -1.310  | 0.269853 | -0.088            |
| 4      | 'Fact'   | -2.685  | 0.068230 | +0.037            |
| 5      | 'Number' | -4.060  | 0.017251 | +0.037            |
| 6      | '###'    | -4.185  | 0.015224 | +0.037            |
| 7      | '4'      | -5.560  | 0.003849 | -0.213            |
| 8      | '1'      | -6.435  | 0.001605 | -0.088            |
| 9      | 'Eight'  | -6.560  | 0.001416 | +0.287            |
| 10     | '6'      | -6.810  | 0.001103 | +0.162            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
