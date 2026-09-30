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
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9512247443199158
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', ' animals', '___', ' humans', 'dogs', '四肢', ' Dogs', ' canine', ' ears', ' Animals', '尾巴', ' furry', ' Humans', ' tails', '____', '动物', ' leash', ' limbs', ' teeth', '__', ' pets', ' Gecko', '__.', '犬', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0567203 | 0.944858    |    0.00135522 |
|       2 | -4.30672   | 0.0134777   |    0.00135517 |
|       1 | -4.43172   | 0.011894    |    0.00135517 |
|       0 | -4.93172   | 0.00721408  |    0.00135517 |
|       3 | -5.05672   | 0.00636641  |    0.00135517 |
|       8 | -5.05672   | 0.00636641  |   -0.123645   |
|       6 | -5.30672   | 0.00495816  |   -0.123645   |
|       5 | -6.18172   | 0.00206687  |    0.00135517 |
|       9 | -6.93172   | 0.00097632  |    0.126355   |
|       7 | -7.05672   | 0.000861599 |    0.00135517 |

Final-decode readout: [' facts', ' factual', ' hypothesis', ' Fakta', '事实', ' fakta', ' Facts', ' statement', '这段话', '上述事实', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', ' hypotheses', ' inference', ' premise', '_fact', ' факт', ' sentence', ' implication', ' Statement', ' entail', ' conclusion', '事實', ' imply', '这句话', ' assertion', '這句話', ' Statements']

Coverage: 32 calls; prompt slice 0:, then one position per decode.

Written by PI/OpenAI.
