---
condition_id: "047_intervention_positions_8"
axis: "intervention_positions"
value: "8"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.16013488173484802
p4: 0.004693910479545593
p8: 0.15544097125530243
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/047_intervention_positions_8/run.md"
---

# 047_intervention_positions_8

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
  "intervention_layer": 1,
  "intervention_positions": 8,
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
['的场所', 'ISA', ' responseData', ' Bỉ', 'χω', '什么都没有', ' Hauses', ' دری']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.111  | 0.329069 | +0.110            |
| 2      | 'The'    | -1.111  | 0.329069 | +0.110            |
| 3      | '8'      | -1.861  | 0.155441 | -0.640            |
| 4      | 'Fact'   | -2.611  | 0.073425 | +0.110            |
| 5      | '6'      | -3.111  | 0.044535 | +3.860            |
| 6      | 'Number' | -3.986  | 0.018565 | +0.110            |
| 7      | '###'    | -4.236  | 0.014458 | -0.015            |
| 8      | '1'      | -4.611  | 0.009937 | +1.735            |
| 9      | '4'      | -5.361  | 0.004694 | -0.015            |
| 10     | '2'      | -5.861  | 0.002847 | +1.860            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
