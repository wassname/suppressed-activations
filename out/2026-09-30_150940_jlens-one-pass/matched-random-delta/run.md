---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 19
readout_block_index: 23
reverse: false
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-3:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: None
donor_norm: None
equal_donor_norm: false
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.1249999925494194
answer_pair_mass: 0.9396295547485352
swap_log_odds_shift: 0.1249999925494194
bare_answer_mass: 0.9396295547485352
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '爬', ' venom', ' insects', '___', '爪子', ' crawling', ' Gecko', '四肢', '.\\', ' limbs', ' claw', '爬虫', '_web', ' paw', '�', '昆虫', '后腿', ' lizard', ').\\', ' eight', '网页', ' craw', '双腿', ' tails']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.132206 | 0.876161   |   -0.00728666 |
|       4 | -2.75721  | 0.0634689  |    0.117713   |
|       6 | -3.63221  | 0.0264578  |   -0.00728679 |
|       1 | -4.63221  | 0.00973326 |   -0.00728655 |
|       2 | -5.00721  | 0.00668957 |   -0.00728655 |
|       3 | -5.13221  | 0.00590352 |   -0.00728655 |
|       5 | -5.63221  | 0.00358067 |   -0.00728655 |
|       7 | -5.75721  | 0.00315993 |   -0.00728655 |
|       9 | -6.56971  | 0.00140221 |   -0.00728655 |
|       0 | -6.63221  | 0.00131725 |   -0.132287   |

Final-decode readout: ['用户', '*\\', ' *\\', ' user', '思路', '#\\', 'user', 'User', ' reasoning', ' User', '用户的', '用户需求', '/User', '#:', ' USER', '思考', '/user', '-user', 'Streamer', '(user', '//*', '/Instruction', '推理', 'Thought', '的思考', ' Users', '和用户', 'AI', '一是要', '任务', '的用户', '#.']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
