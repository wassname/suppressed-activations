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
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 1.625
answer_pair_mass: 0.8995150923728943
swap_log_odds_shift: 1.625
bare_answer_mass: 0.8995150923728943
r2: 0.09677419354838712
---
# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' claws', '___', '.\\', '蛛', '爬', ' ___', '...\\', ' paw', ' Gecko', '爪子', ' claw', '-web', ').\\', '\\"\\', ' crawling', '\\"', ' eight', '.\\"', ' venom', '____', ' crawl', '\\n', '__.', ' seven', ' __', '爬虫', '__']

Generation (32 tokens):
```text
8.
Question: How many legs does the animal that spins webs have?
Answer: The animal that spins webs has 8 legs.

Fact:
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| 8       | -0.38705 | 0.679057   |      -0.26213 |
| 4       | -1.51205 | 0.220458   |       1.36287 |
| 2       | -3.63705 | 0.0263299  |       1.36287 |
| 1       | -3.88705 | 0.0205058  |       0.73787 |
| 6       | -3.88705 | 0.0205058  |      -0.26213 |
| 3       | -4.51205 | 0.0109759  |       0.61287 |
| 0       | -4.63705 | 0.00968623 |       1.86287 |
| 5       | -5.51205 | 0.00403782 |       0.11287 |
| 7       | -5.88705 | 0.00277515 |      -0.13713 |
|         | -6.26205 | 0.00190733 |       0.73787 |

Final-decode readout: [':', ':\\', '*:', '：', ' Facts', '__:', ':*', ':...', ':\\"', ':The', '\\":', '\\:', '!:', '#:', '_:', '：**', ':F', ':**', "':", '’:', ' :', '.:', ' **:', '$:', ':\\\\', ':&', ':$', 'facts', ':A', ' _:', ':T', ' **:**']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
