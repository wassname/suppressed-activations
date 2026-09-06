---
condition_id: "035_intervention_layer_25"
axis: "intervention_layer"
value: "25"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9837353229522705
p4: 0.03254784643650055
p8: 0.9511874914169312
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/035_intervention_layer_25/run.md"
---

# 035_intervention_layer_25

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
  "intervention_layer": 25,
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
[' spinning', 'web', ' spin', ' spins', ' Ủy', '.Sp', '纺', 'ปั่น']
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
| 1      | '8'       | -0.050  | 0.951187 | +0.001            |
| 2      | '4'       | -3.425  | 0.032548 | +0.001            |
| 3      | '6'       | -4.800  | 0.008229 | -0.124            |
| 4      | '<think>' | -5.800  | 0.003027 | +0.001            |
| 5      | '1'       | -6.675  | 0.001262 | -0.124            |
| 6      | 'Eight'   | -7.300  | 0.000676 | +0.001            |
| 7      | '2'       | -7.613  | 0.000494 | +0.064            |
| 8      | '3'       | -7.925  | 0.000362 | +0.001            |
| 9      | '5'       | -8.425  | 0.000219 | +0.001            |
| 10     | '7'       | -8.425  | 0.000219 | -0.061            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
