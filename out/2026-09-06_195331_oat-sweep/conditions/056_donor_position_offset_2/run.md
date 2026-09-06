---
condition_id: "056_donor_position_offset_2"
axis: "donor_position_offset"
value: "2"
is_default: false
swap_log_odds_shift: 1.875
valid_answer_mass: 0.6649447679519653
p4: 0.12130288779735565
p8: 0.5436418652534485
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/056_donor_position_offset_2/run.md"
---

# 056_donor_position_offset_2

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
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 2
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
[' Bốn', '晶圆', 'くださ', ' Ponadto', 'esos', '誇る', '张掖', '犹太人']
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
| 1      | '8'       | -0.609  | 0.543642 | -0.558            |
| 2      | '6'       | -1.359  | 0.256798 | +3.317            |
| 3      | '4'       | -2.109  | 0.121303 | +1.317            |
| 4      | '1'       | -3.359  | 0.034754 | +3.192            |
| 5      | '2'       | -3.859  | 0.021079 | +3.817            |
| 6      | '3'       | -5.234  | 0.005330 | +2.692            |
| 7      | '0'       | -5.359  | 0.004703 | +3.129            |
| 8      | '5'       | -5.734  | 0.003233 | +2.692            |
| 9      | '<think>' | -5.859  | 0.002853 | -0.058            |
| 10     | '7'       | -6.859  | 0.001049 | +1.504            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
