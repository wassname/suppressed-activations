---
condition_id: "030_intervention_layer_20"
axis: "intervention_layer"
value: "20"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.000562528264708817
p4: 1.2278396752662957e-06
p8: 0.0005613004323095083
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/030_intervention_layer_20/run.md"
---

# 030_intervention_layer_20

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
  "intervention_layer": 20,
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
[' факта', 'Integrated', '在校园', 'seh', ' 인프라', '盐酸', ' laba', ' legado']
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
| 1      | 'The'   | -0.110  | 0.895606 | -0.014            |
| 2      | 'Based' | -2.610  | 0.073516 | +0.111            |
| 3      | 'Sp'    | -5.235  | 0.005325 | +0.361            |
| 4      | 'Most'  | -5.360  | 0.004700 | +0.236            |
| 5      | 'To'    | -5.610  | 0.003660 | +0.111            |
| 6      | 'An'    | -5.735  | 0.003230 | +0.361            |
| 7      | '**'    | -6.110  | 0.002220 | +0.111            |
| 8      | 'There' | -6.985  | 0.000925 | +0.111            |
| 9      | 'Anim'  | -6.985  | 0.000925 | -0.014            |
| 10     | 'First' | -7.110  | 0.000817 | +0.111            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
