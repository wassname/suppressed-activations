---
condition_id: "030_lexical_surface_union_C=4_divide=1"
axis: "lexical_surface"
value: "union,C=4,divide=1"
is_default: false
swap_log_odds_shift: 1.000000238418579
valid_answer_mass: 0.1742328703403473
p4: 0.007333067245781422
p8: 0.16689980030059814
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/030_lexical_surface_union_C=4_divide=1/run.md"
---

# 030_lexical_surface_union_C=4_divide=1

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
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "union",
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
['Spin', '-spin', '\tspin', 'spin', '_spin', ' laba', ' Spin', ' webView']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Unlike insects, which typically have six legs, spiders belong to the
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.040  | 0.353327 | +0.181            |
| 2      | 'The'    | -1.165  | 0.311810 | +0.056            |
| 3      | '8'      | -1.790  | 0.166900 | -0.569            |
| 4      | 'Fact'   | -2.540  | 0.078838 | +0.181            |
| 5      | 'Number' | -3.290  | 0.037240 | +0.806            |
| 6      | '###'    | -3.790  | 0.022587 | +0.431            |
| 7      | '4'      | -4.915  | 0.007333 | +0.431            |
| 8      | '1'      | -5.665  | 0.003464 | +0.681            |
| 9      | '6'      | -6.165  | 0.002101 | +0.806            |
| 10     | 'Eight'  | -6.290  | 0.001854 | +0.556            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
