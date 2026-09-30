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
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9869756698608398
r2: 0.032258064516129004
---
# offline naming VJP

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.', '5', '.\\', ' {}.', '++.', '3', '+.', '?.', '\\.', '.?', ' quart', ' ?.', ' fours', '四是', '{}.', '?\\', 'four', '.\\"', '?', '-four', ' FOUR', ' fourth', '().', '_.', '6', ' ().', '四十', '？', '___', '____']

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
| 4       | -0.0135978 | 0.986494    |    0.00130908 |
| 5       | -5.6386    | 0.00355785  |   -0.123691   |
| 2       | -5.6386    | 0.00355785  |    0.00130892 |
| 3       | -5.8886    | 0.00277086  |   -0.123691   |
| 1       | -6.6386    | 0.00130886  |   -0.123691   |
| 6       | -7.2636    | 0.000700583 |   -0.123691   |
| 8       | -7.6386    | 0.000481503 |   -0.123691   |
| 0       | -8.0136    | 0.000330932 |   -0.123691   |
|         | -8.1386    | 0.000292046 |   -0.123691   |
| 7       | -8.5136    | 0.00020072  |   -0.0611906  |

Final-decode readout: [' analyze', 'analyze', '分析', '**', '**:', ' analyzes', ' Analy', '分析和', '分析一下', ')**', ':**', ' analyzing', ' analiz', '-**', '）**', ' analyzed', '):**', ']**', '分析的', '：**', ')**,', ' Analyzer', '*\\', 'analysis', ';**', '分析法', 'alyze', '分析了', ',**', 'analy', ' تحلیل', ' Analysis']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
