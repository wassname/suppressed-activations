---
condition_id: "054_restore_residual_norm_False"
axis: "restore_residual_norm"
value: "False"
is_default: false
swap_log_odds_shift: 2.625
valid_answer_mass: 0.06197747960686684
p4: 0.011306273750960827
p8: 0.050671204924583435
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/054_restore_residual_norm_False/run.md"
---

# 054_restore_residual_norm_False

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
['ISA', ' responseData', 'ácia', '这个东西', 'χω', ' dimostr', 'NEG', 'Agama']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.857  | 0.424265 | +0.364            |
| 2      | 'The'    | -1.232  | 0.291593 | -0.011            |
| 3      | 'Fact'   | -2.232  | 0.107271 | +0.489            |
| 4      | '8'      | -2.982  | 0.050671 | -1.761            |
| 5      | '6'      | -3.357  | 0.034826 | +3.614            |
| 6      | '###'    | -3.857  | 0.021123 | +0.364            |
| 7      | 'Number' | -3.857  | 0.021123 | +0.239            |
| 8      | '4'      | -4.482  | 0.011306 | +0.864            |
| 9      | '1'      | -4.607  | 0.009978 | +1.739            |
| 10     | '2'      | -5.232  | 0.005341 | +2.489            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
