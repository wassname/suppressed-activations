---
condition_id: "007_lexical_surface_pair=2_C=8"
axis: "lexical_surface"
value: "pair=2,C=8"
is_default: false
swap_log_odds_shift: 1.000000238418579
valid_answer_mass: 0.08076127618551254
p4: 0.003399059409275651
p8: 0.07736221700906754
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/007_lexical_surface_pair=2_C=8/run.md"
---

# 007_lexical_surface_pair=2_C=8

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
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_2",
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
['Spin', '-spin', 'spin', '\tspin', '_spin', ' Spin', ' Presents', 'seh']
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
| 1      | '**'     | -1.059  | 0.346713 | +0.162            |
| 2      | 'The'    | -1.059  | 0.346713 | +0.162            |
| 3      | 'Fact'   | -1.934  | 0.144532 | +0.787            |
| 4      | '8'      | -2.559  | 0.077362 | -1.338            |
| 5      | '###'    | -3.684  | 0.025116 | +0.537            |
| 6      | '6'      | -3.934  | 0.019560 | +3.037            |
| 7      | 'Number' | -4.059  | 0.017262 | +0.037            |
| 8      | '1'      | -5.309  | 0.004946 | +1.037            |
| 9      | '4'      | -5.684  | 0.003399 | -0.338            |
| 10     | '2'      | -6.809  | 0.001104 | +0.912            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
