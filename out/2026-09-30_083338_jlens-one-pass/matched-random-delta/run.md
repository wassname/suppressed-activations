---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 23
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: -0.25
bare_answer_mass: 0.9275254011154175
r2: 0.032258064516129004
---
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

Written by PI/OpenAI.
