---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -3.875
answer_pair_mass: 0.7601750493049622
swap_log_odds_shift: -3.875
bare_answer_mass: 0.7601750493049622
r2: 0.033333333333333326
---
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

Written by PI/OpenAI.
