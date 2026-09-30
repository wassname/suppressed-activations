---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: 6.9019775390625
donor_checkpoint: out/2026-09-30_133218_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
elapsed_seconds: 25.82
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source) in raw residual units. Requested donor norm=6.9019775390625; a specified norm rescales this contrast and is not an unscaled component replacement. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |      p(4) |       p(8) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|----------:|-----------:|-------------------:|----------:|
| Base                            |                   0     | 0.943579  | 0.00720431 |           0.950783 | 0.0322581 |
| norm-matched J donor projection |                  -6.75  | 0.0984596 | 0.642038   |           0.740497 | 0.0322581 |
| full donor contrast             |                  -2.875 | 0.748818  | 0.101342   |           0.85016  | 0.0322581 |
| matched-random delta            |                  -0.125 | 0.907641  | 0.00785263 |           0.915493 | 0         |

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

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' claws', ' webs', ' insects', '蛛', ' crawling', '___', ' mammals', ' venom', '爬', ' Gecko', 'webs', ' rept', ' worms', '爬虫', ' crawl', ' web', ' snakes', ' humans', 'web', '昆虫', ' humanoid', ' ants', ' limbs', ' lizard', ' craw', ' ___', ' bugs']

Generation (32 tokens):
```text
8.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 4.
Does the fact
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.443108 | 0.642038   |      4.48997  |
|       6 | -1.56811  | 0.208439   |      3.61497  |
|       4 | -2.31811  | 0.0984596  |     -2.26003  |
|       1 | -4.06811  | 0.0171097  |      0.364967 |
|       2 | -4.69311  | 0.00915817 |     -0.385033 |
|       3 | -4.69311  | 0.00915817 |      0.364967 |
|       0 | -5.19311  | 0.00555471 |     -0.260033 |
|       5 | -5.56811  | 0.00381769 |      0.614967 |
|       7 | -5.69311  | 0.0033691  |      1.36497  |
|       9 | -6.63061  | 0.00131936 |      0.427467 |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' Facts', ' hypothesis', '上述事实', ' statement', '事实和', 'facts', '这段话', ' факты', '的事实', ' sentence', ' statements', ' fatos', ' implication', ' inference', '_fact', ' premise', '事實', ' imply', ' факт', ' hypotheses', ' phrase', '这句话', ' conclusion', '這句話', ' textual', ' факта', ' assertion']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', 'dogs', ' animals', ' ears', ' tails', '兽医', ' Dogs', '___', ' canine', ' teeth', '四肢', ' bones', ' furry', ' Animals', ' humans', '尾巴', ' Gecko', '爪', ' pets', ' leash', ' veterinary', '动物', ' limbs', ' veterin', '____', ' mamm', '四条', ' jaws']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Is the hypothesis
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.289259 | 0.748818   |     -0.231183 |
|       8 | -2.28926  | 0.101342   |      2.64382  |
|       6 | -3.03926  | 0.0478703  |      2.14382  |
|       1 | -3.16426  | 0.0422454  |      1.26882  |
|       2 | -3.91426  | 0.0199553  |      0.393816 |
|       3 | -4.28926  | 0.0137151  |      0.768816 |
|       0 | -4.66426  | 0.00942623 |      0.268816 |
|       5 | -4.91426  | 0.00734116 |      1.26882  |
|       7 | -5.53926  | 0.00392944 |      1.51882  |
|       9 | -5.53926  | 0.00392944 |      1.51882  |

Final-decode readout: [' hypothesis', ' statement', ' hypotheses', ' statements', '这段话', '这句话', 'Statement', 'statement', ' Statement', ' Statements', ' implication', ' prediction', '這句話', ' inference', 'Statements', '陈述', ' hipote', ' sentence', ' assertion', ' deduction', ' facts', ' premise', '?”,', ' Prediction', ' assumption', ' Hyp', '上述事实', ' Fakta', '大胆的', '以上', 'prediction', ' Sentence']

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
Options:
A. 2

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

Final-decode readout: ['  \n', '\n', ' \n', '\\n', '\t\n', '    \n', '\r\n', '<br', '   \n', '.\\', '\n                \n', '     \n', '\t  \n', '\\', ' wings', ' limbs', '        \n', '\xa0\xa0\xa0\xa0', '.<', ' \r\n', '       \n', '\n   \n', '      \n', '             \n', '\n \n', '\n                    \n', '\n            \n', '  \r\n', '            \n', '         \n', '翅膀', ' \n    \n']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
