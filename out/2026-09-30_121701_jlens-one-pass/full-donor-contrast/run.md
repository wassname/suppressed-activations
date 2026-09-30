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
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -9.25
answer_pair_mass: 0.9317694306373596
swap_log_odds_shift: -9.25
bare_answer_mass: 0.9317694306373596
r2: 0.0
---
# full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' webs', '蛛', 'web', '爬', 'webs', ' web', '-web', ' Webs', ' crawling', 'Web', ' venom', '___', ' crawl', 'WEB', '蜘', ' insects', '网页', '爬虫', '_web', ' webb', ' claws', ' ___', ' Web', ' craw', 'mites', '昆虫', '攀爬']

Generation (32 tokens):
```text
8.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer: 8

Let's solve
```

| token   |      log p |          p |   delta log p |
|:--------|-----------:|-----------:|--------------:|
| 8       | -0.0831794 | 0.920186   |      4.8499   |
| 6       | -3.70818   | 0.0245221  |      1.4749   |
| 3       | -4.20818   | 0.0148734  |      0.849896 |
| 4       | -4.45818   | 0.0115834  |     -4.4001   |
| 2       | -4.70818   | 0.00902119 |     -0.400104 |
| 1       | -4.70818   | 0.00902119 |     -0.275104 |
| 7       | -5.70818   | 0.00331871 |      1.3499   |
| 5       | -5.95818   | 0.00258461 |      0.224896 |
| 9       | -6.33318   | 0.00177638 |      0.724896 |
|         | -6.58318   | 0.00138344 |      1.2874   |

Final-decode readout: ['**!', '’**', '**:', ')**.', '”**.', ' **“', '**(', '’:', ")').", ':".', '...**', '**?', '**),', ';**', '**”,', ' **[', '**.', '__:', '…**', ')**,', '!”.', '”:', ']**', '**-', '!**', '】**', ")'),", ' **‘', ':<', ' **「', '):\\', '**)']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
