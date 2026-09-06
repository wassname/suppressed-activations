---
condition_id: "014_normalization_strength_C=64,component_norm=False,residual_norm=True"
axis: "normalization_strength"
value: "C=64,component_norm=False,residual_norm=True"
is_default: false
swap_log_odds_shift: 3.5
valid_answer_mass: 9.706505079520866e-05
p4: 3.384125739103183e-05
p8: 6.322379340417683e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "It"
readout_overlap: 0.0
log: "conditions/014_normalization_strength_C=64,component_norm=False,residual_norm=True/run.md"
---

# 014_normalization_strength_C=64,component_norm=False,residual_norm=True

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
  "strength": 64.0,
  "match_component_norm": false,
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
['谈谈', 'ška', '两周内', ' posting', ' frameworks', 'ConverterFactory', ' posts', ' Posts']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
It looks like you've pasted a string of repeated and mixed variations of the word **"than"** (with different spacing, case, and formatting). Here's
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'It'      | -0.544  | 0.580521 | +10.178           |
| 2      | 'The'     | -2.169  | 0.114311 | -0.947            |
| 3      | 'This'    | -2.419  | 0.089026 | +7.615            |
| 4      | 'Your'    | -2.544  | 0.078565 | +9.928            |
| 5      | 'Looking' | -3.919  | 0.019864 | +9.615            |
| 6      | 'You'     | -4.106  | 0.016468 | +7.740            |
| 7      | '`'       | -4.356  | 0.012825 | +7.615            |
| 8      | 'Hello'   | -4.606  | 0.009988 | +10.490           |
| 9      | 'That'    | -4.669  | 0.009383 | +6.865            |
| 10     | 'Looks'   | -5.106  | 0.006058 | +11.396           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
