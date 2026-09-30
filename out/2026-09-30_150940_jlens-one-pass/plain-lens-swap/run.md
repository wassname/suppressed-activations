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
answer_log_odds_shift: -7.450580596923828e-09
answer_pair_mass: 0.9330177307128906
swap_log_odds_shift: -7.450580596923828e-09
bare_answer_mass: 0.9330177307128906
r2: 0.032258064516129004
---
# plain-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '___', '-web', ' venom', ' insects', '爬', '.\\', '爪子', '四肢', ' Gecko', ' crawling', ' limbs', ').\\', '昆虫', '____', '_web', ' claw', ' paw', ' lizard', '后腿', ' tails', ' eight', '爬虫', '触角', '�', '双腿']

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
|       8 | -0.131299 | 0.876956   |   -0.00637955 |
|       4 | -2.8813   | 0.0560619  |   -0.0063796  |
|       6 | -3.3813   | 0.0340033  |    0.24362    |
|       1 | -4.6313   | 0.0097421  |   -0.00637913 |
|       2 | -5.0063   | 0.00669564 |   -0.00637913 |
|       3 | -5.2563   | 0.00521457 |   -0.131379   |
|       5 | -5.6313   | 0.00358392 |   -0.00637913 |
|       7 | -5.8813   | 0.00279116 |   -0.131379   |
|       0 | -6.4438   | 0.00159035 |    0.0561209  |
|       9 | -6.6313   | 0.00131845 |   -0.0688791  |

Final-decode readout: ['过程', ' Process', 'Process', 'process', ' process', '过程的', '過程', '-process', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', 'prozess', '过程中', ' processus', 'PROCESS', ' процесс', ' proceso', '过程中的', ' processo', ' processes', ' процесса', ' Процесс', 'Processes', ' proces', '/process', '*:']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
