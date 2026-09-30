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
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.9555986523628235
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9555986523628235
r2: 0.032258064516129004
---
# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', ' animals', '___', '四肢', ' dogs', 'dogs', ' ears', ' Animals', ' canine', ' furry', '尾巴', ' Dogs', ' Humans', ' tails', '动物', ' Gecko', '____', ' limbs', ' teeth', ' leash', ' humanoid', '__.', '__', '两只', 'animals', ' bones', ' pets', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0530233 | 0.948358    |    0.00505222 |
|       2 | -4.42802   | 0.0119381   |   -0.119948   |
|       1 | -4.55302   | 0.0105353   |   -0.119948   |
|       8 | -4.92802   | 0.0072408   |    0.00505209 |
|       0 | -5.05302   | 0.00638999  |   -0.119948   |
|       3 | -5.17802   | 0.00563914  |   -0.119948   |
|       6 | -5.17802   | 0.00563914  |    0.00505209 |
|       5 | -6.30302   | 0.00183076  |   -0.119948   |
|       9 | -7.11552   | 0.000812395 |   -0.0574479  |
|       7 | -7.17802   | 0.000763175 |   -0.119948   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' hypothesis', ' Facts', ' statement', '上述事实', '这段话', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', '_fact', ' inference', ' факт', ' hypotheses', ' premise', ' sentence', '事實', ' entail', ' Statement', '这句话', ' implication', ' conclusion', ' imply', ' Statements', '陈述', ' assertion']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
