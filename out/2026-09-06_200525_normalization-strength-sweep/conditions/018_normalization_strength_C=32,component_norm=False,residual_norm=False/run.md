---
condition_id: "018_normalization_strength_C=32,component_norm=False,residual_norm=False"
axis: "normalization_strength"
value: "C=32,component_norm=False,residual_norm=False"
is_default: false
swap_log_odds_shift: 5.499999523162842
valid_answer_mass: 0.000500760565046221
p4: 0.0003997004241682589
p8: 0.00010106014087796211
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/018_normalization_strength_C=32,component_norm=False,residual_norm=False/run.md"
---

# 018_normalization_strength_C=32,component_norm=False,residual_norm=False

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
  "strength": 32.0,
  "match_component_norm": false,
  "restore_residual_norm": false,
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
[' WAR', 'World', '副院长', ' Española', ' масс', 'WAY', ' methodName', 'ônia']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The correct sentence is:

**"The number of facts is one."**

Here is the breakdown of why the other options are incorrect:

1.
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'Let'   | -1.575  | 0.207050 | +10.709           |
| 2      | 'The'   | -1.575  | 0.207050 | -0.353            |
| 3      | 'It'    | -2.075  | 0.125582 | +8.647            |
| 4      | 'To'    | -2.325  | 0.097803 | +7.647            |
| 5      | 'Here'  | -2.575  | 0.076169 | +7.147            |
| 6      | 'This'  | -3.075  | 0.046199 | +6.959            |
| 7      | 'Based' | -3.075  | 0.046199 | +5.584            |
| 8      | 'Your'  | -3.575  | 0.028021 | +8.897            |
| 9      | 'There' | -3.575  | 0.028021 | +5.022            |
| 10     | 'You'   | -3.575  | 0.028021 | +8.272            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
