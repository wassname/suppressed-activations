---
condition_id: "004_normalization_strength_C=64,component_norm=True,residual_norm=True"
axis: "normalization_strength"
value: "C=64,component_norm=True,residual_norm=True"
is_default: false
swap_log_odds_shift: 3.5
valid_answer_mass: 7.042888319119811e-05
p4: 2.455468893458601e-05
p8: 4.58741960756015e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "It"
readout_overlap: 0.0
log: "conditions/004_normalization_strength_C=64,component_norm=True,residual_norm=True/run.md"
---

# 004_normalization_strength_C=64,component_norm=True,residual_norm=True

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
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 64.0,
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
[' políticas', ' Workflow', '爵士', '合伙企业', '강', ' политики', '宇宙', ' usuário']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
It looks like you've pasted a string of repeated "tag" or "placeholder" text, possibly from a code snippet, a design mockup, or
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'It'      | -0.302  | 0.739258 | +10.419           |
| 2      | 'The'     | -2.677  | 0.068762 | -1.456            |
| 3      | 'This'    | -3.240  | 0.039179 | +6.794            |
| 4      | 'Your'    | -3.802  | 0.022324 | +8.669            |
| 5      | 'Looking' | -4.240  | 0.014413 | +9.294            |
| 6      | 'You'     | -4.365  | 0.012720 | +7.482            |
| 7      | '`'       | -4.677  | 0.009306 | +7.294            |
| 8      | 'Looks'   | -4.740  | 0.008742 | +11.763           |
| 9      | 'That'    | -4.802  | 0.008212 | +6.732            |
| 10     | '```'     | -4.802  | 0.008212 | +7.482            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
