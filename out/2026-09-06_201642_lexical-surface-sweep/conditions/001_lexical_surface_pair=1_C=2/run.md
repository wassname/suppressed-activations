---
condition_id: "001_lexical_surface_pair=1_C=2"
axis: "lexical_surface"
value: "pair=1,C=2"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.2729189395904541
p4: 0.0062709590420126915
p8: 0.26664799451828003
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/001_lexical_surface_pair=1_C=2/run.md"
---

# 001_lexical_surface_pair=1_C=2

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
  "donor_position_offset": 0,
  "lexical_forms": "pair_1",
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
['-spin', 'ปั่น', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', '\tspin']
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
| 1      | 'The'    | -1.197  | 0.302152 | +0.025            |
| 2      | '**'     | -1.197  | 0.302152 | +0.025            |
| 3      | '8'      | -1.322  | 0.266648 | -0.100            |
| 4      | 'Fact'   | -2.572  | 0.076396 | +0.150            |
| 5      | 'Number' | -4.072  | 0.017046 | +0.025            |
| 6      | '###'    | -4.197  | 0.015043 | +0.025            |
| 7      | '4'      | -5.072  | 0.006271 | +0.275            |
| 8      | '1'      | -6.322  | 0.001797 | +0.025            |
| 9      | 'Answer' | -6.822  | 0.001090 | +0.150            |
| 10     | 'Eight'  | -6.822  | 0.001090 | +0.025            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
