---
condition_id: "032_intervention_layer_22"
axis: "intervention_layer"
value: "22"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9829446077346802
p4: 0.02881229668855667
p8: 0.9541323184967041
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/032_intervention_layer_22/run.md"
---

# 032_intervention_layer_22

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
  "intervention_layer": 22,
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
[' webView', 'meldung', ' mdi', ' HttpContext', 'SourceType', ' webové', ' prezent', ' niem']
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
| 1      | '8'       | -0.047  | 0.954132 | +0.004            |
| 2      | '4'       | -3.547  | 0.028812 | -0.121            |
| 3      | '6'       | -4.672  | 0.009354 | +0.004            |
| 4      | '<think>' | -5.797  | 0.003037 | +0.004            |
| 5      | '1'       | -6.672  | 0.001266 | -0.121            |
| 6      | 'Eight'   | -7.484  | 0.000562 | -0.183            |
| 7      | '2'       | -7.797  | 0.000411 | -0.121            |
| 8      | '3'       | -8.047  | 0.000320 | -0.121            |
| 9      | '7'       | -8.422  | 0.000220 | -0.058            |
| 10     | '0'       | -8.547  | 0.000194 | -0.058            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
