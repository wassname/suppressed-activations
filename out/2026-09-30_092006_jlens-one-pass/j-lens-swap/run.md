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
expected_answer: '8'
n_tokens: 32
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9542246460914612
r2: 0.032258064516129004
---
# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', '___', ' humans', ' animals', '四肢', ' ears', '尾巴', ' Animals', ' furry', ' tails', ' Gecko', ' Humans', '____', ' limbs', '动物', '__.', 'dogs', ' dogs', ' teeth', ' leash', ' canine', ' humanoid', '__', ' bones', '两只', '爪', ' mamm', ' Dogs', 'animals']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0544622 | 0.946994    |     0.0036133 |
|       2 | -4.42946   | 0.0119209   |    -0.121387  |
|       1 | -4.42946   | 0.0119209   |     0.003613  |
|       8 | -4.92946   | 0.00723039  |     0.003613  |
|       0 | -5.05446   | 0.0063808   |    -0.121387  |
|       3 | -5.17946   | 0.00563103  |    -0.121387  |
|       6 | -5.17946   | 0.00563103  |     0.003613  |
|       5 | -6.30446   | 0.00182813  |    -0.121387  |
|       7 | -7.11696   | 0.000811227 |    -0.058887  |
|       9 | -7.11696   | 0.000811227 |    -0.058887  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' assumption', ' deduction', ' sentences', ' hipote', '?”,', ' entail', '?”', ' logical', ' выше', ' conclusion', ' Hyp', '以上']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
