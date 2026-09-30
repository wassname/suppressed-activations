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
swap_log_odds_shift: -0.125
bare_answer_mass: 0.9545902013778687
r2: 0.032258064516129004
---
# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', '___', ' animals', '四肢', ' furry', '尾巴', ' ears', ' Gecko', ' Humans', ' tails', ' Animals', ' dogs', 'dogs', ' limbs', '____', ' canine', ' humanoid', '动物', ' Dogs', '__.', '两只', ' teeth', '爪', '__', ' leash', 'animals', ' mamm', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0550877 | 0.946402    |    0.00298785 |
|       2 | -4.55509   | 0.0105136   |   -0.247012   |
|       1 | -4.55509   | 0.0105136   |   -0.122012   |
|       8 | -4.80509   | 0.00818798  |    0.127988   |
|       6 | -4.80509   | 0.00818798  |    0.377988   |
|       0 | -5.05509   | 0.00637681  |   -0.122012   |
|       3 | -5.18009   | 0.00562751  |   -0.122012   |
|       5 | -6.30509   | 0.00182699  |   -0.122012   |
|       7 | -7.11759   | 0.00081072  |   -0.0595121  |
|       9 | -7.24259   | 0.000715458 |   -0.184512   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' Facts', ' hypothesis', ' statement', '上述事实', '这段话', '事实和', '的事实', 'facts', ' fatos', ' факты', ' statements', '_fact', ' inference', ' факт', ' sentence', ' premise', ' hypotheses', '事實', '这句话', ' Statement', ' entail', ' imply', ' implication', ' Statements', ' conclusion', '這句話', ' Sentence']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

Written by PI/OpenAI.
