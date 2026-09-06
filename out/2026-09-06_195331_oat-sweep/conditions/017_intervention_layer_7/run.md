---
condition_id: "017_intervention_layer_7"
axis: "intervention_layer"
value: "7"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9684020280838013
p4: 0.03204052522778511
p8: 0.9363614916801453
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/017_intervention_layer_7/run.md"
---

# 017_intervention_layer_7

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
  "intervention_layer": 7,
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
['ปั่น', '원', 'Spin', ' Ủy', ' laba', '呜', 'seh', '哈密']
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
| 1      | '8'       | -0.066  | 0.936361 | -0.014            |
| 2      | '4'       | -3.441  | 0.032041 | -0.014            |
| 3      | '6'       | -3.941  | 0.019434 | +0.736            |
| 4      | '<think>' | -5.691  | 0.003377 | +0.111            |
| 5      | '1'       | -5.691  | 0.003377 | +0.861            |
| 6      | '2'       | -6.691  | 0.001242 | +0.986            |
| 7      | '3'       | -7.316  | 0.000665 | +0.611            |
| 8      | 'Eight'   | -7.441  | 0.000587 | -0.139            |
| 9      | '5'       | -7.753  | 0.000429 | +0.673            |
| 10     | '7'       | -7.878  | 0.000379 | +0.486            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
