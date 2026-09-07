---
condition_id: "028_persistent_generation_L=23_24_25_26_positions=4_C=0.25"
axis: "persistent_generation"
value: "L=23+24+25+26,positions=4,C=0.25"
is_default: false
swap_log_odds_shift: 0.0625
valid_answer_mass: 0.0005036935326643288
p4: 1.0329463293601293e-06
p8: 0.0005026605795137584
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/028_persistent_generation_L=23_24_25_26_positions=4_C=0.25/run.md"
---

# 028_persistent_generation_L=23_24_25_26_positions=4_C=0.25

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
  "intervention_layer": [
    23,
    24,
    25,
    26
  ],
  "intervention_positions": 4,
  "strength": 0.25,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true
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
['在校园', 'seh', '盐酸', 'Integrated', ' факта', ' Ủy', '웹', ' Presents']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `028_persistent_generation_L=23_24_25_26_positions=4_C=0.25`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908832 | +0.001            |
| 2      | 'Based'  | -2.721  | 0.065836 | +0.001            |
| 3      | 'Most'   | -5.596  | 0.003714 | +0.001            |
| 4      | 'Sp'     | -5.721  | 0.003278 | -0.124            |
| 5      | 'To'     | -5.721  | 0.003278 | +0.001            |
| 6      | 'An'     | -6.096  | 0.002253 | +0.001            |
| 7      | '**'     | -6.221  | 0.001988 | +0.001            |
| 8      | 'Animal' | -7.096  | 0.000829 | +0.001            |
| 9      | 'Anim'   | -7.096  | 0.000829 | -0.124            |
| 10     | 'There'  | -7.096  | 0.000829 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
