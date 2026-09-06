---
condition_id: "007_readout_positions_2"
axis: "readout_positions"
value: "2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.9785304665565491
p4: 0.03652549162507057
p8: 0.9420049786567688
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/007_readout_positions_2/run.md"
---

# 007_readout_positions_2

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 2,
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
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['丰台区', 'Agama', '_watch', ' latihan', ' опти', '文化传媒有限公司', ' рекоменда', ' Vader']
```

Unmodified donor readout:

```python
['gos', ' законода', '豆角', 'ツール', ' brak', '呼吸道感染', ' Kepolisian', 'Force']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.060  | 0.942005 | -0.008            |
| 2      | '4'       | -3.310  | 0.036525 | +0.117            |
| 3      | '6'       | -4.310  | 0.013437 | +0.367            |
| 4      | '<think>' | -5.810  | 0.002998 | -0.008            |
| 5      | '1'       | -6.435  | 0.001605 | +0.117            |
| 6      | '2'       | -7.560  | 0.000521 | +0.117            |
| 7      | '3'       | -7.685  | 0.000460 | +0.242            |
| 8      | 'Eight'   | -7.872  | 0.000381 | -0.571            |
| 9      | '7'       | -8.185  | 0.000279 | +0.179            |
| 10     | '5'       | -8.247  | 0.000262 | +0.179            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
