---
condition_id: "002_detector_layers_(8,_16,_24)"
axis: "detector_layers"
value: "(8, 16, 24)"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.3166029155254364
p4: 0.0064372834749519825
p8: 0.3101656436920166
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.125
log: "conditions/002_detector_layers_(8,_16,_24)/run.md"
---

# 002_detector_layers_(8,_16,_24)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    8,
    16,
    24
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
[' relevant', ' gioia', ' category', '_ME', ' relevance', ' thyroid', ' filter', ' (']
```

Unmodified donor readout:

```python
[' (', ' seminal', '(', ' um', ' inter', ' $', ' [', ',']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.171  | 0.310166 | +0.051            |
| 2      | 'The'    | -1.296  | 0.273720 | -0.074            |
| 3      | '**'     | -1.421  | 0.241557 | -0.199            |
| 4      | 'Fact'   | -2.171  | 0.114104 | +0.551            |
| 5      | 'Number' | -3.546  | 0.028850 | +0.551            |
| 6      | '4'      | -5.046  | 0.006437 | +0.301            |
| 7      | '###'    | -5.046  | 0.006437 | -0.824            |
| 8      | 'Answer' | -6.046  | 0.002368 | +0.926            |
| 9      | 'Eight'  | -6.171  | 0.002090 | +0.676            |
| 10     | '1'      | -6.296  | 0.001844 | +0.051            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
