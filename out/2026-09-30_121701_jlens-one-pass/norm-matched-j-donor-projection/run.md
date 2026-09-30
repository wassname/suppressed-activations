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
answer_log_odds_shift: -9.5
answer_pair_mass: 0.9549137949943542
swap_log_odds_shift: -9.5
bare_answer_mass: 0.9549137949943542
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', '蜘蛛', ' spider', ' Spider', 'Spider', '蛛', ' webs', 'webs', '爬', 'web', ' web', ' Webs', '网页', 'WEB', ' crawling', 'Web', '攀爬', ' crawl', '___', '爬虫', '蜘', '-web', ' insects', ' пау', '昆虫', ' venom', '_web', ' Web', ' Gecko', '__.', '数', '[number']

Generation (32 tokens):
```text
8.
Question: How many legs does the spider that lives in the web of the spider is there?
Answer: The number of legs on the animal
```

|   token |      log p |          p |   delta log p |
|--------:|-----------:|-----------:|--------------:|
|       8 | -0.0558902 | 0.945643   |    4.87719    |
|       6 | -3.93089   | 0.0196262  |    1.25219    |
|       2 | -4.68089   | 0.00927076 |   -0.372815   |
|       4 | -4.68089   | 0.00927076 |   -4.62281    |
|       1 | -5.05589   | 0.00637169 |   -0.622815   |
|       3 | -5.68089   | 0.00341052 |   -0.622815   |
|       7 | -6.05589   | 0.00234401 |    1.00219    |
|       5 | -6.18089   | 0.00206859 |    0.00218534 |
|       0 | -7.18089   | 0.00076099 |   -2.24781    |
|       9 | -7.18089   | 0.00076099 |   -0.122815   |

Final-decode readout: [' spiders', ' spider', '蜘蛛', ' Spider', '蛛', 'Spider', ' web', ' webs', ' пау', ' insects', 'webs', ' crab', ' Web', ' crawler', ' Webs', '网页', '爬', ' crawling', ' crawl', ' labyrinth', ' craw', ' asteroid', ' unicorn', 'web', '-spinner', ' giant', ' Sphinx', '爬虫', ' creatures', '攀爬', ' insect', ' creature']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
