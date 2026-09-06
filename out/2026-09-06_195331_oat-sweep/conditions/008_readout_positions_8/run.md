---
condition_id: "008_readout_positions_8"
axis: "readout_positions"
value: "8"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.9294071197509766
p4: 0.03911663219332695
p8: 0.8902904987335205
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/008_readout_positions_8/run.md"
---

# 008_readout_positions_8

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 8,
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
[' того', 'FullScreen', 'vă', 'flug', ' rozwoju', ' principalTable', ' القرآن', ' заслу']
```

Unmodified donor readout:

```python
['吠', ' Dogs', '_man', 'MAN', 'compan', '.getS', 'Overlay', 'Manchester']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.116  | 0.890290 | -0.065            |
| 2      | '6'       | -3.241  | 0.039117 | +1.435            |
| 3      | '4'       | -3.241  | 0.039117 | +0.185            |
| 4      | '1'       | -4.366  | 0.012699 | +2.185            |
| 5      | '2'       | -5.616  | 0.003638 | +2.060            |
| 6      | '<think>' | -5.866  | 0.002834 | -0.065            |
| 7      | 'Eight'   | -5.991  | 0.002501 | +1.310            |
| 8      | '3'       | -6.116  | 0.002207 | +1.810            |
| 9      | '0'       | -6.616  | 0.001338 | +1.873            |
| 10     | '5'       | -6.741  | 0.001181 | +1.685            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
