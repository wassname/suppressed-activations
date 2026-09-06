---
condition_id: "031_intervention_layer_21"
axis: "intervention_layer"
value: "21"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.983420729637146
p4: 0.02882625348865986
p8: 0.9545944929122925
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/031_intervention_layer_21/run.md"
---

# 031_intervention_layer_21

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
  "intervention_layer": 21,
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
[' webView', ' HttpContext', 'må', ' веб', ' webové', ' pathMatch', ' niem', ' fär']
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
| 1      | '8'       | -0.046  | 0.954594 | +0.005            |
| 2      | '4'       | -3.546  | 0.028826 | -0.120            |
| 3      | '6'       | -4.796  | 0.008259 | -0.120            |
| 4      | '<think>' | -5.671  | 0.003443 | +0.130            |
| 5      | '1'       | -6.671  | 0.001267 | -0.120            |
| 6      | 'Eight'   | -7.296  | 0.000678 | +0.005            |
| 7      | '2'       | -7.734  | 0.000438 | -0.058            |
| 8      | '3'       | -8.046  | 0.000320 | -0.120            |
| 9      | '7'       | -8.421  | 0.000220 | -0.058            |
| 10     | '5'       | -8.484  | 0.000207 | -0.058            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
