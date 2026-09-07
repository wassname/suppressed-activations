---
condition_id: "041_layer_position_strength_L=16_positions=4_C=2"
axis: "layer_position_strength"
value: "L=16,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3106731176376343
p4: 0.005587832536548376
p8: 0.30508527159690857
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/041_layer_position_strength_L=16_positions=4_C=2/run.md"
---

# 041_layer_position_strength_L=16_positions=4_C=2

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
  "intervention_layer": 16,
  "intervention_positions": 4,
  "strength": 2.0,
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
['Spin', 'ปั่น', ' Presents', '\tspin', '-spin', 'spin', '_spin', ' Ủy']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `041_layer_position_strength_L=16_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.187  | 0.305085 | +0.034            |
| 2      | '8'      | -1.187  | 0.305085 | +0.034            |
| 3      | '**'     | -1.312  | 0.269237 | -0.091            |
| 4      | 'Fact'   | -2.687  | 0.068074 | +0.034            |
| 5      | 'Number' | -4.062  | 0.017212 | +0.034            |
| 6      | '###'    | -4.187  | 0.015189 | +0.034            |
| 7      | '4'      | -5.187  | 0.005588 | +0.159            |
| 8      | '1'      | -6.312  | 0.001814 | +0.034            |
| 9      | 'Answer' | -6.812  | 0.001100 | +0.159            |
| 10     | 'Eight'  | -6.812  | 0.001100 | +0.034            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
