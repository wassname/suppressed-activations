---
condition_id: "033_intervention_layer_23"
axis: "intervention_layer"
value: "23"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.3033009171485901
p4: 0.0033323492389172316
p8: 0.29996857047080994
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.375
log: "conditions/033_intervention_layer_23/run.md"
---

# 033_intervention_layer_23

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
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
['compan', ' Ủy', ' Uỷ', ' NHÀ', '友達', 'seh', ' ủy', ' компание']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.204  | 0.299969 | +0.017            |
| 2      | '**'     | -1.204  | 0.299969 | +0.017            |
| 3      | 'The'    | -1.329  | 0.264721 | -0.108            |
| 4      | 'Fact'   | -2.454  | 0.085942 | +0.267            |
| 5      | 'Number' | -4.079  | 0.016923 | +0.017            |
| 6      | '###'    | -4.204  | 0.014935 | +0.017            |
| 7      | '4'      | -5.704  | 0.003332 | -0.358            |
| 8      | '1'      | -6.329  | 0.001784 | +0.017            |
| 9      | 'Answer' | -6.704  | 0.001226 | +0.267            |
| 10     | 'Eight'  | -6.829  | 0.001082 | +0.017            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
