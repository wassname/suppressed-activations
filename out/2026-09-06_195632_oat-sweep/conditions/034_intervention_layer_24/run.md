---
condition_id: "034_intervention_layer_24"
axis: "intervention_layer"
value: "24"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.0006502438918687403
p4: 1.2528473689599195e-06
p8: 0.0006489910301752388
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.5
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['狗粮', 'สุนัข', 'DOG', 'seh', ' собак', 'ัข', ' собаки', ' собака']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.090  | 0.913847 | +0.006            |
| 2      | 'Based' | -2.840  | 0.058420 | -0.119            |
| 3      | 'Most'  | -5.465  | 0.004232 | +0.131            |
| 4      | 'To'    | -5.590  | 0.003735 | +0.131            |
| 5      | 'Sp'    | -5.715  | 0.003296 | -0.119            |
| 6      | 'An'    | -5.965  | 0.002567 | +0.131            |
| 7      | '**'    | -6.090  | 0.002265 | +0.131            |
| 8      | 'Anim'  | -7.090  | 0.000833 | -0.119            |
| 9      | 'First' | -7.090  | 0.000833 | +0.131            |
| 10     | 'There' | -7.090  | 0.000833 | +0.006            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
