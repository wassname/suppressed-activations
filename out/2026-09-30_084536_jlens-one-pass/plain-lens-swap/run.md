---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
expected_answer: '8'
n_tokens: 32
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9506462812423706
r2: 0.032258064516129004
---
# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', '____', ' leash', ' teeth', ' limbs', ' Gecko', '__.', '__', ' pets', '犬', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0582194 | 0.943443    |  -0.000143856 |
|       2 | -4.30822   | 0.0134575   |  -0.000144005 |
|       1 | -4.43322   | 0.0118762   |  -0.000144005 |
|       8 | -4.93322   | 0.00720328  |  -0.000144005 |
|       0 | -4.93322   | 0.00720328  |  -0.000144005 |
|       3 | -5.05822   | 0.00635687  |  -0.000144005 |
|       6 | -5.18322   | 0.00560992  |  -0.000144005 |
|       5 | -6.18322   | 0.00206377  |  -0.000144005 |
|       9 | -6.93322   | 0.000974857 |   0.124856    |
|       7 | -7.05822   | 0.000860309 |  -0.000144005 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', ' Statement', '这段话', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' assumption', ' hipote', ' deduction', '?”,', '?”', ' entail', ' sentences', ' выше', ' conclusion', ' logical', ' Hyp', '以上']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

Written by PI/OpenAI.
