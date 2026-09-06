---
condition_id: "014_intervention_layer_4"
axis: "intervention_layer"
value: "4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.260622501373291
p4: 0.004145564511418343
p8: 0.2564769387245178
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/014_intervention_layer_4/run.md"
---

# 014_intervention_layer_4

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
  "intervention_layer": 4,
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
['盐酸', ' laba', ' webView', 'Integrated', '资讯网', ' consu', ' Infant', ' VIH']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.861  | 0.422859 | +0.361            |
| 2      | '8'      | -1.361  | 0.256477 | -0.139            |
| 3      | 'The'    | -1.861  | 0.155561 | -0.639            |
| 4      | 'Fact'   | -2.111  | 0.121151 | +0.611            |
| 5      | '###'    | -4.361  | 0.012769 | -0.139            |
| 6      | 'Number' | -4.736  | 0.008776 | -0.639            |
| 7      | '4'      | -5.486  | 0.004146 | -0.139            |
| 8      | '6'      | -5.486  | 0.004146 | +1.486            |
| 9      | '1'      | -5.861  | 0.002849 | +0.486            |
| 10     | '#'      | -6.986  | 0.000925 | +0.236            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
