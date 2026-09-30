---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 23
readout_block_index: 23
reverse: true
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9506593346595764
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', ' animals', '___', 'dogs', ' humans', ' Dogs', ' canine', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' Humans', '动物', ' leash', ' tails', '____', ' limbs', '犬', ' Gecko', ' pets', '__.', ' teeth', '__', 'animals', '狗', ' bones', ' humanoid']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0582056 | 0.943456    |  -0.000130136 |
|       2 | -4.30821   | 0.0134577   |  -0.000130177 |
|       1 | -4.43321   | 0.0118764   |  -0.000130177 |
|       8 | -4.93321   | 0.00720337  |  -0.000130177 |
|       0 | -4.93321   | 0.00720337  |  -0.000130177 |
|       3 | -5.05821   | 0.00635696  |  -0.000130177 |
|       6 | -5.18321   | 0.00560999  |  -0.000130177 |
|       5 | -6.18321   | 0.0020638   |  -0.000130177 |
|       9 | -6.93321   | 0.000974871 |   0.12487     |
|       7 | -7.05821   | 0.00086032  |  -0.000130177 |

Final-decode readout: [' hypothesis', ' statement', ' statements', '这段话', ' hypotheses', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' hipote', ' assumption', ' sentences', '?”', ' entail', ' deduction', ' conclusion', ' выше', ' logical', ' Hyp', 'sentence']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
