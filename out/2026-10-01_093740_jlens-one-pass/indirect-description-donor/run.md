---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: true
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
vjp_checkpoint: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/donors.pt
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
answer_pair_mass: 0.9851811528205872
r2: 0.06451612903225812
---
# indirect-description donor

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.\\', '.', '++.', '\\.', '5', '3', '?.', ' {}.', '+.', '.?', ' fours', '?\\', ' quart', '四是', ' ?.', '?', '.\\"', 'four', '-four', ' FOUR', '_.', ' fourth', '{}.', '___', '.*', '6', ' ().', '().', '____', '？']

Generation (32 tokens):
```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>

</think>

Yes, the fact
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0154827 | 0.984637    |  -0.000575786 |
| 5       | -5.51548   | 0.00402398  |  -0.000576019 |
| 2       | -5.51548   | 0.00402398  |   0.124424    |
| 3       | -5.64048   | 0.00355115  |   0.124424    |
| 1       | -6.64048   | 0.0013064   |  -0.125576    |
| 6       | -7.14048   | 0.000792369 |  -0.000576019 |
| 8       | -7.51548   | 0.000544587 |  -0.000576019 |
|         | -8.07798   | 0.000310296 |  -0.063076    |
| 0       | -8.14048   | 0.000291496 |  -0.250576    |
| 7       | -8.45298   | 0.000213263 |  -0.000576019 |

Final-decode readout: [' facts', '事实', ' factual', ' Facts', 'facts', '的事实', ' fakta', '_fact', '事實', '事实和', ' Fakta', ' факты', ' Fakten', ' fatos', ' факт', ' Fakt', ' premise', '认定事实', ' факта', ' fakt', '_FACT', ' fato', '事実', ' statement', '上述事实', ' **', ' answer', ' hypothesis', ' **【', ' faptul', ' факти', '事实证明']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
