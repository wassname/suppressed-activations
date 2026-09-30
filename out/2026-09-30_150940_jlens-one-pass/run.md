---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
block_index: 19
residual_index: 20
readout_block_index: 23
reverse: false
swap_logits: false
plural: false
prompt_slice: '-3:'
k: 32
seed: 0
decode_scale: 1.0
donor_norm: None
donor_checkpoint: None
equal_donor_norm: false
relation: legs
elapsed_seconds: 16.74
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 19, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 8 to 4. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention: unit-direction coordinate swap. No source/donor activation extraction. Coordinate equation: h + V(swap(pinv(V)h) - pinv(V)h). Raw-score variant: h + pinv(V).T(swap(V.T h) - V.T h), swapping unnormalised lens numerators rather than guaranteed semantic features.  Schedule: prompt and continuous decode. Prompt slice -3:; decode deltas are multiplied by 1.0. Concept token strings: (' spider', ' dog').

Selection: Explicit intervention-only test: zero standalone readout benchmark cases; source/target prompts are the unchanged built-in legs relation. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |      p(4) |     p(8) |   answer_pair_mass |        r2 |
|:---------------------|------------------------:|----------:|---------:|-------------------:|----------:|
| Base                 |            -7.45058e-09 | 0.0564207 | 0.882568 |           0.938989 | 0.0322581 |
| J-lens swap          |             1.375       | 0.165361  | 0.654016 |           0.819377 | 0.0322581 |
| plain-lens swap      |            -7.45058e-09 | 0.0560619 | 0.876956 |           0.933018 | 0.0322581 |
| matched-random delta |             0.125       | 0.0634689 | 0.876161 |           0.93963  | 0.0322581 |

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

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' claws', '___', '蜘蛛', ' spider', ' paw', '爪子', '.\\', '____', ' tails', '四肢', '蛛', ' limbs', ' furry', '尾巴', 'Spider', ' animals', ').\\', ' Spider', ' mammals', ' Gecko', ' ___', ' insects', '__.', '两只', '后腿', '__', ' lizard', '双腿', ' FOUR', '\\"\\', ' venom']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.424624 | 0.654016   |    -0.299705  |
|       4 | -1.79962  | 0.165361   |     1.0753    |
|       6 | -2.04962  | 0.128783   |     1.5753    |
|       1 | -4.04962  | 0.0174289  |     0.575295  |
|       2 | -4.67462  | 0.00932903 |     0.325295  |
|       3 | -4.67462  | 0.00932903 |     0.450295  |
|       5 | -5.29962  | 0.00499347 |     0.325295  |
|       0 | -5.54962  | 0.00388892 |     0.950295  |
|       7 | -5.79962  | 0.00302869 |    -0.0497046 |
|       9 | -6.42462  | 0.00162114 |     0.137795  |

Final-decode readout: ['过程', ' Process', ' process', 'Process', 'process', '過程', '过程的', '-process', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', '过程中', ' processus', ' процесс', 'prozess', ' processes', 'PROCESS', ' proceso', '过程中的', ' processo', ' proces', 'Processes', ' Процесс', ' процесса', '/process', ' proses']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '___', '-web', ' venom', ' insects', '爬', '.\\', '爪子', '四肢', ' Gecko', ' crawling', ' limbs', ').\\', '昆虫', '____', '_web', ' claw', ' paw', ' lizard', '后腿', ' tails', ' eight', '爬虫', '触角', '�', '双腿']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.131299 | 0.876956   |   -0.00637955 |
|       4 | -2.8813   | 0.0560619  |   -0.0063796  |
|       6 | -3.3813   | 0.0340033  |    0.24362    |
|       1 | -4.6313   | 0.0097421  |   -0.00637913 |
|       2 | -5.0063   | 0.00669564 |   -0.00637913 |
|       3 | -5.2563   | 0.00521457 |   -0.131379   |
|       5 | -5.6313   | 0.00358392 |   -0.00637913 |
|       7 | -5.8813   | 0.00279116 |   -0.131379   |
|       0 | -6.4438   | 0.00159035 |    0.0561209  |
|       9 | -6.6313   | 0.00131845 |   -0.0688791  |

Final-decode readout: ['过程', ' Process', 'Process', 'process', ' process', '过程的', '過程', '-process', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', 'prozess', '过程中', ' processus', 'PROCESS', ' процесс', ' proceso', '过程中的', ' processo', ' processes', ' процесса', ' Процесс', 'Processes', ' proces', '/process', '*:']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '爬', ' venom', ' insects', '___', '爪子', ' crawling', ' Gecko', '四肢', '.\\', ' limbs', ' claw', '爬虫', '_web', ' paw', '�', '昆虫', '后腿', ' lizard', ').\\', ' eight', '网页', ' craw', '双腿', ' tails']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.132206 | 0.876161   |   -0.00728666 |
|       4 | -2.75721  | 0.0634689  |    0.117713   |
|       6 | -3.63221  | 0.0264578  |   -0.00728679 |
|       1 | -4.63221  | 0.00973326 |   -0.00728655 |
|       2 | -5.00721  | 0.00668957 |   -0.00728655 |
|       3 | -5.13221  | 0.00590352 |   -0.00728655 |
|       5 | -5.63221  | 0.00358067 |   -0.00728655 |
|       7 | -5.75721  | 0.00315993 |   -0.00728655 |
|       9 | -6.56971  | 0.00140221 |   -0.00728655 |
|       0 | -6.63221  | 0.00131725 |   -0.132287   |

Final-decode readout: ['用户', '*\\', ' *\\', ' user', '思路', '#\\', 'user', 'User', ' reasoning', ' User', '用户的', '用户需求', '/User', '#:', ' USER', '思考', '/user', '-user', 'Streamer', '(user', '//*', '/Instruction', '推理', 'Thought', '的思考', ' Users', '和用户', 'AI', '一是要', '任务', '的用户', '#.']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
