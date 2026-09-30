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
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
expected_answer: 'control'
n_tokens: 32
swap_log_odds_shift: 0.375
bare_answer_mass: 0.9399450421333313
r2: 0.0
---
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

Written by PI/OpenAI.
