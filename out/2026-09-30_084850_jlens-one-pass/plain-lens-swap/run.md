---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
k: 32
strength: 1
prompt_slice: '0:'
continuous: true
max_new_tokens: 32
seed: 0
expected_answer: '8'
n_tokens: 32
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9523460268974304
r2: 0.032258064516129004
---
# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', 'dogs', ' humans', ' canine', ' Dogs', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' tails', ' Humans', '动物', ' leash', '____', ' limbs', ' teeth', ' pets', '犬', '__.', '__', ' Gecko', 'animals', ' bones', ' humanoid', '狗']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555422 | 0.945972    |    0.00253329 |
|       2 | -4.30554   | 0.0134936   |    0.00253344 |
|       1 | -4.43054   | 0.011908    |    0.00253344 |
|       0 | -4.93054   | 0.00722259  |    0.00253344 |
|       8 | -5.05554   | 0.00637391  |   -0.122467   |
|       3 | -5.18054   | 0.00562496  |   -0.122467   |
|       6 | -5.30554   | 0.00496401  |   -0.122467   |
|       5 | -6.30554   | 0.00182616  |   -0.122467   |
|       9 | -7.05554   | 0.000862615 |    0.00253344 |
|       7 | -7.11804   | 0.000810352 |   -0.0599666  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' hipote', ' assumption', ' deduction', ' sentences', ' entail', '?”,', '?”', ' conclusion', ' Hyp', ' logical', ' выше', 'sentence']

Coverage: 32 calls; prompt slice 0:, then one position per decode.

Written by PI/OpenAI.
