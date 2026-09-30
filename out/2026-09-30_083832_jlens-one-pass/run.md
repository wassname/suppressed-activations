---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
k: 32
seed: 0
elapsed_seconds: 20.77
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, final three prompt positions plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

Selection: four previously answer-correct English cases, four fixed new simple English prompts, and the previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. This is the second observer layer tested; edit layer/strength remain the successful midpoint configuration. One causal pair is not a generalisation rate.

SHOULD: J-lens recovers hidden words better than the same-layer plain lens. The swap should change 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

| concept   | readout    |   hidden rank |   answer rank | joint pass   |
|:----------|:-----------|--------------:|--------------:|:-------------|
| Bulgaria  | J-lens     |           655 |           607 | False        |
| Bulgaria  | plain lens |         35232 |         64063 | False        |
| Iceland   | J-lens     |           140 |           230 | False        |
| Iceland   | plain lens |         57271 |          2035 | False        |
| Turkey    | J-lens     |          1368 |            48 | False        |
| Turkey    | plain lens |         22800 |          4673 | False        |
| Congo     | J-lens     |            13 |          6330 | True         |
| Congo     | plain lens |             0 |           360 | True         |
| Italy     | J-lens     |            63 |             3 | False        |
| Italy     | plain lens |          5820 |             0 | False        |
| Italy     | J-lens     |            25 |             4 | False        |
| Italy     | plain lens |         12847 |           177 | False        |
| dog       | J-lens     |            57 |            57 | False        |
| dog       | plain lens |         14384 |         73837 | False        |
| bird      | J-lens     |            13 |           330 | True         |
| bird      | plain lens |          6835 |        175150 | False        |

| condition            |   swap_log_odds_shift |        p4 |       p8 |   bare_answer_mass |        r2 |
|:---------------------|----------------------:|----------:|---------:|-------------------:|----------:|
| Base                 |          -7.45058e-09 | 0.0564207 | 0.882568 |           0.938989 | 0.0322581 |
| J-lens swap          |           3.25        | 0.565529  | 0.343011 |           0.90854  | 0.0322581 |
| plain-lens swap      |          -7.45058e-09 | 0.0562635 | 0.880109 |           0.936372 | 0.0322581 |
| matched-random delta |           0.25        | 0.0712676 | 0.868218 |           0.939485 | 0.0322581 |

Readout input: "The capital of the country with the national anthem 'Mila Rodino' is"

Baseline continuation (up to 8 tokens): ':\nA. Sofia\nB.'

Readout input: "The capital of the country with the national anthem 'Lofsöngur' is"

Baseline continuation (up to 8 tokens): ' Reykjavík.\nA.'

Readout input: "The country with the national anthem 'İstiklâl Marşı' is led by president"

Baseline continuation (up to 8 tokens): ' Recep Tayyip Erdoğan.\nA.'

Readout input: 'The country with Brazzaville as its capital is led by president'

Baseline continuation (up to 8 tokens): ' Denis Sassou Nguesso.\n'

Readout input: 'Fact: The capital of the country shaped like a boot is '

Baseline continuation (up to 8 tokens): 'rome.\nHypothesis: The'

Readout input: 'Fact: The currency used in the country shaped like a boot is '

Baseline continuation (up to 8 tokens): '100% gold.\nH'

Readout input: 'Fact: The number of legs on the animal that barks is '

Baseline continuation (up to 8 tokens): '4.\nHypothesis: The'

Readout input: 'Fact: The number of legs on the animal with feathers and a beak is '

Baseline continuation (up to 8 tokens): '2.\nHypothesis: The'

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

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' claws', ' spiders', ' paw', '___', '爪子', ' spider', '蜘蛛', '.\\', '____', ' tails', '四肢', ' animals', ' furry', ' mammals', '尾巴', '__.', '动物', ').\\', ' limbs', ' Gecko', '蛛', '双腿', '四条', ' ___', '后腿', ' Animals', '两只', 'Spider', ' fours', 'dogs', '__', ' rabbit']

