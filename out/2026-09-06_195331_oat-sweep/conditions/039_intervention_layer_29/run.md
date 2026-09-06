---
condition_id: "039_intervention_layer_29"
axis: "intervention_layer"
value: "29"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9834564924240112
p4: 0.03253862261772156
p8: 0.9509178996086121
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/039_intervention_layer_29/run.md"
---

# 039_intervention_layer_29

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
  "intervention_layer": 29,
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
[' spinning', ' spin', ' spins', '.Sp', '\tsp', '纺', 'ปั่น', ' spun']
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
| 1      | '8'       | -0.050  | 0.950918 | +0.001            |
| 2      | '4'       | -3.425  | 0.032539 | +0.001            |
| 3      | '6'       | -4.800  | 0.008227 | -0.124            |
| 4      | '<think>' | -5.800  | 0.003027 | +0.001            |
| 5      | '1'       | -6.550  | 0.001430 | +0.001            |
| 6      | 'Eight'   | -7.175  | 0.000765 | +0.126            |
| 7      | '2'       | -7.613  | 0.000494 | +0.063            |
| 8      | '3'       | -7.925  | 0.000361 | +0.001            |
| 9      | '5'       | -8.425  | 0.000219 | +0.001            |
| 10     | '7'       | -8.425  | 0.000219 | -0.062            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
