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
swap_log_odds_shift: -0.125
bare_answer_mass: 0.957251787185669
r2: 0.032258064516129004
---
# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', '___', '四肢', ' animals', ' furry', ' Gecko', ' ears', '尾巴', ' Humans', ' tails', ' Animals', ' limbs', '两只', ' humanoid', '____', '__.', '爪', 'dogs', '动物', ' dogs', ' teeth', ' canine', '双腿', '__', ' spiders', ' Dogs', ' cats', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the fact
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0523033 | 0.949041    |    0.00577217 |
|       2 | -4.4273    | 0.0119467   |   -0.119228   |
|       1 | -4.8023    | 0.00821081  |   -0.369228   |
|       8 | -4.8023    | 0.00821081  |    0.130772   |
|       6 | -4.8023    | 0.00821081  |    0.380772   |
|       0 | -5.1773    | 0.0056432   |   -0.244228   |
|       3 | -5.3023    | 0.00498011  |   -0.244228   |
|       5 | -6.3023    | 0.00183208  |   -0.119228   |
|       7 | -7.3648    | 0.00063315  |   -0.306728   |
|       9 | -7.4273    | 0.000594789 |   -0.369228   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' hypothesis', ' Facts', '这段话', ' statement', '上述事实', '事实和', ' statements', ' fatos', 'facts', '的事实', ' факты', ' inference', '_fact', ' sentence', ' premise', ' hypotheses', ' факт', '这句话', ' entail', ' Statement', ' imply', ' implication', '這句話', '事實', ' Statements', ' Sentence', ' conclusion']

Coverage: 32 calls; prompt slice 0:, then one position per decode.

Written by PI/OpenAI.
