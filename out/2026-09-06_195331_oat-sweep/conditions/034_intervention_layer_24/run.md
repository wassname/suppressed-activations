---
condition_id: "034_intervention_layer_24"
axis: "intervention_layer"
value: "24"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9846308827400208
p4: 0.032577481120824814
p8: 0.952053427696228
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.625
log: "conditions/034_intervention_layer_24/run.md"
---

# 034_intervention_layer_24

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
  "intervention_layer": 24,
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
['compan', '友達', ' NHÀ', ' cão', 'amax', '企业相册', 'seh', ' Hunde']
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
| 1      | '8'       | -0.049  | 0.952053 | +0.002            |
| 2      | '4'       | -3.424  | 0.032577 | +0.002            |
| 3      | '6'       | -4.924  | 0.007269 | -0.248            |
| 4      | '<think>' | -5.799  | 0.003030 | +0.002            |
| 5      | '1'       | -6.549  | 0.001431 | +0.002            |
| 6      | 'Eight'   | -7.424  | 0.000597 | -0.123            |
| 7      | '2'       | -7.612  | 0.000495 | +0.065            |
| 8      | '3'       | -7.924  | 0.000362 | +0.002            |
| 9      | '5'       | -8.424  | 0.000220 | +0.002            |
| 10     | '7'       | -8.424  | 0.000220 | -0.060            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
