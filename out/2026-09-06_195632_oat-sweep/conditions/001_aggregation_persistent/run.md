---
condition_id: "001_aggregation_persistent"
axis: "aggregation"
value: "persistent"
is_default: false
swap_log_odds_shift: 0.3124995231628418
valid_answer_mass: 0.0005054306238889694
p4: 1.330128043264267e-06
p8: 0.0005041005206294358
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.125
log: "conditions/001_aggregation_persistent/run.md"
---

# 001_aggregation_persistent

Resolved config:

```json
{
  "aggregation": "persistent",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['-cancel', 'IMI', 'òi', ' Monteiro', ' krém', ' Страна', 'PBS', '民政部门']
```

Unmodified donor readout:

```python
['_approval', ' Quantidade', ' Emas', '直肠癌', 'dach', '民政部门', ' smaak', ' пользов']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.093  | 0.911435 | +0.003            |
| 2      | 'Based'  | -2.718  | 0.066024 | +0.003            |
| 3      | 'To'     | -5.593  | 0.003725 | +0.128            |
| 4      | 'Sp'     | -5.843  | 0.002901 | -0.247            |
| 5      | 'An'     | -6.093  | 0.002259 | +0.003            |
| 6      | '**'     | -6.218  | 0.001994 | +0.003            |
| 7      | 'Most'   | -6.468  | 0.001553 | -0.872            |
| 8      | 'First'  | -6.718  | 0.001209 | +0.503            |
| 9      | 'There'  | -6.843  | 0.001067 | +0.253            |
| 10     | 'Animal' | -7.218  | 0.000733 | -0.122            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
