---
condition_id: "028_intervention_layer_18"
axis: "intervention_layer"
value: "18"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.9809430241584778
p4: 0.022539490833878517
p8: 0.9584035277366638
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/028_intervention_layer_18/run.md"
---

# 028_intervention_layer_18

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
  "intervention_layer": 18,
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
['\tspin', ' Presents', 'สปิน', 'ปั่น', 'kab', 'seh', ' niem', 'meldung']
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
| 1      | '8'       | -0.042  | 0.958404 | +0.009            |
| 2      | '4'       | -3.792  | 0.022539 | -0.366            |
| 3      | '6'       | -4.417  | 0.012065 | +0.259            |
| 4      | '<think>' | -6.042  | 0.002376 | -0.241            |
| 5      | '1'       | -6.667  | 0.001272 | -0.116            |
| 6      | 'Eight'   | -7.417  | 0.000601 | -0.116            |
| 7      | '2'       | -7.730  | 0.000439 | -0.054            |
| 8      | '3'       | -8.105  | 0.000302 | -0.179            |
| 9      | '5'       | -8.355  | 0.000235 | +0.071            |
| 10     | '7'       | -8.480  | 0.000208 | -0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
