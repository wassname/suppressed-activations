---
condition_id: "021_intervention_layer_11"
axis: "intervention_layer"
value: "11"
is_default: false
swap_log_odds_shift: 0.6250004768371582
valid_answer_mass: 0.0004957024357281625
p4: 1.7813583781389752e-06
p8: 0.0004939210484735668
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/021_intervention_layer_11/run.md"
---

# 021_intervention_layer_11

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
  "intervention_layer": 11,
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
['丝绸', 'Spin', ' 인프라', 'seh', 'Integrated', '在校园', '盐酸', '웹']
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.113  | 0.893030 | -0.017            |
| 2      | 'Based'  | -2.488  | 0.083065 | +0.233            |
| 3      | 'To'     | -5.363  | 0.004686 | +0.358            |
| 4      | 'Most'   | -5.988  | 0.002508 | -0.392            |
| 5      | 'Sp'     | -6.113  | 0.002214 | -0.517            |
| 6      | 'An'     | -6.113  | 0.002214 | -0.017            |
| 7      | '**'     | -6.113  | 0.002214 | +0.108            |
| 8      | 'First'  | -6.738  | 0.001185 | +0.483            |
| 9      | 'There'  | -7.238  | 0.000719 | -0.142            |
| 10     | 'Animal' | -7.238  | 0.000719 | -0.142            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
