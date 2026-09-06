---
condition_id: "051_strength_2.0"
axis: "strength"
value: "2.0"
is_default: false
swap_log_odds_shift: -0.625
valid_answer_mass: 0.23067373037338257
p4: 0.001978600164875388
p8: 0.2286951243877411
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/051_strength_2.0/run.md"
---

# 051_strength_2.0

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
  "strength": 2.0,
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
['Spin', '\tspin', '-spin', '盐酸', '_spin', '旋', '旋转', ' laba']
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
| 1      | '**'     | -1.100  | 0.332749 | +0.121            |
| 2      | 'The'    | -1.225  | 0.293650 | -0.004            |
| 3      | '8'      | -1.475  | 0.228695 | -0.254            |
| 4      | 'Fact'   | -2.350  | 0.095334 | +0.371            |
| 5      | 'Number' | -4.100  | 0.016567 | -0.004            |
| 6      | '###'    | -4.350  | 0.012902 | -0.129            |
| 7      | '6'      | -5.600  | 0.003697 | +1.371            |
| 8      | 'Eight'  | -6.225  | 0.001979 | +0.621            |
| 9      | '4'      | -6.225  | 0.001979 | -0.879            |
| 10     | '1'      | -6.350  | 0.001746 | -0.004            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
