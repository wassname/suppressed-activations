---
condition_id: "015_intervention_layer_5"
axis: "intervention_layer"
value: "5"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.38527384400367737
p4: 0.005418348591774702
p8: 0.3798554837703705
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/015_intervention_layer_5/run.md"
---

# 015_intervention_layer_5

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
  "intervention_layer": 5,
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
[' laba', 'Spin', 'Integrated', '盐酸', '\tspin', ' mdi', ' webView', ' веб']
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
| 1      | '8'      | -0.968  | 0.379855 | +0.254            |
| 2      | '**'     | -1.218  | 0.295832 | +0.004            |
| 3      | 'The'    | -1.468  | 0.230394 | -0.246            |
| 4      | 'Fact'   | -2.843  | 0.058253 | -0.121            |
| 5      | 'Number' | -4.843  | 0.007884 | -0.746            |
| 6      | '###'    | -4.843  | 0.007884 | -0.621            |
| 7      | '4'      | -5.218  | 0.005418 | +0.129            |
| 8      | '1'      | -5.718  | 0.003286 | +0.629            |
| 9      | 'Answer' | -6.468  | 0.001552 | +0.504            |
| 10     | '#'      | -6.968  | 0.000942 | +0.254            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
