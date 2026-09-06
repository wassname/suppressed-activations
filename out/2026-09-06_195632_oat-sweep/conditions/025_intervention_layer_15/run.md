---
condition_id: "025_intervention_layer_15"
axis: "intervention_layer"
value: "15"
is_default: false
swap_log_odds_shift: 0.8125004768371582
valid_answer_mass: 0.0004999280790798366
p4: 2.1654404918081127e-06
p8: 0.0004977626376785338
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/025_intervention_layer_15/run.md"
---

# 025_intervention_layer_15

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
  "intervention_layer": 15,
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
[' 인프라', '\tspin', 'seh', ' krém', ' Fait', '웹', 'edata', 'Spin']
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
| 1      | 'The'   | -0.105  | 0.899976 | -0.009            |
| 2      | 'Based' | -2.730  | 0.065194 | -0.009            |
| 3      | 'Most'  | -5.230  | 0.005351 | +0.366            |
| 4      | 'To'    | -5.355  | 0.004723 | +0.366            |
| 5      | 'Sp'    | -5.355  | 0.004723 | +0.241            |
| 6      | 'An'    | -5.605  | 0.003678 | +0.491            |
| 7      | '**'    | -6.230  | 0.001969 | -0.009            |
| 8      | 'That'  | -6.480  | 0.001533 | +1.116            |
| 9      | 'There' | -6.730  | 0.001194 | +0.366            |
| 10     | 'Anim'  | -6.855  | 0.001054 | +0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
