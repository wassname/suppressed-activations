---
condition_id: "036_lexical_surface_union_C=1_divide=4"
axis: "lexical_surface"
value: "union,C=1,divide=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3005337715148926
p4: 0.005405464209616184
p8: 0.29512831568717957
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/036_lexical_surface_union_C=1_divide=4/run.md"
---

# 036_lexical_surface_union_C=1_divide=4

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
  "strength": 0.25,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "union",
  "lexical_divisor": 4
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
['-spin', 'ปั่น', 'Spin', ' Ủy', ' Presents', ' Spin', 'seh', '\tspin']
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
| 1      | '8'      | -1.220  | 0.295128 | +0.001            |
| 2      | 'The'    | -1.220  | 0.295128 | +0.001            |
| 3      | '**'     | -1.220  | 0.295128 | +0.001            |
| 4      | 'Fact'   | -2.720  | 0.065852 | +0.001            |
| 5      | 'Number' | -4.095  | 0.016650 | +0.001            |
| 6      | '###'    | -4.345  | 0.012967 | -0.124            |
| 7      | '4'      | -5.220  | 0.005405 | +0.126            |
| 8      | '1'      | -6.345  | 0.001755 | +0.001            |
| 9      | 'Answer' | -6.845  | 0.001064 | +0.126            |
| 10     | 'Eight'  | -6.845  | 0.001064 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
