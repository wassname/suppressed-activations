---
condition_id: "024_intervention_layer_14"
axis: "intervention_layer"
value: "14"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.9308477640151978
p4: 0.039177268743515015
p8: 0.8916705250740051
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/024_intervention_layer_14/run.md"
---

# 024_intervention_layer_14

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
  "intervention_layer": 14,
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
[' Presents', '\tspin', 'ปั่น', '领头羊', 'meldung', ' laba', 'ಲು', '哈密']
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
| 1      | '8'       | -0.115  | 0.891671 | -0.063            |
| 2      | '6'       | -2.865  | 0.057003 | +1.812            |
| 3      | '4'       | -3.240  | 0.039177 | +0.187            |
| 4      | '<think>' | -5.740  | 0.003216 | +0.062            |
| 5      | '1'       | -5.990  | 0.002505 | +0.562            |
| 6      | 'Eight'   | -6.740  | 0.001183 | +0.562            |
| 7      | '2'       | -6.990  | 0.000921 | +0.687            |
| 8      | '3'       | -7.427  | 0.000595 | +0.499            |
| 9      | '5'       | -7.802  | 0.000409 | +0.624            |
| 10     | '7'       | -8.052  | 0.000318 | +0.312            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
