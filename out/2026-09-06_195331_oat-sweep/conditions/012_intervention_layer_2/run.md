---
condition_id: "012_intervention_layer_2"
axis: "intervention_layer"
value: "2"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.7768412828445435
p4: 0.04148590937256813
p8: 0.7353553771972656
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/012_intervention_layer_2/run.md"
---

# 012_intervention_layer_2

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
  "intervention_layer": 2,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' Ponadto', '.ToolStripMenuItem', '张掖', 'må', '卫国', '的场所', ' Ufficio', ' medarbe']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.307  | 0.735355 | -0.256            |
| 2      | '6'       | -1.807  | 0.164080 | +2.869            |
| 3      | '4'       | -3.182  | 0.041486 | +0.244            |
| 4      | '1'       | -3.432  | 0.032309 | +3.119            |
| 5      | '2'       | -4.307  | 0.013469 | +3.369            |
| 6      | '<think>' | -5.807  | 0.003005 | -0.006            |
| 7      | '3'       | -5.807  | 0.003005 | +2.119            |
| 8      | '0'       | -6.182  | 0.002065 | +2.306            |
| 9      | '5'       | -6.307  | 0.001823 | +2.119            |
| 10     | '7'       | -7.495  | 0.000556 | +0.869            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
