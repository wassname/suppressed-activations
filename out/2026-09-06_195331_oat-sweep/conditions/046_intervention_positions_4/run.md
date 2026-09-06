---
condition_id: "046_intervention_positions_4"
axis: "intervention_positions"
value: "4"
is_default: false
swap_log_odds_shift: 1.75
valid_answer_mass: 0.6390124559402466
p4: 0.10512807965278625
p8: 0.5338844060897827
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/046_intervention_positions_4/run.md"
---

# 046_intervention_positions_4

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
  "intervention_positions": 4,
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
[' Ponadto', '的场所', ' responseData', ' Satgas', 'اطر', '政法大学', 'χω', 'esos']
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
| 1      | '8'       | -0.628  | 0.533884 | -0.576            |
| 2      | '6'       | -1.253  | 0.285768 | +3.424            |
| 3      | '4'       | -2.253  | 0.105128 | +1.174            |
| 4      | '1'       | -3.378  | 0.034130 | +3.174            |
| 5      | '2'       | -3.878  | 0.020701 | +3.799            |
| 6      | '3'       | -5.003  | 0.006721 | +2.924            |
| 7      | '0'       | -5.753  | 0.003175 | +2.736            |
| 8      | '5'       | -5.878  | 0.002802 | +2.549            |
| 9      | '<think>' | -6.003  | 0.002472 | -0.201            |
| 10     | '7'       | -6.878  | 0.001031 | +1.486            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
