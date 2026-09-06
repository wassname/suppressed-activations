---
condition_id: "006_readout_positions_1"
axis: "readout_positions"
value: "1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9776723980903625
p4: 0.032347239553928375
p8: 0.9453251361846924
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/006_readout_positions_1/run.md"
---

# 006_readout_positions_1

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 1,
  "rank": 8,
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['抗美援朝', ' latihan', ' рекоменда', ' Vader', ' Lounge', ' Reggio', ' Kampus', '_unix']
```

Unmodified donor readout:

```python
['gos', ' законода', '豆角', 'ツール', ' brak', '呼吸道感染', ' Kepolisian', 'Force']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.056  | 0.945325 | -0.005            |
| 2      | '4'       | -3.431  | 0.032347 | -0.005            |
| 3      | '6'       | -4.181  | 0.015280 | +0.495            |
| 4      | '<think>' | -6.056  | 0.002343 | -0.255            |
| 5      | '1'       | -6.431  | 0.001610 | +0.120            |
| 6      | '2'       | -7.556  | 0.000523 | +0.120            |
| 7      | '3'       | -7.806  | 0.000407 | +0.120            |
| 8      | '5'       | -8.244  | 0.000263 | +0.183            |
| 9      | '7'       | -8.244  | 0.000263 | +0.120            |
| 10     | '0'       | -8.306  | 0.000247 | +0.183            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
