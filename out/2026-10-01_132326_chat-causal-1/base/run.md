---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: false
country_swap: false
coordinate_kind: None
reverse: false
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
vjp_checkpoint: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_132306_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: joint_properties
expected_answer: '8'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 1.9371509552001953e-07
answer_pair_mass: 0.9240074753761292
r2: 0.0
---
# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ';**', ' insects', ' Spider', '昆虫', ' claws', ';\\', ' venom', '爬', '；', ' crawling', '**;', '/web', ' insect', '两只', '-web', '四肢', '万只', ' mammals', '爬虫', '触角', '爬行', '肢', 'bugs', ' rept', '�', '蚣', ' humanoid']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0826352 | 0.920687    |             0 |
| 6       | -2.83264   | 0.0588575   |             0 |
| <       | -4.45764   | 0.0115897   |             0 |
| 4       | -5.70764   | 0.00332051  |             0 |
| eight   | -6.33264   | 0.00177734  |             0 |
| Eight   | -7.20764   | 0.000740907 |             0 |
| <think> | -7.83264   | 0.000396579 |             0 |
| 0       | -7.95764   | 0.00034998  |             0 |
| 1       | -8.14513   | 0.000290144 |             0 |
| <span   | -8.27013   | 0.000256051 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '<\\/', '；', '--;', '</tool_response>', '>;', ';;', '.;', '</', ' -->', ' <$', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', "';", '<<<<', '`;', ')', '؛', './.', ';.', '。']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
