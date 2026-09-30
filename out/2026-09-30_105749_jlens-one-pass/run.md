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
elapsed_seconds: 19.34
---
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt

# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Random uses one fixed seed0 direction at the same absolute norm as the projection, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: J-lens recovers hidden words better than the same-layer plain lens. The swap should change 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                        |   swap_log_odds_shift |        p4 |         p8 |   bare_answer_mass |        r2 |
|:---------------------------------|----------------------:|----------:|-----------:|-------------------:|----------:|
| Base                             |                 0     | 0.943579  | 0.00720431 |           0.950783 | 0.0322581 |
| J-projected donor contrast       |                -5.25  | 0.0983349 | 0.143076   |           0.241411 | 0.0322581 |
| full donor contrast              |                -9.25  | 0.0115834 | 0.920186   |           0.931769 | 0         |
| norm-matched full donor contrast |                -3.75  | 0.516155  | 0.167571   |           0.683727 | 0.0322581 |
| matched-random delta             |                 0.375 | 0.935038  | 0.00490663 |           0.939945 | 0         |

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

[J-projected donor contrast](j-projected-donor-contrast/run.md)

# J-projected donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' spiders', ' claws', ' spider', '蜘蛛', ' Gecko', ' Spider', 'Spider', '四肢', ' mammals', '___', ' humanoid', ' paw', '爪子', ' humans', ' limbs', ' Humans', '触角', ' venom', ' insects', '双腿', ' furry', '两只', ' rept', '__.', ' tails', ' crawling', '爬虫', '昆虫', ' lizard', '蛛', ' webs', '____']

Generation (32 tokens):
```text
6.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the fact
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       6 | -0.319376 | 0.726602   |      4.8637   |
|       8 | -1.94438  | 0.143076   |      2.9887   |
|       4 | -2.31938  | 0.0983349  |     -2.2613   |
|       1 | -4.56938  | 0.0103644  |     -0.136301 |
|       2 | -5.06938  | 0.00628634 |     -0.761301 |
|       3 | -5.06938  | 0.00628634 |     -0.011301 |
|       0 | -5.56938  | 0.00381286 |     -0.636301 |
|       5 | -5.94438  | 0.00262054 |      0.238699 |
|       7 | -6.56938  | 0.00140267 |      0.488699 |
|       9 | -7.63188  | 0.00048475 |     -0.573801 |

Final-decode readout: [' Fakta', '上述事实', ' facts', ' factual', '事实', ' fakta', ' Facts', '事实和', ' факты', ' hypothesis', '这段话', ' textual', ' statement', '的事实', ' implication', '事實', ' fatos', 'facts', '這句話', '?\\', ' факта', ' synopsis', ' statements', ' Representation', ' Fiction', ' text', ' premise', '这句话', ' sentence', ' phrase', '文本', '_fact']

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

[norm-matched full donor contrast](norm-matched-full-donor-contrast/run.md)

# norm-matched full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' claws', ' spiders', ' paw', '___', ' Gecko', ' spider', '爪子', ' mammals', '四肢', '蜘蛛', ' humans', ' animals', ' ___', ' humanoid', ' limbs', ' venom', ' furry', '两只', ' tails', ' Spider', ' teeth', 'Spider', ' rept', ' ears', ' Humans', '____', ' Animals', '动物', '__.', '爪', '_________', ' insects']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 6.
Does the fact
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.661347 | 0.516155    |     -0.603272 |
| 6       | -1.28635  | 0.276278    |      3.89673  |
| 8       | -1.78635  | 0.167571    |      3.14673  |
| 1       | -4.53635  | 0.0107125   |     -0.103272 |
| 3       | -4.53635  | 0.0107125   |      0.521728 |
| 2       | -4.78635  | 0.00834288  |     -0.478272 |
| 0       | -5.53635  | 0.0039409   |     -0.603272 |
| 5       | -5.91135  | 0.00270853  |      0.271728 |
| 7       | -6.66135  | 0.00127942  |      0.396728 |
|         | -7.34885  | 0.000643333 |      0.521728 |

Final-decode readout: [' facts', ' factual', ' Fakta', '上述事实', '事实', ' fakta', ' Facts', ' statement', '这段话', ' hypothesis', ' statements', '?”,', '事实和', '_fact', 'facts', '?”.', ' факты', '_FACT', 'statement', ' fatos', '的事实', '**?', ' inference', ' факт', '?\\', ' conclusion', ' Statements', ' sentence', ' premise', ' Statement', ' bold', ' synopsis']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', '___', ' dogs', '四肢', ' ears', ' animals', ' canine', 'dogs', ' Dogs', ' Humans', ' tails', '尾巴', ' leash', ' furry', ' Animals', ' teeth', ' limbs', '____', ' Gecko', '__.', ' pets', '__', ' humanoid', '两只', '动物', ' mamm', ' human', ' bones']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer:

<think>
Thinking Process:
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0671677 | 0.935038    |   -0.00909219 |
|       2 | -3.81717   | 0.02199     |    0.490908   |
|       1 | -4.44217   | 0.0117704   |   -0.00909233 |
|       0 | -4.69217   | 0.00916679  |    0.240908   |
|       3 | -4.81717   | 0.00808967  |    0.240908   |
|       8 | -5.31717   | 0.00490663  |   -0.384092   |
|       6 | -5.44217   | 0.00433009  |   -0.259092   |
|       5 | -6.19217   | 0.00204539  |   -0.00909233 |
|       9 | -6.94217   | 0.000966173 |    0.115908   |
|       7 | -7.19217   | 0.000752456 |   -0.134092   |

Final-decode readout: ['**:', '*:', ':.', '__:', '”:', ':**', ':\\', '’:', ':', ':*', '：**', '»:', '：', '.):', '):', '():', ']:', '+:', '*\\', ':")', '#:', '_:', ':\\\\', '.:**', '.:', ':".', '>:', ' **:**', ':{}', ' *:', ' **:', '!:']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
