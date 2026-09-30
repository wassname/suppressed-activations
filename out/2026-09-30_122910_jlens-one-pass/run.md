---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
prompt_slice: '-3:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
elapsed_seconds: 21.95
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                            |                  0      |     0.25503  |     0.225063  |           0.480093 | 0.0322581 |
| norm-matched J donor projection |                  0.875  |     0.214225 |     0.0788088 |           0.293033 | 0.0967742 |
| full donor contrast             |                  0.5    |     0.246953 |     0.132184  |           0.379137 | 0.0967742 |
| matched-random delta            |                  1.8125 |     0.15975  |     0.0230142 |           0.182764 | 0.0322581 |

[Base](base/run.md)

# Base

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', ' ___', '________', ' outer', ' bottom', ' _____', '_____', ' ______', ' skull', ' left', ' middle', '_.', ' right', ' upper', ' longest', ' bones', ' bone', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.36637 | 0.25503   |             0 |
| outside | -1.49137 | 0.225063  |             0 |
| left    | -3.24137 | 0.0391101 |             0 |
| right   | -3.55387 | 0.0286136 |             0 |
| ground  | -3.61637 | 0.02688   |             0 |
| surface | -3.80387 | 0.0222843 |             0 |
| far     | -3.92887 | 0.0196658 |             0 |
| end     | -4.05387 | 0.017355  |             0 |
| same    | -4.11637 | 0.0163035 |             0 |
| bottom  | -4.17887 | 0.0153157 |             0 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', '?“', ' TRUE', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', '?",', 'true', 'TRUE', ')?', '.?', '?)', ' logical', '?’', '？', '?$', ' True', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

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

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: ['_____', '________', ' ________', ' _____', '___', ' ___', ' underside', '_________', ' spider', '＿＿', '________________', ' highest', '\\xc', ' lowest', '____________', ' __________________', ' ______', ' Spider', ' abdomen', '_\\', ' ____', ' upside', ' longest', ' hardest', '...\\', '____', '?\\', ' webs', ' biome', ' fastest', '\\u', ' closest']

Generation (32 tokens):
```text
 inside of the body.
Question: Relative to the rest of the body, the skeleton of the animal that barks and is called man's best friend is
```

| token    |    log p |         p |   delta log p |
|:---------|---------:|----------:|--------------:|
| inside   | -1.39856 | 0.246953  |    -0.0321846 |
| outside  | -2.02356 | 0.132184  |    -0.532185  |
| same     | -3.02356 | 0.0486279 |     1.09282   |
| side     | -3.33606 | 0.0355769 |     0.905315  |
| surface  | -3.58606 | 0.0277073 |     0.217815  |
| other    | -3.77356 | 0.0229702 |     1.15532   |
| ground   | -3.89856 | 0.0202711 |    -0.282185  |
| dorsal   | -3.89856 | 0.0202711 |     1.46782   |
| opposite | -3.96106 | 0.0190429 |     0.530315  |
| right    | -4.27356 | 0.0139321 |    -0.719685  |

Final-decode readout: [' spiders', ' spider', ' Spider', '蜘蛛', 'Spider', ' ___', '蛛', '___', ' _____', ' ________', '_____', ' insects', '________', ' webs', ' __________________', ' **(', ' ______', '____________', ' ____', '________________', ' humans', '____', ' crawling', ' __', '_________', 'webs', ' mammals', ' web', ' ---', ' insect', ' consists', '?\\']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' upside', ' underside', ' bones', ' abdomen', ' same', ' lower', ' lowest', ' highest', ' bone', ' skull', '___', ' upper', ' side', ' bottom', ' ________', ' ____', ' _____', ' backbone', ' ___', ' middle', ' neck', '____', ' ______', ' jaw', ' torso', ' belly', ' dorsal', ' skeletal', ' nose', ' front', ' right', '________']

Generation (32 tokens):
```text
 inside.
Question: What is the inside of the skeleton of the animal that barks and is called man's best friend?
Answer:

<think>

```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.83414 | 0.15975   |      -0.46777 |
| ground  | -2.08414 | 0.124414  |       1.53223 |
| bottom  | -3.02164 | 0.0487211 |       1.15723 |
| upper   | -3.02164 | 0.0487211 |       1.40723 |
| head    | -3.27164 | 0.037944  |       1.15723 |
| lower   | -3.33414 | 0.0356451 |       1.21973 |
| floor   | -3.33414 | 0.0356451 |       1.40723 |
| top     | -3.33414 | 0.0356451 |       0.90723 |
| outside | -3.77164 | 0.0230142 |      -2.28027 |
| right   | -3.83414 | 0.0216198 |      -0.28027 |

Final-decode readout: ['"**', '”**', '）**', 'Thinking', ' Thinking', '”**,', '”**.', '思考', ' "**', '】**', ' Thought', ';**', '==="', ')**', '»**', ' Think', '".**', '"""', ' **“', ' **"', '的思考', '...**', '**)', '**),', '**', '」**', '.AI', 'Thought', '\r\n\r\n\r\n\r\n', '*****', ')**,', ' \n\n\n\n']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
