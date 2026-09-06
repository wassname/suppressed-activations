---
condition_id: "041_intervention_layer_31"
axis: "intervention_layer"
value: "31"
is_default: false
swap_log_odds_shift: -0.0625
valid_answer_mass: 0.0005073340144008398
p4: 9.18381601877627e-07
p8: 0.0005064156139269471
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/041_intervention_layer_31/run.md"
---

# 041_intervention_layer_31

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
  "intervention_layer": 31,
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
[' spinning', 'web', '-web', ' spin', ' spins', '在校园', 'Web', '纺']
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
| 1      | 'The'    | -0.088  | 0.915621 | +0.008            |
| 2      | 'Based'  | -2.838  | 0.058534 | -0.117            |
| 3      | 'Most'   | -5.588  | 0.003742 | +0.008            |
| 4      | 'Sp'     | -5.713  | 0.003302 | -0.117            |
| 5      | 'To'     | -5.713  | 0.003302 | +0.008            |
| 6      | 'An'     | -5.963  | 0.002572 | +0.133            |
| 7      | '**'     | -6.213  | 0.002003 | +0.008            |
| 8      | 'Animal' | -6.963  | 0.000946 | +0.133            |
| 9      | 'Anim'   | -6.963  | 0.000946 | +0.008            |
| 10     | 'There'  | -7.088  | 0.000835 | +0.008            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
