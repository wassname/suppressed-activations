---
condition_id: "027_layer_position_strength_L=12_positions=4_C=4"
axis: "layer_position_strength"
value: "L=12,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.28617745637893677
p4: 0.006575604435056448
p8: 0.2796018421649933
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/027_layer_position_strength_L=12_positions=4_C=4/run.md"
---

# 027_layer_position_strength_L=12_positions=4_C=4

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
['Spin', '\tspin', 'ปั่น', ' Presents', '_spin', ' Ủy', '资讯网', '哈密']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `027_layer_position_strength_L=12_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.149  | 0.316830 | +0.072            |
| 2      | 'The'    | -1.274  | 0.279602 | -0.053            |
| 3      | '8'      | -1.274  | 0.279602 | -0.053            |
| 4      | 'Fact'   | -2.774  | 0.062388 | -0.053            |
| 5      | '###'    | -3.899  | 0.020254 | +0.322            |
| 6      | 'Number' | -4.024  | 0.017874 | +0.072            |
| 7      | '4'      | -5.024  | 0.006576 | +0.322            |
| 8      | '1'      | -6.024  | 0.002419 | +0.322            |
| 9      | '6'      | -6.399  | 0.001663 | +0.572            |
| 10     | 'Answer' | -6.774  | 0.001143 | +0.197            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
