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
prompt_slice: '-3:'
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
answer_log_odds_shift: 0.8750001192092896
answer_pair_mass: 0.2930333912372589
r2: 0.09677419354838712
---
# norm-matched J donor projection

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' spider', ' spiders', ' underside', ' Spider', '蛛', '蜘蛛', ' scale', ' outskirts', ' microscopic', ' webs', ' substrate', ' spine', ' scaffold', '网页', ' largest', ' highest', ' organism', ' biome', ' axis', ' middle', ' longest', 'Spider', ' abdomen', ' backbone', ' upside', ' verte', ' verge', ' level', ' dorsal', ' torso', ' surface', ' smallest']

Generation (32 tokens):
```text
 inside.
Question: Which of the arthropods is the most likely candidate for the riddle?
Answer: The skeleton of the arthropod is
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.54073 | 0.214225  |     -0.174356 |
| surface | -2.35323 | 0.0950616 |      1.45064  |
| outside | -2.54073 | 0.0788088 |     -1.04936  |
| same    | -2.66573 | 0.0695485 |      1.45064  |
| order   | -2.79073 | 0.0613764 |      4.51314  |
| mes     | -3.60323 | 0.0272356 |      4.70064  |
| ground  | -4.10323 | 0.0165192 |     -0.486856 |
| ex      | -4.35323 | 0.0128652 |      5.01314  |
| scale   | -4.41573 | 0.0120857 |      4.95064  |
| macro   | -4.41573 | 0.0120857 |      5.57564  |

Final-decode readout: [' spiders', ' spider', ' Spider', '蜘蛛', 'Spider', '蛛', 'webs', ' webs', ' described', ' resembles', ' closest', ' pictured', '爬行', ' depicted', ' crawled', ' пау', ' discussed', ' consists', ' crawling', ' mentioned', ' itself', ' Webs', ' whose', ' web', ' crawl', '爬虫', ' insects', ' ecosystem', ' referred', ' nearest', ' sitemap', ' named']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
