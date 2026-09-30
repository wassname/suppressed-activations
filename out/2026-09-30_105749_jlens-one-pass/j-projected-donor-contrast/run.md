---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
expected_answer: '8'
n_tokens: 32
swap_log_odds_shift: -5.25
bare_answer_mass: 0.24141129851341248
r2: 0.032258064516129004
---
# J-projected donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', ' claws', ' spider', '蜘蛛', ' Gecko', ' Spider', 'Spider', '四肢', ' mammals', '___', ' humanoid', ' paw', '爪子', ' humans', ' limbs', ' Humans', '触角', ' venom', ' insects', '双腿', ' furry', '两只', ' rept', '__.', ' tails', ' crawling', '爬虫', '昆虫', ' lizard', '蛛', ' webs', '____']

Generation (32 tokens):
```text
6.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the fact
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       6 | -0.319376 | 0.726602   |      4.8637   |
|       8 | -1.94438  | 0.143076   |      2.9887   |
|       4 | -2.31938  | 0.0983349  |     -2.2613   |
|       1 | -4.56938  | 0.0103644  |     -0.136301 |
|       2 | -5.06938  | 0.00628634 |     -0.761301 |
|       3 | -5.06938  | 0.00628634 |     -0.011301 |
|       0 | -5.56938  | 0.00381286 |     -0.636301 |
|       5 | -5.94438  | 0.00262054 |      0.238699 |
|       7 | -6.56938  | 0.00140267 |      0.488699 |
|       9 | -7.63188  | 0.00048475 |     -0.573801 |

Final-decode readout: [' Fakta', '上述事实', ' facts', ' factual', '事实', ' fakta', ' Facts', '事实和', ' факты', ' hypothesis', '这段话', ' textual', ' statement', '的事实', ' implication', '事實', ' fatos', 'facts', '這句話', '?\\', ' факта', ' synopsis', ' statements', ' Representation', ' Fiction', ' text', ' premise', '这句话', ' sentence', ' phrase', '文本', '_fact']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
