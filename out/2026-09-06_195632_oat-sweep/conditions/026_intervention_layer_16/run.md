---
condition_id: "026_intervention_layer_16"
axis: "intervention_layer"
value: "16"
is_default: false
swap_log_odds_shift: 0.6875
valid_answer_mass: 0.0005730307893827558
p4: 2.1915470824751537e-06
p8: 0.0005708392709493637
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/026_intervention_layer_16/run.md"
---

# 026_intervention_layer_16

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
  "intervention_layer": 16,
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
[' 인프라', 'Spin', '\tspin', 'seh', '在校园', '盐酸', ' Presents', ' legado']
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

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.093  | 0.910827 | +0.003            |
| 2      | 'Based' | -2.843  | 0.058227 | -0.122            |
| 3      | 'An'    | -5.468  | 0.004218 | +0.628            |
| 4      | 'To'    | -5.468  | 0.004218 | +0.253            |
| 5      | 'Most'  | -5.593  | 0.003722 | +0.003            |
| 6      | 'Sp'    | -5.718  | 0.003285 | -0.122            |
| 7      | '**'    | -6.218  | 0.001992 | +0.003            |
| 8      | 'That'  | -6.593  | 0.001369 | +1.003            |
| 9      | 'There' | -6.843  | 0.001066 | +0.253            |
| 10     | 'First' | -6.843  | 0.001066 | +0.378            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
