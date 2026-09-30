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
relation: legs
elapsed_seconds: 22.48
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |       p(4) |       p(8) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-----------:|-----------:|-------------------:|----------:|
| Base                            |                   0     | 0.943579   | 0.00720431 |           0.950783 | 0.0322581 |
| norm-matched J donor projection |                  -9.5   | 0.00927076 | 0.945643   |           0.954914 | 0.0322581 |
| full donor contrast             |                  -9.25  | 0.0115834  | 0.920186   |           0.931769 | 0         |
| matched-random delta            |                   0.625 | 0.877146   | 0.00358469 |           0.880731 | 0.129032  |

[Base](base/run.md)

# Base

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' tails', '动物', ' Humans', '____', ' leash', ' limbs', ' teeth', '犬', '__.', ' pets', '__', ' Gecko', 'animals', ' bones', ' humanoid', '两只']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0580755 | 0.943579    |             0 |
|       2 | -4.30808   | 0.0134594   |             0 |
|       1 | -4.43308   | 0.0118779   |             0 |
|       8 | -4.93308   | 0.00720431  |             0 |
|       0 | -4.93308   | 0.00720431  |             0 |
|       3 | -5.05808   | 0.00635778  |             0 |
|       6 | -5.18308   | 0.00561072  |             0 |
|       5 | -6.18308   | 0.00206407  |             0 |
|       7 | -7.05808   | 0.000860432 |             0 |
|       9 | -7.05808   | 0.000860432 |             0 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', ' assumption', ' hipote', ' sentences', '?”,', ' deduction', ' entail', '?”', ' logical', ' выше', ' conclusion', '以上', ' Hyp']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

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

[full donor contrast](full-donor-contrast/run.md)

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

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '___', '爪子', ' humans', ' mammals', ' ears', ' dogs', ' canine', '四肢', ' tails', ' leash', ' Humans', ' animals', ' Dogs', '尾巴', 'dogs', ' teeth', '__.', ' furry', ' Gecko', ' ___', '__', ' human', ' limbs', ' Animals', ' pets', '____', ' mamm', '.\\', ' humanoid', ' Feet']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer: The animal that barks and
```

|   token |     log p |           p |   delta log p |
|--------:|----------:|------------:|--------------:|
|       4 | -0.131082 | 0.877146    |    -0.0730065 |
|       2 | -2.88108  | 0.0560741   |     1.42699   |
|       1 | -4.00608  | 0.0182046   |     0.426993  |
|       0 | -4.00608  | 0.0182046   |     0.926993  |
|       3 | -4.13108  | 0.0160655   |     0.926993  |
|       6 | -5.38108  | 0.00460284  |    -0.198007  |
|       8 | -5.63108  | 0.00358469  |    -0.698007  |
|       5 | -5.75608  | 0.00316348  |     0.426993  |
|       9 | -6.75608  | 0.00116378  |     0.301993  |
|       7 | -7.13108  | 0.000799853 |    -0.0730066 |

Final-decode readout: ['且具有', '并具有', '并且', ' &&', ' và', '且', '并能', ' has', ' are', ' refers', '.\\"', '且在', ',and', ' consists', '并被', 'และมี', '?\\', '...\\', ' belongs', '.\\', '.and', '且有', ' isn', ' и', '-and', ',is', 'และ', ':\\"', '_and', '&&', ' was', ' és']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
