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
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9539009928703308
r2: 0.032258064516129004
---
# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' animals', ' humans', '___', '四肢', ' dogs', ' ears', ' Animals', '尾巴', 'dogs', ' canine', ' furry', ' tails', ' Humans', ' Dogs', '动物', '____', ' limbs', ' leash', ' Gecko', ' teeth', '__.', '__', ' humanoid', ' bones', ' pets', '两只', 'animals', '兽医']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0539107 | 0.947517    |    0.00416481 |
|       2 | -4.42891   | 0.0119275   |   -0.120835   |
|       1 | -4.42891   | 0.0119275   |    0.0041647  |
|       0 | -4.92891   | 0.00723438  |    0.0041647  |
|       8 | -5.05391   | 0.00638432  |   -0.120835   |
|       3 | -5.17891   | 0.00563414  |   -0.120835   |
|       6 | -5.30391   | 0.00497211  |   -0.120835   |
|       5 | -6.30391   | 0.00182914  |   -0.120835   |
|       9 | -7.05391   | 0.000864023 |    0.0041647  |
|       7 | -7.11641   | 0.000811675 |   -0.0583353  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', '陈述', ' inference', ' assertion', ' Sentence', ' premise', ' prediction', ' assumption', ' hipote', '?”,', ' sentences', ' entail', '?”', ' deduction', ' logical', ' выше', ' conclusion', '同志为', ' Hyp']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
