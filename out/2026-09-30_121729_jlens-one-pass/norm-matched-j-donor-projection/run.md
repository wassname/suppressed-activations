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
relation: skeleton
expected_answer: 'outside'
n_tokens: 32
answer_0: 'outside'
answer_1: 'inside'
answer_log_odds_shift: 0.125
answer_pair_mass: 1.2303219421028189e-07
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', '网页', ' web', ' website', ' webs', '网站', ' Webs', 'Spider', ' Web', '蛛', ' Website', '爬', 'web', 'internet', 'webs', ' webpage', ' Homepage', ' websites', ' Internet', 'website', ' Site', ' www', ' Wiki', ' Pornhub', ' WEB', ' Websites', '的网站', 'bsites', '网址']

Generation (32 tokens):
```text
10th floor of the World Spider Center.
Question: Where is the skeleton of the animal that barks and is called man's collection of spiders?
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| 1       | -1.46407 | 0.231292   |    -0.319567  |
| 3       | -1.83907 | 0.158965   |     0.305433  |
| 2       | -1.83907 | 0.158965   |    -0.0695673 |
| 4       | -2.08907 | 0.123802   |     0.180433  |
| 5       | -2.21407 | 0.109255   |     0.305433  |
| 6       | -2.71407 | 0.0662663  |     0.242933  |
| 7       | -3.02657 | 0.0484815  |     0.180433  |
| 8       | -3.21407 | 0.0401925  |     0.242933  |
| 9       | -3.52657 | 0.0294055  |    -0.194567  |
|         | -6.27657 | 0.00187983 |     0.555433  |

Final-decode readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' webs', 'webs', '蛛', ' web', '爬', ' Webs', ' crawling', ' crawl', 'web', '-web', ' Web', '爬虫', ' пау', '.?', '爬行', '?\\', 'WEB', ' climbing', ' climbs', '攀爬', ' crawled', 'Web', '/Web', ' WEB', ' craw', 'crawl', ' climb']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
