---
condition_id: "017_lexical_surface_pair=5_C=2"
axis: "lexical_surface"
value: "pair=5,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2757105529308319
p4: 0.004958986770361662
p8: 0.27075156569480896
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/017_lexical_surface_pair=5_C=2/run.md"
---

# 017_lexical_surface_pair=5_C=2

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
  "lexical_forms": "pair_5",
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', ' Presents', 'seh', '\tspin']
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
| 1      | 'The'    | -1.182  | 0.306802 | +0.040            |
| 2      | '**'     | -1.182  | 0.306802 | +0.040            |
| 3      | '8'      | -1.307  | 0.270752 | -0.085            |
| 4      | 'Fact'   | -2.682  | 0.068457 | +0.040            |
| 5      | 'Number' | -4.182  | 0.015275 | -0.085            |
| 6      | '###'    | -4.307  | 0.013480 | -0.085            |
| 7      | '4'      | -5.307  | 0.004959 | +0.040            |
| 8      | '1'      | -6.307  | 0.001824 | +0.040            |
| 9      | '6'      | -6.932  | 0.000976 | +0.040            |
| 10     | 'Answer' | -6.932  | 0.000976 | +0.040            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
