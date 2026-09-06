---
condition_id: "010_rank_16"
axis: "rank"
value: "16"
is_default: false
swap_log_odds_shift: 6.5
valid_answer_mass: 5.932621206738986e-06
p4: 3.335180281283101e-06
p8: 2.597440925455885e-06
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/010_rank_16/run.md"
---

# 010_rank_16

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
  "rank": 16,
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
['趣事', ' 인프라', '_FACT', ' факта', '晶圆', '在校园', ' Playback', ' Gelegenheit', ' Highlights', 'έ', ' Sebag', '的场所', '_at', ' voller', '实验学校', ' ОГ']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens', '吠', ' canine', ' doga', ' chien', ' perros', ' соба', ' собак', ' собака']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

**Answer:**
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.361  | 0.696990 | -0.265            |
| 2      | 'Based' | -1.486  | 0.226280 | +1.235            |
| 3      | 'There' | -4.111  | 0.016392 | +2.985            |
| 4      | 'To'    | -4.236  | 0.014466 | +1.485            |
| 5      | 'It'    | -4.861  | 0.007743 | +4.485            |
| 6      | 'This'  | -5.111  | 0.006030 | +2.735            |
| 7      | 'First' | -5.111  | 0.006030 | +2.110            |
| 8      | '**'    | -5.361  | 0.004696 | +0.860            |
| 9      | 'I'     | -5.611  | 0.003657 | +3.798            |
| 10     | 'You'   | -5.861  | 0.002848 | +2.173            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
