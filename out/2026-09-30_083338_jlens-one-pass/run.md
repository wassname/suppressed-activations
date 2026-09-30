---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 23
residual_index: 24
k: 32
seed: 0
elapsed_seconds: 18.71
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule for this pilot: fixed block 23 (default midpoint), last-position readout, prompt-word removal only; no final-layer output mask. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, final three prompt positions plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

Selection: first four previously answer-correct English cases, plus the previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. One configuration and one causal pair, not a generalisation rate.

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

| condition            |   swap_log_odds_shift |        p4 |       p8 |   bare_answer_mass |        r2 |
|:---------------------|----------------------:|----------:|---------:|-------------------:|----------:|
| Base                 |          -7.45058e-09 | 0.0564207 | 0.882568 |           0.938989 | 0.0322581 |
| J-lens swap          |           2.25        | 0.341548  | 0.563117 |           0.904665 | 0.0322581 |
| plain-lens swap      |           0.875       | 0.124587  | 0.812411 |           0.936999 | 0.0322581 |
| matched-random delta |          -0.25        | 0.0439887 | 0.883537 |           0.927525 | 0.0322581 |

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

Prefill readout: [' dog', ' dogs', 'dog', 'Dog', ' Dog', ' Dogs', '犬', 'dogs', '狗', '狗的', ' canine', ' claws', ' paw', '___', '爪子', ' animals', ' eight', '____', ' furry', '宠物', '8', '.\\', '狗狗', '后腿', '动物', 'DOG', '4', ' pets', ' Animals', '6', ' puppy', ' seven']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.574267 | 0.563117   |    -0.449348  |
|       4 | -1.07427  | 0.341548   |     1.80065   |
|       6 | -3.32427  | 0.0359989  |     0.300652  |
|       1 | -4.07427  | 0.0170047  |     0.550653  |
|       2 | -4.44927  | 0.0116871  |     0.550653  |
|       3 | -4.57427  | 0.0103139  |     0.550653  |
|       5 | -5.07427  | 0.00625567 |     0.550653  |
|       0 | -5.19927  | 0.00552061 |     1.30065   |
|       7 | -5.69927  | 0.00334842 |     0.0506525 |
|       9 | -6.38677  | 0.00168369 |     0.175653  |

Final-decode readout: ['*\\', '用户', ' *\\', ' reasoning', '#\\', '思路', ' user', 'user', '用户需求', '思考', '用户的', ' User', 'User', '#:', ' USER', '推理', 'Thought', '的思考', '//*', '/User', 'Streamer', '-user', '(user', '/user', ';**', ' Thought', '和用户', '**-', '/Instruction', '#.', '1', ' Users']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' claws', ' spiders', '___', '爪子', '蜘蛛', ' paw', ' dogs', 'dogs', '.\\', 'dog', '蛛', '____', ' dog', '后腿', ' furry', ' venom', ' limbs', '四肢', 'Dog', ').\\', ' eight', ' insects', '-web', ' Dogs', ' tails', ' ___', '-legged', '犬', '两只', '饲养', '爬', ' Gecko']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.207748 | 0.812411   |    -0.0828293 |
|       4 | -2.08275  | 0.124587   |     0.792171  |
|       6 | -3.70775  | 0.0245327  |    -0.0828292 |
|       1 | -4.45775  | 0.0115884  |     0.167171  |
|       2 | -4.83275  | 0.0079646  |     0.167171  |
|       3 | -5.08275  | 0.00620284 |     0.042171  |
|       5 | -5.45775  | 0.00426314 |     0.167171  |
|       7 | -5.83275  | 0.00293001 |    -0.082829  |
|       0 | -6.33275  | 0.00177714 |     0.167171  |
|       9 | -6.52025  | 0.0014733  |     0.042171  |

Final-decode readout: ['*\\', '用户', ' *\\', '思路', ' reasoning', '#\\', ' user', 'user', '用户需求', '思考', '用户的', '#:', ' USER', ' User', 'User', '的思考', '推理', 'Thought', '/User', '//*', '-user', 'Streamer', '(user', '/user', '**-', ';**', '和用户', ' Thought', '/Instruction', ' Users', '#.', '1']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', '蛛', ' claws', '-web', '爬', ' insects', ' venom', ' Gecko', '___', ' crawling', ' limbs', '�', '双腿', '四肢', '-legged', ' eight', '昆虫', '后腿', '爬虫', '网页', 'Spinner', '_web', '-leg', ' FOUR', 'ウェブ', '爪子', '肢', '/web']

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
|       8 | -0.123823 | 0.883537   |    0.00109668 |
|       4 | -3.12382  | 0.0439887  |   -0.248903   |
|       6 | -3.37382  | 0.0342584  |    0.251097   |
|       1 | -4.49882  | 0.0111221  |    0.126097   |
|       2 | -4.62382  | 0.0098152  |    0.376097   |
|       3 | -5.12382  | 0.00595322 |    0.00109673 |
|       5 | -5.62382  | 0.00361081 |    0.00109673 |
|       7 | -5.74882  | 0.00318653 |    0.00109673 |
|       9 | -6.62382  | 0.00132834 |   -0.0614033  |
|       0 | -6.81132  | 0.00110124 |   -0.311403   |

Final-decode readout: ['**:', '»:', '*:', ':**', '”:', '__:', '):', '：**', ':.', ']:', '.):', ':\\', '>:', '：', ':', ':</', '":', '+:', '’:', '():', '#:', ':")', ':".', '.:', '}:', '!:', ' **:', '):**', '\\":', ':user', '):\\', '**!']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.
