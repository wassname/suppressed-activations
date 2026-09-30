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
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
elapsed_seconds: 27.99
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -1: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |      p(4) |       p(8) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|----------:|-----------:|-------------------:|----------:|
| Base                            |                   0     | 0.943579  | 0.00720431 |           0.950783 | 0.0322581 |
| norm-matched J donor projection |                  -6.25  | 0.0722889 | 0.285908   |           0.358197 | 0.0322581 |
| full donor contrast             |                  -3.875 | 0.555732  | 0.204443   |           0.760175 | 0.0333333 |
| matched-random delta            |                  -0.125 | 0.907641  | 0.00785263 |           0.915493 | 0.129032  |

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

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

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

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: ['___', ' spiders', ' claws', ' ___', ' spider', '蜘蛛', ' Gecko', ' paw', ' mammals', '_________', '_____', '________', ' Spider', 'Spider', ' webs', '四肢', ' **.**', ' insects', ' rept', '________________', '爪子', '**!', ' **[', '__.', ' **【', '____________', ' animals', '昆虫', ' verte', '四条', ' humanoid', ' __________________']

Generation (32 tokens):
```text
4.
Question: How many legs does a dog have?
Answer: 4

Let<|im_end|>
<|im_start|>assistant
<think>

</think>

Let follow the
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.587468 | 0.555732    |    -0.529393  |
| 8       | -1.58747  | 0.204443    |     3.34561   |
| 6       | -1.71247  | 0.18042     |     3.47061   |
| 3       | -3.96247  | 0.0190161   |     1.09561   |
| 1       | -4.21247  | 0.0148098   |     0.220607  |
| 2       | -4.33747  | 0.0130696   |    -0.0293927 |
| 0       | -5.08747  | 0.00617363  |    -0.154393  |
| 5       | -5.96247  | 0.00257355  |     0.220607  |
| 7       | -6.71247  | 0.00121566  |     0.345607  |
|         | -7.02497  | 0.000889396 |     0.845607  |

Final-decode readout: ['...**', ':**', '’:', '：**', '**:', ':\\', '**!', ':".', '):**', ' **[', ' **“', ' **:**', ":')", ']:', '”:', ' **:', '!**', '...).', '...\\', ' **.', ':)', ':]', ' **(', '**?', '_:', '__:', ':</', ':', '.):', '):\\', '…**', ':")']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '___', ' mammals', '爪子', '四肢', ' ears', ' humans', ' animals', ' dogs', ' canine', ' tails', '__.', '__', ' leash', '尾巴', ' Gecko', ' Dogs', ' Animals', ' ___', ' teeth', 'dogs', ' limbs', '____', ' Humans', ' furry', ' mamm', '.\\', ' humanoid', ' bones', '四条', '两只']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer: The animal that barks and
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0969068 | 0.907641    |    -0.0388313 |
|       2 | -3.47191   | 0.0310578   |     0.836169  |
|       1 | -3.97191   | 0.0188375   |     0.461169  |
|       0 | -4.34691   | 0.0129468   |     0.586169  |
|       3 | -4.59691   | 0.010083    |     0.461169  |
|       8 | -4.84691   | 0.00785263  |     0.0861688 |
|       6 | -5.22191   | 0.00539703  |    -0.0388312 |
|       5 | -5.84691   | 0.00288882  |     0.336169  |
|       9 | -6.84691   | 0.00106274  |     0.211169  |
|       7 | -6.97191   | 0.000937863 |     0.0861688 |

Final-decode readout: ['且具有', '并具有', '并且', ' &&', ' và', '且', '并能', ' has', ' are', '.\\"', ' refers', '且在', ',and', '并被', 'และมี', '且有', '.and', '...\\', ' и', ' belongs', '?\\', '.\\', ' consists', ' isn', '-and', ',is', 'และ', '&&', '_and', '并保持', ':\\"', ' és']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
