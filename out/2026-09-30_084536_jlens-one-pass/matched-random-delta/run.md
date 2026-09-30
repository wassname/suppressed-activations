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
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9512401223182678
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' humans', ' animals', 'dogs', '___', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', ' leash', '____', ' teeth', ' limbs', ' pets', '犬', '__.', ' Gecko', '__', 'animals', ' humanoid', '兽医', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0567041 | 0.944874    |    0.00137144 |
|       2 | -4.3067    | 0.0134779   |    0.00137138 |
|       1 | -4.4317    | 0.0118942   |    0.00137138 |
|       0 | -4.9317    | 0.0072142   |    0.00137138 |
|       3 | -5.0567    | 0.00636651  |    0.00137138 |
|       8 | -5.0567    | 0.00636651  |   -0.123629   |
|       6 | -5.3067    | 0.00495824  |   -0.123629   |
|       5 | -6.1817    | 0.0020669   |    0.00137138 |
|       9 | -6.9317    | 0.000976336 |    0.126371   |
|       7 | -7.0567    | 0.000861613 |    0.00137138 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', ' Statement', '这段话', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' assumption', ' hipote', '?”', ' sentences', ' deduction', ' entail', ' logical', ' Hyp', ' conclusion', '同志为', ' выше']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

Written by PI/OpenAI.
