---
condition_id: "071_layer_position_strength_L=23_positions=4_C=2"
axis: "layer_position_strength"
value: "L=23,positions=4,C=2"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.2988317608833313
p4: 0.0037149719428271055
p8: 0.2951167821884155
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/071_layer_position_strength_L=23_positions=4_C=2/run.md"
---

# 071_layer_position_strength_L=23_positions=4_C=2

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
  "intervention_layer": 23,
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
['compan', ' Ủy', 'seh', ' Uỷ', ' ủy', '友達', 'вна', ' webové']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `071_layer_position_strength_L=23_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.220  | 0.295117 | +0.001            |
| 2      | 'The'    | -1.220  | 0.295117 | +0.001            |
| 3      | '**'     | -1.220  | 0.295117 | +0.001            |
| 4      | 'Fact'   | -2.720  | 0.065849 | +0.001            |
| 5      | 'Number' | -4.095  | 0.016649 | +0.001            |
| 6      | '###'    | -4.220  | 0.014693 | +0.001            |
| 7      | '4'      | -5.595  | 0.003715 | -0.249            |
| 8      | '1'      | -6.345  | 0.001755 | +0.001            |
| 9      | 'Answer' | -6.845  | 0.001064 | +0.126            |
| 10     | 'Eight'  | -6.845  | 0.001064 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
