---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
country_swap: false
coordinate_kind: None
reverse: true
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
vjp_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt
donor_checkpoint: None
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: arithmetic_control
expected_answer: '4'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.9857485294342041
r2: 0.032258064516129004
---
# Base

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.', '5', '.\\', ' {}.', '++.', '3', '?.', '+.', '\\.', '.?', ' quart', ' fours', ' ?.', '{}.', '?\\', '四是', '.\\"', 'four', '?', '-four', ' FOUR', '().', ' fourth', '_.', ' ().', '6', '？', '四十', '___', '.*']

Generation (32 tokens):
```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0149069 | 0.985204    |             0 |
| 5       | -5.51491   | 0.0040263   |             0 |
| 2       | -5.63991   | 0.0035532   |             0 |
| 3       | -5.76491   | 0.00313569  |             0 |
| 1       | -6.51491   | 0.00148119  |             0 |
| 6       | -7.13991   | 0.000792826 |             0 |
| 8       | -7.51491   | 0.000544901 |             0 |
| 0       | -7.88991   | 0.000374504 |             0 |
|         | -8.01491   | 0.000330499 |             0 |
| 9       | -8.38991   | 0.000227148 |             0 |

Final-decode readout: [' analyze', 'analyze', '分析', '**', '**:', ' analyzes', ' Analy', '分析和', '分析一下', ')**', ':**', ' analyzing', ' analiz', '-**', '）**', ' analyzed', '):**', '分析的', ']**', '：**', ' Analyzer', ')**,', 'analysis', '*\\', '分析法', ';**', 'alyze', '分析了', ',**', 'analy', ' تحلیل', '的分析']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
