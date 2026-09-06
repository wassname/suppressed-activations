---
condition_id: "025_lexical_surface_pair=7_C=2"
axis: "lexical_surface"
value: "pair=7,C=2"
is_default: false
swap_log_odds_shift: 0.1250002384185791
valid_answer_mass: 0.27197515964508057
p4: 0.004891803488135338
p8: 0.2670833468437195
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/025_lexical_surface_pair=7_C=2/run.md"
---

# 025_lexical_surface_pair=7_C=2

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
  "lexical_forms": "pair_7",
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
| 1      | 'The'    | -1.195  | 0.302645 | +0.026            |
| 2      | '**'     | -1.195  | 0.302645 | +0.026            |
| 3      | '8'      | -1.320  | 0.267083 | -0.099            |
| 4      | 'Fact'   | -2.570  | 0.076521 | +0.151            |
| 5      | 'Number' | -4.070  | 0.017074 | +0.026            |
| 6      | '###'    | -4.195  | 0.015068 | +0.026            |
| 7      | '4'      | -5.320  | 0.004892 | +0.026            |
| 8      | '1'      | -6.320  | 0.001800 | +0.026            |
| 9      | 'Answer' | -6.820  | 0.001092 | +0.151            |
| 10     | 'Eight'  | -6.820  | 0.001092 | +0.026            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
