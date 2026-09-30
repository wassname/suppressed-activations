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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -6.25
answer_pair_mass: 0.3581971526145935
swap_log_odds_shift: -6.25
bare_answer_mass: 0.3581971526145935
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', '蜘蛛', ' spider', ' Spider', 'Spider', ' claws', '蛛', ' Gecko', ' webs', '___', '爬', 'webs', ' mammals', ' humanoid', ' insects', '昆虫', '爬虫', ' crawling', ' venom', '四肢', '触角', ' rept', 'web', '蜘', '爪子', '__.', ' Webs', ' Humans', '双腿', '两只', ' limbs', ' crawl']

Generation (32 tokens):
```text
6.
Question: How many legs does the spider that lives in the web of the spider is there?
Answer: The number of legs on the animal
```

|   token |     log p |           p |   delta log p |
|--------:|----------:|------------:|--------------:|
|       6 | -0.502084 | 0.605268    |     4.68099   |
|       8 | -1.25208  | 0.285908    |     3.68099   |
|       4 | -2.62708  | 0.0722889   |    -2.56901   |
|       1 | -4.37708  | 0.0125619   |     0.0559912 |
|       3 | -4.87708  | 0.0076192   |     0.180991  |
|       2 | -5.00208  | 0.00672392  |    -0.694009  |
|       0 | -5.62708  | 0.00359905  |    -0.694009  |
|       5 | -5.87708  | 0.00280295  |     0.305991  |
|       7 | -6.25208  | 0.00192643  |     0.805991  |
|       9 | -7.37708  | 0.000625422 |    -0.319009  |

Final-decode readout: [' spiders', ' spider', '蜘蛛', ' Spider', '蛛', 'Spider', ' web', ' webs', ' пау', ' insects', 'webs', ' Web', ' crab', ' Webs', ' crawler', '网页', '爬', ' crawl', ' crawling', ' labyrinth', ' asteroid', ' craw', ' unicorn', '-spinner', ' Sphinx', ' Fibonacci', 'web', ' giant', '爬虫', ' worms', ' insect', ' creature']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
