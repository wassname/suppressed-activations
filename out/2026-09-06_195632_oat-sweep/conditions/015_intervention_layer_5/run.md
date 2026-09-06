---
condition_id: "015_intervention_layer_5"
axis: "intervention_layer"
value: "5"
is_default: false
swap_log_odds_shift: 4.76837158203125e-07
valid_answer_mass: 0.000849946984089911
p4: 1.6376231997128343e-06
p8: 0.0008483093697577715
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/015_intervention_layer_5/run.md"
---

# 015_intervention_layer_5

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
  "intervention_layer": 5,
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
['Spin', 'web', '-spin', 'edata', 'seh', ' Ủy', '_spin', 'spin']
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
| 1      | 'The'    | -0.072  | 0.930284 | +0.024            |
| 2      | 'Based'  | -3.072  | 0.046316 | -0.351            |
| 3      | 'To'     | -5.697  | 0.003355 | +0.024            |
| 4      | 'An'     | -5.697  | 0.003355 | +0.399            |
| 5      | '**'     | -5.822  | 0.002961 | +0.399            |
| 6      | 'Sp'     | -5.822  | 0.002961 | -0.226            |
| 7      | 'First'  | -6.697  | 0.001234 | +0.524            |
| 8      | '8'      | -7.072  | 0.000848 | +0.399            |
| 9      | 'That'   | -7.197  | 0.000749 | +0.399            |
| 10     | 'Animal' | -7.322  | 0.000661 | -0.226            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
