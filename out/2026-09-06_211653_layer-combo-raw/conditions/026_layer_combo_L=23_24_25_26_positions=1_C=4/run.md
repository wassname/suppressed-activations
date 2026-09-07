---
condition_id: "026_layer_combo_L=23_24_25_26_positions=1_C=4"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=4"
is_default: false
swap_log_odds_shift: 2.6875
valid_answer_mass: 0.07866469025611877
p4: 0.0381036102771759
p8: 0.04056107997894287
repeated_bigram_fraction: 0.967741935483871
generation_tokens: 32
first_token: "吠"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.375
log: "conditions/026_layer_combo_L=23_24_25_26_positions=1_C=4/run.md"
---

# 026_layer_combo_L=23_24_25_26_positions=1_C=4

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
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
}
```

Source input (`repr`):

```python
'Fact: The number of legs on the animal that spins webs is '
```

Donor input (`repr`):

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Readout after intervention:

```python
[' dogs', ' puppies', '狗粮', '犬', ' canine', ' puppy', '吠', ' chien']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `026_layer_combo_L=23_24_25_26_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '吠'     | -1.267  | 0.281550 | +21.779           |
| 2      | 'web'   | -1.392  | 0.248467 | +16.264           |
| 3      | '8'     | -3.205  | 0.040561 | -3.080            |
| 4      | '4'     | -3.267  | 0.038104 | -0.393            |
| 5      | '\n'    | -3.892  | 0.020395 | +8.482            |
| 6      | 'can'   | -4.080  | 0.016908 | +19.647           |
| 7      | '7'     | -4.142  | 0.015884 | +1.607            |
| 8      | '2'     | -4.142  | 0.015884 | +0.857            |
| 9      | '1'     | -4.205  | 0.014922 | +0.420            |
| 10     | ' '     | -4.205  | 0.014922 | +2.795            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
