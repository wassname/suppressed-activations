---
condition_id: "017_intervention_layer_7"
axis: "intervention_layer"
value: "7"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.0011541974963620305
p4: 1.9629692360467743e-06
p8: 0.0011522345012053847
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/017_intervention_layer_7/run.md"
---

# 017_intervention_layer_7

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
  "intervention_layer": 7,
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
['丝绸', 'Spin', '-spin', '웹', '盐酸', 'spin', 'seh', '在校园']
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
| 1      | 'The'   | -0.141  | 0.868444 | -0.045            |
| 2      | 'Based' | -2.266  | 0.103721 | +0.455            |
| 3      | 'To'    | -5.516  | 0.004022 | +0.205            |
| 4      | 'Sp'    | -5.891  | 0.002764 | -0.295            |
| 5      | 'An'    | -5.891  | 0.002764 | +0.205            |
| 6      | '**'    | -6.141  | 0.002153 | +0.080            |
| 7      | 'Most'  | -6.391  | 0.001676 | -0.795            |
| 8      | 'There' | -6.641  | 0.001306 | +0.455            |
| 9      | '8'     | -6.766  | 0.001152 | +0.705            |
| 10     | 'That'  | -6.766  | 0.001152 | +0.830            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
