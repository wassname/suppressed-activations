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
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.5
answer_pair_mass: 0.4434364438056946
r2: 0.09677419354838712
---
# norm-matched J donor projection

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' spider', ' spiders', ' upside', ' middle', ' outskirts', ' abdomen', ' bottom', ' side', ' dorsal', ' highest', ' interior', ' Spider', ' outer', ' spine', ' inside', ' torso', ' lowest', '___', ' ceiling', ' axis', ' downside', '________', ' scale', ' sidelines', ' verge', ' same', ' backbone', ' biome', ' verte', ' _____', ' ________']

Generation (32 tokens):
```text
 inside.
Question: Which of the arthropods is the most likely candidate for the riddle?
Answer: The skeleton of the arthropod is
```

| token   |   log p |         p |   delta log p |
|:--------|--------:|----------:|--------------:|
| inside  | -1.2419 | 0.288834  |     0.124472  |
| outside | -1.8669 | 0.154602  |    -0.375528  |
| surface | -3.1169 | 0.0442942 |     0.686973  |
| ground  | -3.7419 | 0.023709  |    -0.125527  |
| left    | -3.7419 | 0.023709  |    -0.500527  |
| dorsal  | -3.9294 | 0.0196554 |     1.43697   |
| right   | -3.9294 | 0.0196554 |    -0.375527  |
| bottom  | -3.9919 | 0.0184646 |     0.186973  |
| same    | -4.0544 | 0.0173459 |     0.0619726 |
| floor   | -4.1169 | 0.0162949 |     0.624473  |

Final-decode readout: [' spiders', ' spider', ' Spider', '蜘蛛', 'Spider', '蛛', 'webs', ' webs', ' described', ' resembles', ' closest', ' pictured', '爬行', ' consists', ' crawled', ' crawling', ' пау', ' depicted', ' discussed', ' mentioned', ' whose', ' itself', ' crawl', ' insects', ' Webs', ' nearest', ' web', '爬虫', ' referred', ' ecosystem', ' corresponds', ' named']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
