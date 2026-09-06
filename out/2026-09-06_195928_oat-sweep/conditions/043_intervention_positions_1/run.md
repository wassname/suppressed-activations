---
condition_id: "043_intervention_positions_1"
axis: "intervention_positions"
value: "1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2994941473007202
p4: 0.004763872362673283
p8: 0.2947302758693695
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/043_intervention_positions_1/run.md"
---

# 043_intervention_positions_1

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
  "intervention_positions": 1,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
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
| 1      | '8'      | -1.222  | 0.294730 | -0.000            |
| 2      | 'The'    | -1.222  | 0.294730 | -0.000            |
| 3      | '**'     | -1.222  | 0.294730 | -0.000            |
| 4      | 'Fact'   | -2.722  | 0.065763 | -0.000            |
| 5      | 'Number' | -4.097  | 0.016628 | -0.000            |
| 6      | '###'    | -4.222  | 0.014674 | -0.000            |
| 7      | '4'      | -5.347  | 0.004764 | -0.000            |
| 8      | '1'      | -6.347  | 0.001753 | -0.000            |
| 9      | 'Answer' | -6.847  | 0.001063 | +0.125            |
| 10     | 'Eight'  | -6.847  | 0.001063 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
