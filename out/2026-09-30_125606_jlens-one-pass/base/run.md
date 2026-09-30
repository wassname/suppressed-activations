---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -7.450580596923828e-09
answer_pair_mass: 0.9389888644218445
swap_log_odds_shift: -7.450580596923828e-09
bare_answer_mass: 0.9389888644218445
r2: 0.032258064516129004
---
# Base

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '___', ' venom', '爬', ' insects', '.\\', ' crawling', '四肢', '爪子', ' Gecko', ' limbs', '_web', ').\\', '网页', '昆虫', '�', '爬虫', ' claw', '____', ' eight', '后腿', ' lizard', '双腿', ' paw', '触角']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.124919 | 0.882568   |             0 |
|       4 | -2.87492  | 0.0564207  |             0 |
|       6 | -3.62492  | 0.0266513  |             0 |
|       1 | -4.62492  | 0.00980445 |             0 |
|       2 | -4.99992  | 0.00673849 |             0 |
|       3 | -5.12492  | 0.0059467  |             0 |
|       5 | -5.62492  | 0.00360685 |             0 |
|       7 | -5.74992  | 0.00318304 |             0 |
|       0 | -6.49992  | 0.00150356 |             0 |
|       9 | -6.56242  | 0.00141246 |             0 |

Final-decode readout: ['**:', '»:', '*:', ':**', '”:', '__:', '):', ':.', '：**', ':\\', ']:', '.):', '>:', ':', '：', ':</', '’:', '":', '+:', ':")', '#:', '():', ':".', '.:', '!:', '}:', ' **:', '):**', ':user', '):\\', '\\":', ')):']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
