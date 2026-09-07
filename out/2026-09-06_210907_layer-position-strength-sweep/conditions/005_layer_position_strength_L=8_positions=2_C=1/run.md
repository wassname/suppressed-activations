---
condition_id: "005_layer_position_strength_L=8_positions=2_C=1"
axis: "layer_position_strength"
value: "L=8,positions=2,C=1"
is_default: false
swap_log_odds_shift: 0.1250002384185791
valid_answer_mass: 0.2884780764579773
p4: 0.0051886290311813354
p8: 0.28328946232795715
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/005_layer_position_strength_L=8_positions=2_C=1/run.md"
---

# 005_layer_position_strength_L=8_positions=2_C=1

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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `005_layer_position_strength_L=8_positions=2_C=1`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.136  | 0.321009 | +0.085            |
| 2      | '**'     | -1.261  | 0.283289 | -0.040            |
| 3      | '8'      | -1.261  | 0.283289 | -0.040            |
| 4      | 'Fact'   | -2.761  | 0.063210 | -0.040            |
| 5      | 'Number' | -4.136  | 0.015982 | -0.040            |
| 6      | '###'    | -4.261  | 0.014104 | -0.040            |
| 7      | '4'      | -5.261  | 0.005189 | +0.085            |
| 8      | '1'      | -6.386  | 0.001685 | -0.040            |
| 9      | '6'      | -6.886  | 0.001022 | +0.085            |
| 10     | 'Answer' | -6.886  | 0.001022 | +0.085            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
