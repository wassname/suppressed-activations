---
condition_id: "009_layer_position_strength_L=8_positions=2_C=16"
axis: "layer_position_strength"
value: "L=8,positions=2,C=16"
is_default: false
swap_log_odds_shift: 0.3749997615814209
valid_answer_mass: 0.26530104875564575
p4: 0.006095918361097574
p8: 0.2592051327228546
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/009_layer_position_strength_L=8_positions=2_C=16/run.md"
---

# 009_layer_position_strength_L=8_positions=2_C=16

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
  "intervention_layer": 8,
  "intervention_positions": 2,
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

[Full diagnostic data](../../result.json) (`rows` → `009_layer_position_strength_L=8_positions=2_C=16`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.100  | 0.332826 | +0.121            |
| 2      | 'The'    | -1.225  | 0.293718 | -0.004            |
| 3      | '8'      | -1.350  | 0.259205 | -0.129            |
| 4      | 'Fact'   | -2.725  | 0.065537 | -0.004            |
| 5      | 'Number' | -4.225  | 0.014623 | -0.129            |
| 6      | '###'    | -4.225  | 0.014623 | -0.004            |
| 7      | '4'      | -5.100  | 0.006096 | +0.246            |
| 8      | '6'      | -6.600  | 0.001360 | +0.371            |
| 9      | 'Answer' | -6.600  | 0.001360 | +0.371            |
| 10     | '1'      | -6.725  | 0.001200 | -0.379            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
