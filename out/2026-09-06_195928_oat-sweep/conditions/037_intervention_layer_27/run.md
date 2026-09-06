---
condition_id: "037_intervention_layer_27"
axis: "intervention_layer"
value: "27"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3005707561969757
p4: 0.00540612917393446
p8: 0.2951646149158478
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/037_intervention_layer_27/run.md"
---

# 037_intervention_layer_27

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
  "intervention_layer": 27,
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp', '-spin']
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
| 1      | '8'      | -1.220  | 0.295165 | +0.001            |
| 2      | 'The'    | -1.220  | 0.295165 | +0.001            |
| 3      | '**'     | -1.220  | 0.295165 | +0.001            |
| 4      | 'Fact'   | -2.720  | 0.065860 | +0.001            |
| 5      | 'Number' | -4.095  | 0.016652 | +0.001            |
| 6      | '###'    | -4.345  | 0.012969 | -0.124            |
| 7      | '4'      | -5.220  | 0.005406 | +0.126            |
| 8      | '1'      | -6.345  | 0.001755 | +0.001            |
| 9      | '6'      | -6.845  | 0.001065 | +0.126            |
| 10     | 'Answer' | -6.845  | 0.001065 | +0.126            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
