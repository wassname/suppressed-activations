---
condition_id: "011_rank_32"
axis: "rank"
value: "32"
is_default: false
swap_log_odds_shift: 7.3125
valid_answer_mass: 2.9225016078271437e-06
p4: 2.1719097276218235e-06
p8: 7.505919938921579e-07
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/011_rank_32/run.md"
---

# 011_rank_32

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
  "rank": 32,
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
[' voller', ' линей', '_Begin', '这些话', '绮', 'ALIGN', ' эконом', '目标和', 'έ', '晶圆', '\tspin', '这番', 'urdy', '的场所', ' 인프라', 'Calibri', '堕落', 'ék', 'Jay', ' набра', 'Uniform', '到晚', '满腔', '政法大学', '闽', 'PAGE', 'At', 'significant', ' längre', 'อิส', '비용', '满怀']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens', '吠', ' canine', ' doga', ' chien', ' perros', ' соба', ' собак', ' собака', ' cão', '狗狗', '汪', ' Dogs', ' щен', '汪汪', '和金', ' dogg', ' ogs', '_unix', ' Hunde', '茶香', ' розы', '狗的', '散歩', '_gold']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs** (four pairs).
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.852  | 0.426389 | -0.756            |
| 2      | 'Based' | -1.102  | 0.332072 | +1.619            |
| 3      | 'To'    | -2.727  | 0.065389 | +2.994            |
| 4      | 'There' | -2.852  | 0.057705 | +4.244            |
| 5      | 'It'    | -2.977  | 0.050925 | +6.369            |
| 6      | 'First' | -3.602  | 0.027258 | +3.619            |
| 7      | 'This'  | -4.977  | 0.006892 | +2.869            |
| 8      | 'I'     | -5.227  | 0.005367 | +4.181            |
| 9      | '**'    | -5.352  | 0.004737 | +0.869            |
| 10     | 'Let'   | -5.352  | 0.004737 | +4.619            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
