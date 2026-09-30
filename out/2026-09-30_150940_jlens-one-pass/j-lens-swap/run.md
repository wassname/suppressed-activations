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
expected_answer: '4'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 1.375
answer_pair_mass: 0.8193766474723816
swap_log_odds_shift: 1.375
bare_answer_mass: 0.8193766474723816
r2: 0.032258064516129004
---
# J-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' claws', '___', '蜘蛛', ' spider', ' paw', '爪子', '.\\', '____', ' tails', '四肢', '蛛', ' limbs', ' furry', '尾巴', 'Spider', ' animals', ').\\', ' Spider', ' mammals', ' Gecko', ' ___', ' insects', '__.', '两只', '后腿', '__', ' lizard', '双腿', ' FOUR', '\\"\\', ' venom']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.424624 | 0.654016   |    -0.299705  |
|       4 | -1.79962  | 0.165361   |     1.0753    |
|       6 | -2.04962  | 0.128783   |     1.5753    |
|       1 | -4.04962  | 0.0174289  |     0.575295  |
|       2 | -4.67462  | 0.00932903 |     0.325295  |
|       3 | -4.67462  | 0.00932903 |     0.450295  |
|       5 | -5.29962  | 0.00499347 |     0.325295  |
|       0 | -5.54962  | 0.00388892 |     0.950295  |
|       7 | -5.79962  | 0.00302869 |    -0.0497046 |
|       9 | -6.42462  | 0.00162114 |     0.137795  |

Final-decode readout: ['过程', ' Process', ' process', 'Process', 'process', '過程', '过程的', '-process', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', '过程中', ' processus', ' процесс', 'prozess', ' processes', 'PROCESS', ' proceso', '过程中的', ' processo', ' proces', 'Processes', ' Процесс', ' процесса', '/process', ' proses']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
