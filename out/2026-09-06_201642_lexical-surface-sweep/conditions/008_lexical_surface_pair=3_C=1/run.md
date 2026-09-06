---
condition_id: "008_lexical_surface_pair=3_C=1"
axis: "lexical_surface"
value: "pair=3,C=1"
is_default: false
swap_log_odds_shift: 0.1250002384185791
valid_answer_mass: 0.2972773611545563
p4: 0.005346894729882479
p8: 0.2919304668903351
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/008_lexical_surface_pair=3_C=1/run.md"
---

# 008_lexical_surface_pair=3_C=1

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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', ' Presents', 'seh', '\tspin']
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
| 1      | '8'      | -1.231  | 0.291930 | -0.010            |
| 2      | 'The'    | -1.231  | 0.291930 | -0.010            |
| 3      | '**'     | -1.231  | 0.291930 | -0.010            |
| 4      | 'Fact'   | -2.606  | 0.073812 | +0.115            |
| 5      | 'Number' | -4.106  | 0.016470 | -0.010            |
| 6      | '###'    | -4.231  | 0.014534 | -0.010            |
| 7      | '4'      | -5.231  | 0.005347 | +0.115            |
| 8      | '1'      | -6.356  | 0.001736 | -0.010            |
| 9      | '6'      | -6.856  | 0.001053 | +0.115            |
| 10     | 'Answer' | -6.856  | 0.001053 | +0.115            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
