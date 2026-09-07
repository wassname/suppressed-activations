---
condition_id: "003_layer_position_strength_L=8_positions=1_C=8"
axis: "layer_position_strength"
value: "L=8,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2767699360847473
p4: 0.004978042095899582
p8: 0.27179190516471863
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/003_layer_position_strength_L=8_positions=1_C=8/run.md"
---

# 003_layer_position_strength_L=8_positions=1_C=8

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
  "intervention_positions": 1,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `003_layer_position_strength_L=8_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.178  | 0.307981 | +0.044            |
| 2      | '**'     | -1.178  | 0.307981 | +0.044            |
| 3      | '8'      | -1.303  | 0.271792 | -0.081            |
| 4      | 'Fact'   | -2.803  | 0.060645 | -0.081            |
| 5      | 'Number' | -4.053  | 0.017375 | +0.044            |
| 6      | '###'    | -4.178  | 0.015333 | +0.044            |
| 7      | '4'      | -5.303  | 0.004978 | +0.044            |
| 8      | '1'      | -6.303  | 0.001831 | +0.044            |
| 9      | 'Answer' | -6.803  | 0.001111 | +0.169            |
| 10     | 'Eight'  | -6.928  | 0.000980 | -0.081            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
