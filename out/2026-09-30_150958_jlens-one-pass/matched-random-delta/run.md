---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 19
readout_block_index: 23
reverse: true
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-3:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: None
donor_norm: None
equal_donor_norm: false
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9506011605262756
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9506011605262756
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', 'dogs', '___', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', ' leash', '____', ' limbs', ' teeth', ' pets', '犬', ' Gecko', 'animals', '__.', '__', ' humanoid', '兽医', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0573761 | 0.944239    |   0.000699442 |
|       2 | -4.30738   | 0.0134688   |   0.00069952  |
|       1 | -4.43238   | 0.0118862   |   0.00069952  |
|       0 | -4.93238   | 0.00720935  |   0.00069952  |
|       3 | -5.05738   | 0.00636223  |   0.00069952  |
|       8 | -5.05738   | 0.00636223  |  -0.1243      |
|       6 | -5.18238   | 0.00561465  |   0.00069952  |
|       5 | -6.18238   | 0.00206551  |   0.00069952  |
|       9 | -6.93238   | 0.00097568  |   0.1257      |
|       7 | -7.05738   | 0.000861035 |   0.00069952  |

Final-decode readout: [' hypothesis', ' statement', ' statements', '这段话', ' Statement', ' hypotheses', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' assumption', ' deduction', '?”', ' entail', ' hipote', ' sentences', ' logical', ' conclusion', ' Hyp', ' выше', '以上']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
