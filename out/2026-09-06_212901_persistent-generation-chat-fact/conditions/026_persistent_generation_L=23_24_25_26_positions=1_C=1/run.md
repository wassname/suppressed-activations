---
condition_id: "026_persistent_generation_L=23_24_25_26_positions=1_C=1"
axis: "persistent_generation"
value: "L=23+24+25+26,positions=1,C=1"
is_default: false
swap_log_odds_shift: -0.0625004768371582
valid_answer_mass: 0.000574818579480052
p4: 1.0405425427961745e-06
p8: 0.0005737780593335629
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/026_persistent_generation_L=23_24_25_26_positions=1_C=1/run.md"
---

# 026_persistent_generation_L=23_24_25_26_positions=1_C=1

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
  "intervention_positions": 1,
  "strength": 1.0,
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
['-spin', 'Spin', 'seh', 'ปั่น', '盐酸', 'spin', ' krém', ' 인프라']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `026_persistent_generation_L=23_24_25_26_positions=1_C=1`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.088  | 0.915516 | +0.008            |
| 2      | 'Based'  | -2.838  | 0.058527 | -0.117            |
| 3      | 'Sp'     | -5.588  | 0.003742 | +0.008            |
| 4      | 'Most'   | -5.588  | 0.003742 | +0.008            |
| 5      | 'To'     | -5.713  | 0.003302 | +0.008            |
| 6      | 'An'     | -6.088  | 0.002269 | +0.008            |
| 7      | '**'     | -6.213  | 0.002003 | +0.008            |
| 8      | 'Animal' | -7.088  | 0.000835 | +0.008            |
| 9      | 'Anim'   | -7.088  | 0.000835 | -0.117            |
| 10     | 'There'  | -7.088  | 0.000835 | +0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
