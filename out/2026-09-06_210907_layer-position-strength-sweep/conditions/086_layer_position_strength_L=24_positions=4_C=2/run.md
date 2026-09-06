---
condition_id: "086_layer_position_strength_L=24_positions=4_C=2"
axis: "layer_position_strength"
value: "L=24,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29696011543273926
p4: 0.00472356379032135
p8: 0.2922365367412567
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/086_layer_position_strength_L=24_positions=4_C=2/run.md"
---

# 086_layer_position_strength_L=24_positions=4_C=2

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
  "intervention_layer": 24,
  "intervention_positions": 4,
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
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
['compan', ' Ủy', '友達', ' NHÀ', ' собаки', ' Galler', ' собака', 'kab']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 51.78230285644531,
    "perturbation_norm": 11.081626892089844,
    "relative_perturbation_by_position": [
      0.33927828073501587,
      0.22908633947372437,
      0.0837673544883728,
      0.1260589361190796
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.230  | 0.292237 | -0.009            |
| 2      | 'The'    | -1.230  | 0.292237 | -0.009            |
| 3      | '**'     | -1.230  | 0.292237 | -0.009            |
| 4      | 'Fact'   | -2.605  | 0.073889 | +0.116            |
| 5      | 'Number' | -4.105  | 0.016487 | -0.009            |
| 6      | '###'    | -4.230  | 0.014550 | -0.009            |
| 7      | '4'      | -5.355  | 0.004724 | -0.009            |
| 8      | '1'      | -6.355  | 0.001738 | -0.009            |
| 9      | 'Answer' | -6.855  | 0.001054 | +0.116            |
| 10     | 'Eight'  | -6.855  | 0.001054 | -0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
