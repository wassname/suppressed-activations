---
condition_id: "015_normalization_strength_C=4,component_norm=False,residual_norm=False"
axis: "normalization_strength"
value: "C=4,component_norm=False,residual_norm=False"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.15407447516918182
p4: 0.0019154001493006945
p8: 0.15215907990932465
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/015_normalization_strength_C=4,component_norm=False,residual_norm=False/run.md"
---

# 015_normalization_strength_C=4,component_norm=False,residual_norm=False

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
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": false,
  "restore_residual_norm": false,
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
['盐酸', 'må', ' laba', ' Infant', '_keeper', ' webView', ' Urbano', 'ränkt']
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
| 1      | '**'     | -0.883  | 0.413611 | +0.339            |
| 2      | 'The'    | -1.383  | 0.250868 | -0.161            |
| 3      | '8'      | -1.883  | 0.152159 | -0.661            |
| 4      | 'Fact'   | -2.133  | 0.118502 | +0.589            |
| 5      | 'Number' | -4.008  | 0.018173 | +0.089            |
| 6      | '###'    | -4.008  | 0.018173 | +0.214            |
| 7      | '6'      | -4.633  | 0.009727 | +2.339            |
| 8      | 'Eight'  | -6.008  | 0.002459 | +0.839            |
| 9      | '1'      | -6.258  | 0.001915 | +0.089            |
| 10     | '4'      | -6.258  | 0.001915 | -0.911            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
