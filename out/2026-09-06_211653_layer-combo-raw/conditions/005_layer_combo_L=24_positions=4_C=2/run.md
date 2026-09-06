---
condition_id: "005_layer_combo_L=24_positions=4_C=2"
axis: "layer_combo"
value: "L=24,positions=4,C=2"
is_default: false
swap_log_odds_shift: 2.875
valid_answer_mass: 0.8994007110595703
p4: 0.4777700901031494
p8: 0.4216306209564209
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/005_layer_combo_L=24_positions=4_C=2/run.md"
---

# 005_layer_combo_L=24_positions=4_C=2

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
    24
  ],
  "intervention_positions": 4,
  "strength": 2.0,
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
['狗粮', '吠', 'สุนัข', ' собаки', ' canine', ' собак', ' perros', ' cão']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 50.820335388183594,
    "perturbation_norm": 16.057842254638672,
    "relative_perturbation_by_position": [
      0.30034005641937256,
      0.31660860776901245,
      0.19878952205181122,
      0.42904192209243774
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.739  | 0.477770 | +2.136            |
| 2      | '8'     | -0.864  | 0.421631 | -0.739            |
| 3      | '6'     | -2.989  | 0.050357 | +0.636            |
| 4      | '1'     | -4.114  | 0.016348 | +0.511            |
| 5      | '2'     | -4.364  | 0.012732 | +0.636            |
| 6      | '0'     | -4.864  | 0.007722 | +1.636            |
| 7      | '3'     | -5.114  | 0.006014 | +0.011            |
| 8      | '5'     | -6.051  | 0.002355 | -0.426            |
| 9      | '7'     | -6.301  | 0.001834 | -0.551            |
| 10     | '9'     | -6.551  | 0.001429 | +0.011            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
