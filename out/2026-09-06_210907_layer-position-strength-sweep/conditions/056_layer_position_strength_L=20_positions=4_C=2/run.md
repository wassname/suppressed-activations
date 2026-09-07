---
condition_id: "056_layer_position_strength_L=20_positions=4_C=2"
axis: "layer_position_strength"
value: "L=20,positions=4,C=2"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.29913076758384705
p4: 0.004206863697618246
p8: 0.29492390155792236
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/056_layer_position_strength_L=20_positions=4_C=2/run.md"
---

# 056_layer_position_strength_L=20_positions=4_C=2

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
['Spin', '\tspin', ' Presents', '_spin', 'seh', ' веб', 'Integrated', ' webView']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `056_layer_position_strength_L=20_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.221  | 0.294924 | +0.000            |
| 2      | 'The'    | -1.221  | 0.294924 | +0.000            |
| 3      | '**'     | -1.221  | 0.294924 | +0.000            |
| 4      | 'Fact'   | -2.721  | 0.065806 | +0.000            |
| 5      | 'Number' | -4.096  | 0.016638 | +0.000            |
| 6      | '###'    | -4.221  | 0.014683 | +0.000            |
| 7      | '4'      | -5.471  | 0.004207 | -0.125            |
| 8      | '1'      | -6.346  | 0.001754 | +0.000            |
| 9      | 'Eight'  | -6.721  | 0.001205 | +0.125            |
| 10     | 'Answer' | -6.846  | 0.001064 | +0.125            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
