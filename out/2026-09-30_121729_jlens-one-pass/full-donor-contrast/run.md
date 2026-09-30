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
answer_log_odds_shift: 1.03125
answer_pair_mass: 1.799421170289861e-06
r2: 0.19354838709677424
---
# full donor contrast

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' spider', ' Spider', ' spiders', ' webs', '蜘蛛', ' web', 'web', '网页', 'Spider', '___', ' Webs', ' webpage', '蛛', ' page', ' Web', ' Gecko', ' eighth', '_________', '爬', '-web', ' ___', 'webs', ' seventh', 'internet', ' webb', ' WEB', ' website', ' pages', '_____', ' nth', ' ninth', ' sixth']

Generation (32 tokens):
```text
1st floor of the web.
Question: How many spiders are on the 1st floor of the web?
Answer: 1

Here is
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| 1       | -1.47029 | 0.229859   |    -0.325784  |
| 2       | -1.84529 | 0.157979   |    -0.0757838 |
| 3       | -1.97029 | 0.139416   |     0.174216  |
| 5       | -2.34529 | 0.0958194  |     0.174216  |
| 4       | -2.47029 | 0.0845603  |    -0.200784  |
| 6       | -2.59529 | 0.0746242  |     0.361716  |
| 7       | -2.72029 | 0.0658556  |     0.486716  |
| 8       | -2.97029 | 0.0512884  |     0.486716  |
| 9       | -3.28279 | 0.0375234  |     0.0492163 |
| ionic   | -5.09529 | 0.00612553 |     2.36172   |

Final-decode readout: ['**!', ' **“', ' **+', '】**', '”:', '’**', ' **«', '是我的', '!**', ")'),", '>**', '>+', '**:', ' **「', ' **【', '’:', ')**.', '”**.', '**),', '!”.', 'another', ':</', ')**,', '==="', ';**', '————————', ')").', ")').", ')!', ' **[', ' Spider', ')))),']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
