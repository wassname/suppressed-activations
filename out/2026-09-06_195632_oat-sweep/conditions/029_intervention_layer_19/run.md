---
condition_id: "029_intervention_layer_19"
axis: "intervention_layer"
value: "19"
is_default: false
swap_log_odds_shift: 0.2499995231628418
valid_answer_mass: 0.0005102178547531366
p4: 1.2615757896128343e-06
p8: 0.0005089562619104981
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/029_intervention_layer_19/run.md"
---

# 029_intervention_layer_19

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
  "intervention_layer": 19,
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
[' 인프라', 'seh', 'Integrated', ' веб', ' webView', '盐酸', '\tspin', ' факта']
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
| 1      | 'The'   | -0.083  | 0.920214 | +0.013            |
| 2      | 'Based' | -3.083  | 0.045815 | -0.362            |
| 3      | 'Sp'    | -4.958  | 0.007026 | +0.638            |
| 4      | 'Most'  | -5.458  | 0.004261 | +0.138            |
| 5      | 'To'    | -5.458  | 0.004261 | +0.263            |
| 6      | 'An'    | -5.583  | 0.003761 | +0.513            |
| 7      | '**'    | -6.208  | 0.002013 | +0.013            |
| 8      | 'Anim'  | -6.208  | 0.002013 | +0.763            |
| 9      | 'There' | -7.083  | 0.000839 | +0.013            |
| 10     | 'First' | -7.083  | 0.000839 | +0.138            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
