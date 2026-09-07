---
condition_id: "022_persistent_generation_L=24_26_positions=4_C=1"
axis: "persistent_generation"
value: "L=24+26,positions=4,C=1"
is_default: false
swap_log_odds_shift: 4.76837158203125e-07
valid_answer_mass: 0.0005700280889868736
p4: 1.0982934099956765e-06
p8: 0.0005689297686330974
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/022_persistent_generation_L=24_26_positions=4_C=1/run.md"
---

# 022_persistent_generation_L=24_26_positions=4_C=1

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
    24,
    26
  ],
  "intervention_positions": 4,
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
[' Ủy', ' krém', 'Integrated', '丝绸', '웹', '\')."', ' факта', 'edata']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `022_persistent_generation_L=24_26_positions=4_C=1`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.097  | 0.907780 | -0.001            |
| 2      | 'Based'  | -2.722  | 0.065759 | -0.001            |
| 3      | 'Most'   | -5.472  | 0.004204 | +0.124            |
| 4      | 'Sp'     | -5.722  | 0.003274 | -0.126            |
| 5      | 'To'     | -5.722  | 0.003274 | -0.001            |
| 6      | 'An'     | -5.972  | 0.002550 | +0.124            |
| 7      | '**'     | -6.222  | 0.001986 | -0.001            |
| 8      | 'Anim'   | -6.972  | 0.000938 | -0.001            |
| 9      | 'There'  | -7.097  | 0.000828 | -0.001            |
| 10     | 'Animal' | -7.097  | 0.000828 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
