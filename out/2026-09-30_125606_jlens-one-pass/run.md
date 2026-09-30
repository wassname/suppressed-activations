---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
elapsed_seconds: 28.60
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 8 to 4. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -1: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |      p(4) |     p(8) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|----------:|---------:|-------------------:|----------:|
| Base                            |            -7.45058e-09 | 0.0564207 | 0.882568 |           0.938989 | 0.0322581 |
| norm-matched J donor projection |             3.125       | 0.299158  | 0.205608 |           0.504766 | 0.0322581 |
| full donor contrast             |             3.375       | 0.336462  | 0.180095 |           0.516557 | 0.129032  |
| matched-random delta            |             0.375       | 0.0800746 | 0.860883 |           0.940958 | 0.0967742 |

[Base](base/run.md)

# Base

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '___', ' venom', '爬', ' insects', '.\\', ' crawling', '四肢', '爪子', ' Gecko', ' limbs', '_web', ').\\', '网页', '昆虫', '�', '爬虫', ' claw', '____', ' eight', '后腿', ' lizard', '双腿', ' paw', '触角']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.124919 | 0.882568   |             0 |
|       4 | -2.87492  | 0.0564207  |             0 |
|       6 | -3.62492  | 0.0266513  |             0 |
|       1 | -4.62492  | 0.00980445 |             0 |
|       2 | -4.99992  | 0.00673849 |             0 |
|       3 | -5.12492  | 0.0059467  |             0 |
|       5 | -5.62492  | 0.00360685 |             0 |
|       7 | -5.74992  | 0.00318304 |             0 |
|       0 | -6.49992  | 0.00150356 |             0 |
|       9 | -6.56242  | 0.00141246 |             0 |

Final-decode readout: ['**:', '»:', '*:', ':**', '”:', '__:', '):', ':.', '：**', ':\\', ']:', '.):', '>:', ':', '：', ':</', '’:', '":', '+:', ':")', '#:', '():', ':".', '.:', '!:', '}:', ' **:', '):**', ':user', '):\\', '\\":', ')):']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

# norm-matched J donor projection

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['___', '____', ' ___', '.\\', ' ____', ' ______', ' __', '\\"', ' dogs', '__', ' claws', ' paw', '__.', '_________', '\\n', '?\\', '.\\"', '________', ' animals', '\\"\\', ' ________', ' Dogs', ' _____', ' \\"', '爪子', '____________', 'dogs', '_____', '_.', ').\\', '\\_', '。\\']

Generation (32 tokens):
```text
6.
Question: How many legs does the animal that spins webs have?
Options:
A. 4
B. 6
C.
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       6 | -1.08178 | 0.33899    |      2.54313  |
|       4 | -1.20678 | 0.299158   |      1.66813  |
|       8 | -1.58178 | 0.205608   |     -1.45687  |
|       2 | -2.95678 | 0.0519858  |      2.04314  |
|       1 | -3.20678 | 0.0404866  |      1.41814  |
|       0 | -3.83178 | 0.0216709  |      2.66814  |
|       3 | -3.95678 | 0.0191245  |      1.16814  |
|       5 | -4.70678 | 0.00903378 |      0.918135 |
|       7 | -5.20678 | 0.00547927 |      0.543135 |
|       9 | -5.83178 | 0.00293284 |      0.730635 |

Final-decode readout: [' Unknown', ' unknown', ' Cannot', ' Depends', ' unspecified', ' Anything', ' Dogs', ' unsure', ' None', 'Unknown', ' Undefined', 'unknown', ' undefined', ' dogs', ' undecided', ' uncertain', ' Unsure', ' Something', '未知', ' Dog', ' indefinite', ' depends', ' Doesn', ' unclear', ' UNKNOWN', ' cannot', 'Cannot', ' anything', '不确定', ' dog', ' none', ' Nothing']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['.\\', '____', '___', '.\\"', '\\"\\', '__.', '。\\', ').\\', '__', '\\"', ' claws', ' ____', ' __', '\\n', ' ___', ' spiders', ' ______', '.__', '爪子', ' paw', ' \\"', '?\\', '\\")', ' dogs', '.*', '\\""', '_________', ' animals', '\\_', '____________', '_.', ' Dogs']

Generation (32 tokens):
```text
4.
Question: What is the name of the animal that spins webs?
Answer: The animal that spins webs is a dog.
The answer is
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       4 | -1.08927 | 0.336462   |      1.78565  |
|       6 | -1.21427 | 0.296926   |      2.41065  |
|       8 | -1.71427 | 0.180095   |     -1.58935  |
|       2 | -2.46427 | 0.0850708  |      2.53565  |
|       1 | -3.08927 | 0.0455351  |      1.53565  |
|       0 | -3.83927 | 0.0215093  |      2.66065  |
|       3 | -4.08927 | 0.0167514  |      1.03565  |
|       5 | -4.71427 | 0.0089664  |      0.910649 |
|       7 | -5.33927 | 0.00479937 |      0.410649 |
|       9 | -6.08927 | 0.00226706 |      0.473149 |

Final-decode readout: [':\\"', ' answers', ' answer', ':\\', '____', '?\\', '正确答案', 'answer', ' correct', ' isn', ' ____', ':"', '-answer', '是否正确', '答案', '\\"\\', ' incorrect', '的答案', '.\\', '\\n', ':', '...\\', ' Answer', ' should', ':__', ' seems', '=\\"', 'correct', 'answers', ' was', '\\":', '\\"']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', '___', '蛛', ' claws', '.\\', ' ___', '...\\', ').\\', '爬', '\\"', '-web', '.\\"', '\\"\\', ' eight', ' Gecko', ' venom', ' crawling', '____', '__.', '__', '?\\', ' __', '\\n', ' insects', '\\""', '。\\', '爪子', ' seven']

Generation (32 tokens):
```text
8.
Question: How many legs does the animal that spins webs have?
Answer: The animal that spins webs has 8 legs.

Fact:
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| 8       | -0.149796 | 0.860883   |     -0.024877 |
| 4       | -2.5248   | 0.0800746  |      0.350123 |
| 1       | -4.3998   | 0.0122798  |      0.225123 |
| 2       | -4.3998   | 0.0122798  |      0.600123 |
| 6       | -4.5248   | 0.0108369  |     -0.899877 |
| 3       | -5.0248   | 0.00657293 |      0.100123 |
| 0       | -5.1498   | 0.00580059 |      1.35012  |
|         | -5.7748   | 0.00310483 |      1.22512  |
| 5       | -6.0248   | 0.00241804 |     -0.399877 |
| 7       | -6.2123   | 0.00200463 |     -0.462377 |

Final-decode readout: [':', ':\\', '：', '*:', ' Facts', '__:', ':*', ':...', ':\\"', '\\":', ':The', '\\:', '#:', '!:', '_:', ':F', '：**', "':", '’:', ' :', ':**', '.:', '$:', ':&', ':\\\\', ' **:', 'facts', ':$', ':A', ' _:', ':T', '事实']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
