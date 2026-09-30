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
swap_log_odds_shift: -3.75
bare_answer_mass: 0.6837265491485596
r2: 0.032258064516129004
---
# norm-matched full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' claws', ' spiders', ' paw', '___', ' Gecko', ' spider', '爪子', ' mammals', '四肢', '蜘蛛', ' humans', ' animals', ' ___', ' humanoid', ' limbs', ' venom', ' furry', '两只', ' tails', ' Spider', ' teeth', 'Spider', ' rept', ' ears', ' Humans', '____', ' Animals', '动物', '__.', '爪', '_________', ' insects']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 6.
Does the fact
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.661347 | 0.516155    |     -0.603272 |
| 6       | -1.28635  | 0.276278    |      3.89673  |
| 8       | -1.78635  | 0.167571    |      3.14673  |
| 1       | -4.53635  | 0.0107125   |     -0.103272 |
| 3       | -4.53635  | 0.0107125   |      0.521728 |
| 2       | -4.78635  | 0.00834288  |     -0.478272 |
| 0       | -5.53635  | 0.0039409   |     -0.603272 |
| 5       | -5.91135  | 0.00270853  |      0.271728 |
| 7       | -6.66135  | 0.00127942  |      0.396728 |
|         | -7.34885  | 0.000643333 |      0.521728 |

Final-decode readout: [' facts', ' factual', ' Fakta', '上述事实', '事实', ' fakta', ' Facts', ' statement', '这段话', ' hypothesis', ' statements', '?”,', '事实和', '_fact', 'facts', '?”.', ' факты', '_FACT', 'statement', ' fatos', '的事实', '**?', ' inference', ' факт', '?\\', ' conclusion', ' Statements', ' sentence', ' premise', ' Statement', ' bold', ' synopsis']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
