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
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -6.75
answer_pair_mass: 0.7404972314834595
swap_log_odds_shift: -6.75
bare_answer_mass: 0.7404972314834595
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' claws', ' webs', ' insects', '蛛', ' crawling', '___', ' mammals', ' venom', '爬', ' Gecko', 'webs', ' rept', ' worms', '爬虫', ' crawl', ' web', ' snakes', ' humans', 'web', '昆虫', ' humanoid', ' ants', ' limbs', ' lizard', ' craw', ' ___', ' bugs']

Generation (32 tokens):
```text
8.
Question: How many legs does the spider that lives in the web of the spider's home is there?
Answer: The number of legs on
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.443108 | 0.642038   |      4.48997  |
|       6 | -1.56811  | 0.208439   |      3.61497  |
|       4 | -2.31811  | 0.0984596  |     -2.26003  |
|       1 | -4.06811  | 0.0171097  |      0.364967 |
|       2 | -4.69311  | 0.00915817 |     -0.385033 |
|       3 | -4.69311  | 0.00915817 |      0.364967 |
|       0 | -5.19311  | 0.00555471 |     -0.260033 |
|       5 | -5.56811  | 0.00381769 |      0.614967 |
|       7 | -5.69311  | 0.0033691  |      1.36497  |
|       9 | -6.63061  | 0.00131936 |      0.427467 |

Final-decode readout: [' spiders', ' spider', '蜘蛛', ' Spider', ' insects', 'Spider', ' crawling', ' crawl', ' webs', ' crawled', ' creatures', ' worms', ' humans', ' counted', '蛛', ' climbed', ' compared', ' craw', ' organisms', ' robots', ' **“', '爬行', ' climbing', ' belongs', ' ants', ' bugs', ' _____', '-spinner', ' climbers', '...\\', ' ___', '.\\']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
