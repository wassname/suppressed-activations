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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.375
answer_pair_mass: 0.9409580230712891
swap_log_odds_shift: 0.375
bare_answer_mass: 0.9409580230712891
r2: 0.09677419354838712
---
# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', '___', '蛛', ' claws', '.\\', ' ___', '...\\', ').\\', '爬', '\\"', '-web', '.\\"', '\\"\\', ' eight', ' Gecko', ' venom', ' crawling', '____', '__.', '__', '?\\', ' __', '\\n', ' insects', '\\""', '。\\', '爪子', ' seven']

Generation (32 tokens):
```text
8.
Question: How many legs does the animal that spins webs have?
Answer: The animal that spins webs has 8 legs.

Fact:
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| 8       | -0.149796 | 0.860883   |     -0.024877 |
| 4       | -2.5248   | 0.0800746  |      0.350123 |
| 1       | -4.3998   | 0.0122798  |      0.225123 |
| 2       | -4.3998   | 0.0122798  |      0.600123 |
| 6       | -4.5248   | 0.0108369  |     -0.899877 |
| 3       | -5.0248   | 0.00657293 |      0.100123 |
| 0       | -5.1498   | 0.00580059 |      1.35012  |
|         | -5.7748   | 0.00310483 |      1.22512  |
| 5       | -6.0248   | 0.00241804 |     -0.399877 |
| 7       | -6.2123   | 0.00200463 |     -0.462377 |

Final-decode readout: [':', ':\\', '：', '*:', ' Facts', '__:', ':*', ':...', ':\\"', '\\":', ':The', '\\:', '#:', '!:', '_:', ':F', '：**', "':", '’:', ' :', ':**', '.:', '$:', ':&', ':\\\\', ' **:', 'facts', ':$', ':A', ' _:', ':T', '事实']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
