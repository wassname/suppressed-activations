---
condition_id: "024_lexical_surface_pair=7_C=1"
axis: "lexical_surface"
value: "pair=7,C=1"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2973612844944
p4: 0.0053484016098082066
p8: 0.29201287031173706
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/024_lexical_surface_pair=7_C=1/run.md"
---

# 024_lexical_surface_pair=7_C=1

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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', '\tspin']
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
| 1      | '8'      | -1.231  | 0.292013 | -0.009            |
| 2      | 'The'    | -1.231  | 0.292013 | -0.009            |
| 3      | '**'     | -1.231  | 0.292013 | -0.009            |
| 4      | 'Fact'   | -2.606  | 0.073832 | +0.116            |
| 5      | 'Number' | -4.106  | 0.016474 | -0.009            |
| 6      | '###'    | -4.231  | 0.014538 | -0.009            |
| 7      | '4'      | -5.231  | 0.005348 | +0.116            |
| 8      | '1'      | -6.356  | 0.001736 | -0.009            |
| 9      | 'Answer' | -6.856  | 0.001053 | +0.116            |
| 10     | 'Eight'  | -6.856  | 0.001053 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
