---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: 0.25
bare_answer_mass: 0.9394852519035339
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '爬', ' venom', '___', ' crawling', '爪子', ' insects', ' Gecko', '四肢', '.\\', ' claw', '_web', ' limbs', ' paw', '爬虫', '�', ').\\', '后腿', ' lizard', '网页', '昆虫', ' eight', ' craw', '双腿', '蜘']

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
|       8 | -0.141313 | 0.868218   |    -0.0163937 |
|       4 | -2.64131  | 0.0712676  |     0.233606  |
|       6 | -3.64131  | 0.0262179  |    -0.0163937 |
|       1 | -4.64131  | 0.00964502 |    -0.0163937 |
|       2 | -5.01631  | 0.00662892 |    -0.0163937 |
|       3 | -5.14131  | 0.00585    |    -0.0163937 |
|       5 | -5.51631  | 0.00402064 |     0.108606  |
|       7 | -5.76631  | 0.00313128 |    -0.0163937 |
|       0 | -6.51631  | 0.00147911 |    -0.0163937 |
|       9 | -6.51631  | 0.00147911 |     0.0461063 |

Final-decode readout: [' Process', '过程', 'Process', ' process', 'process', '過程', '-process', '过程的', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', 'PROCESS', '过程中', 'prozess', ' processus', ' процесс', ' proceso', '过程中的', ' processes', ' processo', ' процесса', ' Процесс', ' proces', 'Processes', '*:', '/process']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

Written by PI/OpenAI.
