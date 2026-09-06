---
condition_id: "012_lexical_surface_pair=4_C=1"
axis: "lexical_surface"
value: "pair=4,C=1"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.25118595361709595
p4: 0.0045178839936852455
p8: 0.24666805565357208
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/012_lexical_surface_pair=4_C=1/run.md"
---

# 012_lexical_surface_pair=4_C=1

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
  "strength": 1.0,
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', ' Presents', '\tspin', 'seh']
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
| 1      | 'The'    | -1.150  | 0.316728 | +0.072            |
| 2      | '**'     | -1.150  | 0.316728 | +0.072            |
| 3      | '8'      | -1.400  | 0.246668 | -0.178            |
| 4      | 'Fact'   | -2.650  | 0.070672 | +0.072            |
| 5      | 'Number' | -4.150  | 0.015769 | -0.053            |
| 6      | '###'    | -4.150  | 0.015769 | +0.072            |
| 7      | '4'      | -5.400  | 0.004518 | -0.053            |
| 8      | '1'      | -6.525  | 0.001467 | -0.178            |
| 9      | 'Answer' | -6.900  | 0.001008 | +0.072            |
| 10     | 'Eight'  | -6.900  | 0.001008 | -0.053            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
