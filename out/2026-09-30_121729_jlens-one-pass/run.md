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
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton
elapsed_seconds: 12.78
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is inside to outside. Positive answer_log_odds_shift favours inside over outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes inside toward outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p(inside) |   p(outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|------------:|-------------:|-------------------:|----------:|
| Base                            |                0        | 2.43453e-06 |  1.34448e-06 |        3.77901e-06 | 0.0322581 |
| norm-matched J donor projection |                0.125    | 8.27184e-08 |  4.03138e-08 |        1.23032e-07 | 0.0322581 |
| full donor contrast             |                1.03125  | 1.50339e-06 |  2.96034e-07 |        1.79942e-06 | 0.193548  |
| matched-random delta            |                0.171875 | 4.18023e-07 |  1.94399e-07 |        6.12422e-07 | 0.806452  |

[Base](base/run.md)

# Base

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' seventh', ' page', ' sixth', ' eighth', ' fifth', ' fourth', ' list', '第', '___', ' Guinness', ' ninth', ' Biology', ' Floor', ' Planet', ' Page', ' tenth', ' planet', ' Science', ' Seventh', ' second', ' nth', ' website', ' Museum', ' List', ' Plate', ' third', ' pages', ' Body', ' Earth', ' biology', ' Fifth', ' bones']

Generation (32 tokens):
```text
10th floor of the building.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the 
```

| token                    |    log p |          p |   delta log p |
|:-------------------------|---------:|-----------:|--------------:|
| 1                        | -1.14451 | 0.318381   |             0 |
| 2                        | -1.76951 | 0.170417   |             0 |
| 3                        | -2.14451 | 0.117126   |             0 |
| 4                        | -2.26951 | 0.103363   |             0 |
| 5                        | -2.51951 | 0.0804993  |             0 |
| 6                        | -2.95701 | 0.0519743  |             0 |
| 7                        | -3.20701 | 0.0404776  |             0 |
| 9                        | -3.33201 | 0.0357214  |             0 |
| 8                        | -3.45701 | 0.031524   |             0 |
| ........................ | -6.26951 | 0.00189316 |             0 |

Final-decode readout: [' floor', ' fifth', ' basement', ' tenth', ' seventh', ' ninth', ' sixth', ' hallway', ' fourth', ' upstairs', ' eighth', ' kitchen', ' third', ' bathroom', ' Floor', ' elevator', ' ceiling', ' hotel', ' lobby', ' Fifth', ' floors', ' downstairs', ' rooftop', ' bedroom', ' stairs', ' second', ' hospital', ' next', ' restaurant', ' door', ' mansion', ' same']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

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

[full donor contrast](full-donor-contrast/run.md)

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

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' Floor', ' Science', ' page', ' floor', ' Body', '\\""', '___', ' Guinness', ' website', ' Medical', ' Page', ' Bone', ' Museum', ' Doctor', ' Planet', ' Book', ' Smithsonian', ' Zoo', ' Monday', ' Biology', ' Number', ' Tuesday', ' seventh', ' list', '\\"\\', ' Bones', ' medical', ' Spot', ' Doctors', ' Medicine', ' List', ' Top']

Generation (32 tokens):
```text
1st floor of the 1st floor of the 1st floor of the 1st floor of the 1st floor of the 1st
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       1 | -1.01585 | 0.362093   |     0.128652  |
|       2 | -1.64085 | 0.193814   |     0.128652  |
|       3 | -2.26585 | 0.103741   |    -0.121347  |
|       4 | -2.39085 | 0.0915515  |    -0.121347  |
|       5 | -2.64085 | 0.0713004  |    -0.121347  |
|       6 | -3.01585 | 0.049004   |    -0.0588474 |
|       7 | -3.39085 | 0.0336799  |    -0.183847  |
|       9 | -3.39085 | 0.0336799  |    -0.0588474 |
|       8 | -3.70335 | 0.0246407  |    -0.246347  |
|       0 | -6.26585 | 0.00190009 |     0.628653  |

Final-decode readout: ['...).', '...', '....', '.', '.....', '!.', '...\\', '….', '..."', '.…', '…', '…..', '...)', '!', ' ….', "...'", '……', ',...', '\\.', '......', '.").', ')...', '..', '...,', '…).', '...”', '.!', '.).', '.......', '...(', ' ...', '.".']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
