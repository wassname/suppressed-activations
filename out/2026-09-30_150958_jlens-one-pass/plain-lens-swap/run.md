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
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9523676633834839
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9523676633834839
r2: 0.032258064516129004
---
# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', '___', 'dogs', '四肢', ' Dogs', ' canine', ' ears', ' Animals', '尾巴', ' furry', ' tails', ' Humans', '动物', '____', ' leash', ' teeth', ' limbs', ' Gecko', '__.', ' pets', '犬', '__', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555194 | 0.945994    |    0.00255607 |
|       2 | -4.30552   | 0.0134939   |    0.00255585 |
|       1 | -4.43052   | 0.0119083   |    0.00255585 |
|       0 | -4.93052   | 0.00722275  |    0.00255585 |
|       8 | -5.05552   | 0.00637405  |   -0.122444   |
|       3 | -5.18052   | 0.00562508  |   -0.122444   |
|       6 | -5.30552   | 0.00496412  |   -0.122444   |
|       5 | -6.30552   | 0.0018262   |   -0.122444   |
|       9 | -7.05552   | 0.000862634 |    0.00255585 |
|       7 | -7.11802   | 0.00081037  |   -0.0599442  |

Final-decode readout: [' facts', ' factual', '事实', ' hypothesis', ' Fakta', ' Facts', ' fakta', ' statement', '上述事实', '这段话', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', ' premise', ' hypotheses', '_fact', ' inference', ' факт', ' sentence', ' entail', ' Statement', '事實', ' conclusion', ' imply', ' implication', '这句话', ' Statements', 'statement', 'Statement']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
