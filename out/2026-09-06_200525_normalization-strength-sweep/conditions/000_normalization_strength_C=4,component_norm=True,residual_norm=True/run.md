---
condition_id: "000_normalization_strength_C=4,component_norm=True,residual_norm=True"
axis: "normalization_strength"
value: "C=4,component_norm=True,residual_norm=True"
is_default: false
swap_log_odds_shift: 1.75
valid_answer_mass: 0.09364114701747894
p4: 0.007968772202730179
p8: 0.08567237108945847
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/000_normalization_strength_C=4,component_norm=True,residual_norm=True/run.md"
---

# 000_normalization_strength_C=4,component_norm=True,residual_norm=True

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
[' responseData', 'χω', 'ISA', ' Hauses', '什么都没有', ' begeist', 'Agama', '的场所']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.832  | 0.435080 | +0.389            |
| 2      | 'The'    | -1.332  | 0.263889 | -0.111            |
| 3      | 'Fact'   | -2.207  | 0.110006 | +0.514            |
| 4      | '8'      | -2.457  | 0.085672 | -1.236            |
| 5      | '6'      | -3.457  | 0.031517 | +3.514            |
| 6      | '###'    | -4.082  | 0.016870 | +0.139            |
| 7      | 'Number' | -4.082  | 0.016870 | +0.014            |
| 8      | '1'      | -4.582  | 0.010232 | +1.764            |
| 9      | '4'      | -4.832  | 0.007969 | +0.514            |
| 10     | '2'      | -5.582  | 0.003764 | +2.139            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
