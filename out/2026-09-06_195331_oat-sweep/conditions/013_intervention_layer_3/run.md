---
condition_id: "013_intervention_layer_3"
axis: "intervention_layer"
value: "3"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.8944405913352966
p4: 0.03764497488737106
p8: 0.856795608997345
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/013_intervention_layer_3/run.md"
---

# 013_intervention_layer_3

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
  "intervention_layer": 3,
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
[' laba', ' medarbe', 'seh', ' Ponadto', ' ОГ', '_keeper', 'må', 'くださ']
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
| 1      | '8'       | -0.155  | 0.856796 | -0.103            |
| 2      | '1'       | -3.030  | 0.048337 | +3.522            |
| 3      | '4'       | -3.280  | 0.037645 | +0.147            |
| 4      | '6'       | -3.280  | 0.037645 | +1.397            |
| 5      | '2'       | -5.155  | 0.005773 | +2.522            |
| 6      | '0'       | -5.655  | 0.003502 | +2.834            |
| 7      | '3'       | -6.030  | 0.002407 | +1.897            |
| 8      | '5'       | -6.280  | 0.001874 | +2.147            |
| 9      | '<think>' | -6.655  | 0.001288 | -0.853            |
| 10     | 'Eight'   | -6.780  | 0.001137 | +0.522            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