Generation (32 tokens):
```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.569993 | 0.565529   |     2.30493   |
|       8 | -1.06999  | 0.343011   |    -0.945074  |
|       6 | -3.19499  | 0.0409668  |     0.429926  |
|       1 | -4.06999  | 0.0170775  |     0.554926  |
|       3 | -4.56999  | 0.010358   |     0.554926  |
|       2 | -4.69499  | 0.00914093 |     0.304926  |
|       0 | -5.31999  | 0.00489279 |     1.17993   |
|       5 | -5.56999  | 0.00381051 |     0.0549264 |
|       7 | -6.06999  | 0.00231119 |    -0.320074  |
|       9 | -6.50749  | 0.00149222 |     0.0549264 |

Final-decode readout: ['*\\', '用户', ' *\\', '#\\', ' reasoning', '思路', ' user', 'user', 'User', ' User', '用户的', ' USER', '/User', '用户需求', '思考', '#:', 'Streamer', '//*', '/user', '/Instruction', '-user', '推理', 'AI', '(user', '/question', '的思考', '任务', 'Thought', '**-', '链', 'Task', '#.']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '___', '-web', ' venom', ' insects', '爬', '.\\', '四肢', '爪子', ' Gecko', ' crawling', ' limbs', ').\\', '昆虫', '_web', ' claw', '____', ' lizard', '爬虫', ' eight', ' tails', ' paw', '双腿', '后腿', '网页', '�']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       8 | -0.12771 | 0.880109   |   -0.0027908  |
|       4 | -2.87771 | 0.0562635  |   -0.00279069 |
|       6 | -3.50271 | 0.0301157  |    0.122209   |
|       1 | -4.62771 | 0.00977712 |   -0.00279045 |
|       2 | -5.00271 | 0.00671971 |   -0.00279045 |
|       3 | -5.25271 | 0.00523332 |   -0.12779    |
|       5 | -5.62771 | 0.0035968  |   -0.00279045 |
|       7 | -5.75271 | 0.00317417 |   -0.00279045 |
|       0 | -6.50271 | 0.00149937 |   -0.00279045 |
|       9 | -6.56521 | 0.00140853 |   -0.00279045 |

Final-decode readout: ['**:', ':**', '»:', '*:', '”:', '__:', ':.', '):', ':\\', '.):', ']:', '：**', ':', '>:', ':</', '：', ':".', ':")', '":', '’:', '#:', '():', '+:', '.:', '!:', '}:', '):**', ' **:', '):\\', ':user', '"):', ')):']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '爬', ' venom', '___', ' crawling', '爪子', ' insects', ' Gecko', '四肢', '.\\', ' claw', '_web', ' limbs', ' paw', '爬虫', '�', ').\\', '后腿', ' lizard', '网页', '昆虫', ' eight', ' craw', '双腿', '蜘']

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
|       8 | -0.141313 | 0.868218   |    -0.0163937 |
|       4 | -2.64131  | 0.0712676  |     0.233606  |
|       6 | -3.64131  | 0.0262179  |    -0.0163937 |
|       1 | -4.64131  | 0.00964502 |    -0.0163937 |
|       2 | -5.01631  | 0.00662892 |    -0.0163937 |
|       3 | -5.14131  | 0.00585    |    -0.0163937 |
|       5 | -5.51631  | 0.00402064 |     0.108606  |
|       7 | -5.76631  | 0.00313128 |    -0.0163937 |
|       0 | -6.51631  | 0.00147911 |    -0.0163937 |
|       9 | -6.51631  | 0.00147911 |     0.0461063 |

Final-decode readout: [' Process', '过程', 'Process', ' process', 'process', '過程', '-process', '过程的', '_process', '过程和', ' Processes', '的过程', ' Prozess', ' Processo', ' PROCESS', '这个过程', 'プロセス', 'PROCESS', '过程中', 'prozess', ' processus', ' процесс', ' proceso', '过程中的', ' processes', ' processo', ' процесса', ' Процесс', ' proces', 'Processes', '*:', '/process']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.
