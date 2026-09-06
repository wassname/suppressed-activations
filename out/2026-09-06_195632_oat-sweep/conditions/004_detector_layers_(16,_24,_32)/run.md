---
condition_id: "004_detector_layers_(16,_24,_32)"
axis: "detector_layers"
value: "(16, 24, 32)"
is_default: false
swap_log_odds_shift: 0.6250004768371582
valid_answer_mass: 0.0006263487739488482
p4: 2.2508495476358803e-06
p8: 0.0006240979419089854
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/004_detector_layers_(16,_24,_32)/run.md"
---

# 004_detector_layers_(16,_24,_32)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    16,
    24,
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
[':number', ' Déb', ' конкурс', ' وعدد', ' Конкурс', ' Número', '消费市场', '_Number']
```

Unmodified donor readout:

```python
['新', 'kontakt', ' متاب', ' kulinar', ' Kemal', ' القا', '砕', ' Territ']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.129  | 0.878795 | -0.033            |
| 2      | 'Based' | -2.379  | 0.092624 | +0.342            |
| 3      | 'Most'  | -5.254  | 0.005226 | +0.342            |
| 4      | 'Sp'    | -5.379  | 0.004611 | +0.217            |
| 5      | 'To'    | -5.754  | 0.003169 | -0.033            |
| 6      | 'An'    | -5.879  | 0.002797 | +0.217            |
| 7      | 'Anim'  | -6.504  | 0.001497 | +0.467            |
| 8      | '**'    | -6.504  | 0.001497 | -0.283            |
| 9      | 'There' | -7.004  | 0.000908 | +0.092            |
| 10     | 'Many'  | -7.129  | 0.000801 | +0.342            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
