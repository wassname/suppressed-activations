---
condition_id: "011_lexical_surface_pair=3_C=8"
axis: "lexical_surface"
value: "pair=3,C=8"
is_default: false
swap_log_odds_shift: 2.749999761581421
valid_answer_mass: 0.08734194934368134
p4: 0.01762675680220127
p8: 0.06971519440412521
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/011_lexical_surface_pair=3_C=8/run.md"
---

# 011_lexical_surface_pair=3_C=8

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
  "lexical_forms": "pair_3",
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
['\tspin', 'Spin', '-spin', 'spin', '_spin', '旋', ' Rotation', ' rotate']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is a **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.913  | 0.401183 | +0.308            |
| 2      | '**'     | -1.288  | 0.275729 | -0.067            |
| 3      | 'Fact'   | -2.163  | 0.114941 | +0.558            |
| 4      | '8'      | -2.663  | 0.069715 | -1.442            |
| 5      | '6'      | -2.913  | 0.054294 | +4.058            |
| 6      | 'Number' | -4.038  | 0.017627 | +0.058            |
| 7      | '4'      | -4.038  | 0.017627 | +1.308            |
| 8      | '###'    | -4.538  | 0.010691 | -0.317            |
| 9      | '1'      | -4.663  | 0.009435 | +1.683            |
| 10     | '2'      | -5.413  | 0.004457 | +2.308            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
