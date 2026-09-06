---
condition_id: "000_default_default"
axis: "default"
value: "default"
is_default: true
swap_log_odds_shift: 2.0
valid_answer_mass: 0.6204516887664795
p4: 0.12521536648273468
p8: 0.4952363073825836
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/000_default_default/run.md"
---

# 000_default_default

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
[' Ponadto', '政法大学', 'اطر', '베이스', 'NEG', 'esos', ' responseData', 'ツール']
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
| 1      | '8'       | -0.703  | 0.495236 | -0.651            |
| 2      | '6'       | -1.328  | 0.265081 | +3.349            |
| 3      | '4'       | -2.078  | 0.125215 | +1.349            |
| 4      | '1'       | -2.953  | 0.052198 | +3.599            |
| 5      | '2'       | -3.328  | 0.035875 | +4.349            |
| 6      | '3'       | -4.703  | 0.009071 | +3.224            |
| 7      | '0'       | -5.703  | 0.003337 | +2.786            |
| 8      | '<think>' | -5.703  | 0.003337 | +0.099            |
| 9      | '5'       | -5.703  | 0.003337 | +2.724            |
| 10     | '7'       | -6.953  | 0.000956 | +1.411            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
