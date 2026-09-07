---
condition_id: "031_persistent_generation_L=23_24_25_26_positions=4_C=2"
axis: "persistent_generation"
value: "L=23+24+25+26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.0624995231628418
valid_answer_mass: 0.0005701701156795025
p4: 1.1692721955114393e-06
p8: 0.0005690008401870728
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/031_persistent_generation_L=23_24_25_26_positions=4_C=2/run.md"
---

# 031_persistent_generation_L=23_24_25_26_positions=4_C=2

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
  "strength": 2.0,
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
['狗粮', 'สุนัข', '和金', ' doga', ' krém', ' Ủy', '的神奇', '\')."']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `031_persistent_generation_L=23_24_25_26_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachids, which means they have **8 legs**. This distinguishes them from
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.097  | 0.907893 | -0.001            |
| 2      | 'Based' | -2.722  | 0.065768 | -0.001            |
| 3      | 'Sp'    | -5.472  | 0.004204 | +0.124            |
| 4      | 'Most'  | -5.597  | 0.003710 | -0.001            |
| 5      | 'To'    | -5.722  | 0.003274 | -0.001            |
| 6      | 'An'    | -6.097  | 0.002250 | -0.001            |
| 7      | '**'    | -6.222  | 0.001986 | -0.001            |
| 8      | 'There' | -7.097  | 0.000828 | -0.001            |
| 9      | 'Anim'  | -7.097  | 0.000828 | -0.126            |
| 10     | 'First' | -7.222  | 0.000731 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
