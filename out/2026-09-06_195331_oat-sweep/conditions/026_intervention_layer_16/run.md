---
condition_id: "026_intervention_layer_16"
axis: "intervention_layer"
value: "16"
is_default: false
swap_log_odds_shift: -0.5
valid_answer_mass: 0.9778340458869934
p4: 0.019881663843989372
p8: 0.9579523801803589
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/026_intervention_layer_16/run.md"
---

# 026_intervention_layer_16

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
  "intervention_layer": 16,
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
['\tspin', ' Presents', 'ปั่น', 'kab', 'สปิน', 'meldung', 'Spin', '哈密']
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
| 1      | '8'       | -0.043  | 0.957952 | +0.008            |
| 2      | '4'       | -3.918  | 0.019882 | -0.492            |
| 3      | '6'       | -4.168  | 0.015484 | +0.508            |
| 4      | '<think>' | -6.043  | 0.002375 | -0.242            |
| 5      | '1'       | -6.918  | 0.000990 | -0.367            |
| 6      | 'Eight'   | -7.293  | 0.000680 | +0.008            |
| 7      | '2'       | -7.918  | 0.000364 | -0.242            |
| 8      | '3'       | -8.355  | 0.000235 | -0.429            |
| 9      | '7'       | -8.543  | 0.000195 | -0.179            |
| 10     | '5'       | -8.605  | 0.000183 | -0.179            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
