---
condition_id: "017_intervention_layer_7"
axis: "intervention_layer"
value: "7"
is_default: false
swap_log_odds_shift: -0.5
valid_answer_mass: 0.4106847643852234
p4: 0.003987123258411884
p8: 0.4066976308822632
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/017_intervention_layer_7/run.md"
---

# 017_intervention_layer_7

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
  "intervention_layer": 7,
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
['ปั่น', '원', 'Spin', ' Ủy', ' laba', '哈密', 'kab', 'spin']
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
| 1      | '8'      | -0.900  | 0.406698 | +0.322            |
| 2      | '**'     | -1.275  | 0.279519 | -0.053            |
| 3      | 'The'    | -1.525  | 0.217690 | -0.303            |
| 4      | 'Fact'   | -3.400  | 0.033384 | -0.678            |
| 5      | 'Number' | -3.900  | 0.020248 | +0.197            |
| 6      | '###'    | -3.900  | 0.020248 | +0.322            |
| 7      | '4'      | -5.525  | 0.003987 | -0.178            |
| 8      | '1'      | -5.650  | 0.003519 | +0.697            |
| 9      | '6'      | -6.525  | 0.001467 | +0.447            |
| 10     | 'Answer' | -6.525  | 0.001467 | +0.447            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
