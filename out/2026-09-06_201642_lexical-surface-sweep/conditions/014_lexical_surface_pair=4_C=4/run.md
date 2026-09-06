---
condition_id: "014_lexical_surface_pair=4_C=4"
axis: "lexical_surface"
value: "pair=4,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.20280364155769348
p4: 0.003225874388590455
p8: 0.19957776367664337
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/014_lexical_surface_pair=4_C=4/run.md"
---

# 014_lexical_surface_pair=4_C=4

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
  "lexical_forms": "pair_4",
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
['Spin', '-spin', '\tspin', ' Spin', 'spin', ' laba', '_spin', ' webView']
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
| 1      | '**'     | -1.112  | 0.329048 | +0.110            |
| 2      | 'The'    | -1.112  | 0.329048 | +0.110            |
| 3      | '8'      | -1.612  | 0.199578 | -0.390            |
| 4      | 'Fact'   | -2.362  | 0.094274 | +0.360            |
| 5      | 'Number' | -4.237  | 0.014457 | -0.140            |
| 6      | '###'    | -4.237  | 0.014457 | -0.015            |
| 7      | '4'      | -5.737  | 0.003226 | -0.390            |
| 8      | '6'      | -5.862  | 0.002847 | +1.110            |
| 9      | '1'      | -6.362  | 0.001727 | -0.015            |
| 10     | 'Eight'  | -6.737  | 0.001187 | +0.110            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
