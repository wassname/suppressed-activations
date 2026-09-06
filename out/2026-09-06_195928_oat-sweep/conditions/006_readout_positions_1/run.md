---
condition_id: "006_readout_positions_1"
axis: "readout_positions"
value: "1"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.27091357111930847
p4: 0.003367902245372534
p8: 0.2675456702709198
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.125
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' passiert', '豆角', ' brak', 'ENCIA', 'esos', 'anismos', '隨即', ' Localização']
```

Unmodified donor readout:

```python
['\tva', '豆角', 'gos', ' Lounge', ' Kepolisian', ' законода', ' выставке', 'สุนัข']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.818  | 0.441108 | +0.403            |
| 2      | '8'      | -1.318  | 0.267546 | -0.097            |
| 3      | 'The'    | -1.818  | 0.162275 | -0.597            |
| 4      | 'Fact'   | -2.818  | 0.059698 | -0.097            |
| 5      | 'Number' | -3.443  | 0.031954 | +0.653            |
| 6      | '###'    | -3.943  | 0.019381 | +0.278            |
| 7      | '4'      | -5.693  | 0.003368 | -0.347            |
| 8      | '1'      | -6.193  | 0.002043 | +0.153            |
| 9      | 'Answer' | -6.693  | 0.001239 | +0.278            |
| 10     | 'Eight'  | -6.693  | 0.001239 | +0.153            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
