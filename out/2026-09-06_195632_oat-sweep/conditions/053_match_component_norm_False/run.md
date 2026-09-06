---
condition_id: "053_match_component_norm_False"
axis: "match_component_norm"
value: "False"
is_default: false
swap_log_odds_shift: 0.6875
valid_answer_mass: 0.0004911756841465831
p4: 1.8784933217830257e-06
p8: 0.0004892972065135837
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/053_match_component_norm_False/run.md"
---

# 053_match_component_norm_False

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
  "match_component_norm": false,
  "restore_residual_norm": true,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['-web', 'mmm', '长腿', 'web', 'Mbps', '(web', '盐酸', '闸蟹']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **eight legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.123  | 0.884670 | -0.026            |
| 2      | 'Based'  | -2.498  | 0.082287 | +0.224            |
| 3      | 'To'     | -5.248  | 0.005260 | +0.474            |
| 4      | 'Sp'     | -5.248  | 0.005260 | +0.349            |
| 5      | 'There'  | -5.748  | 0.003191 | +1.349            |
| 6      | '**'     | -5.998  | 0.002485 | +0.224            |
| 7      | 'An'     | -5.998  | 0.002485 | +0.099            |
| 8      | 'First'  | -6.373  | 0.001708 | +0.849            |
| 9      | 'That'   | -6.623  | 0.001330 | +0.974            |
| 10     | 'Spider' | -6.623  | 0.001330 | +1.099            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
