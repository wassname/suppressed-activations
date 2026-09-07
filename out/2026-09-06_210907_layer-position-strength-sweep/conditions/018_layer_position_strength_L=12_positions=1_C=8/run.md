---
condition_id: "018_layer_position_strength_L=12_positions=1_C=8"
axis: "layer_position_strength"
value: "L=12,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.1250002384185791
valid_answer_mass: 0.28619030117988586
p4: 0.0051474804058671
p8: 0.28104281425476074
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/018_layer_position_strength_L=12_positions=1_C=8/run.md"
---

# 018_layer_position_strength_L=12_positions=1_C=8

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

[Full diagnostic data](../../result.json) (`rows` → `018_layer_position_strength_L=12_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.144  | 0.318463 | +0.077            |
| 2      | 'The'    | -1.269  | 0.281043 | -0.048            |
| 3      | '8'      | -1.269  | 0.281043 | -0.048            |
| 4      | 'Fact'   | -2.769  | 0.062709 | -0.048            |
| 5      | '###'    | -3.894  | 0.020359 | +0.327            |
| 6      | 'Number' | -4.144  | 0.015855 | -0.048            |
| 7      | '4'      | -5.269  | 0.005147 | +0.077            |
| 8      | '1'      | -6.269  | 0.001894 | +0.077            |
| 9      | 'Answer' | -6.769  | 0.001149 | +0.202            |
| 10     | '6'      | -6.894  | 0.001014 | +0.077            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
