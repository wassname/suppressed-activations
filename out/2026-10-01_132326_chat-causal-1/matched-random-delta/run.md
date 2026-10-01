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
expected_answer: 'control'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.24999980628490448
answer_pair_mass: 0.9312981367111206
r2: 0.0
---
# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ' insects', ';**', '昆虫', ' Spider', ' claws', ';\\', ' venom', '爬', ' crawling', '/web', '；', '四肢', ' insect', '两只', '**;', '万只', '-web', '触角', ' mammals', '爬虫', 'bugs', '肢', '蚣', '爬行', '�', ' humanoid', ' rept']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0739806 | 0.92869     |    0.0086546  |
| 6       | -2.94898   | 0.0523931   |   -0.116345   |
| <       | -4.44898   | 0.0116905   |    0.00865459 |
| 4       | -5.94898   | 0.0026085   |   -0.241345   |
| eight   | -6.57398   | 0.00139623  |   -0.241345   |
| Eight   | -7.32398   | 0.000659532 |   -0.116345   |
| <think> | -7.94898   | 0.000353022 |   -0.116345   |
| 0       | -8.19898   | 0.000274934 |   -0.241345   |
| 1       | -8.32398   | 0.000242628 |   -0.178845   |
| <span   | -8.38648   | 0.000227928 |   -0.116345   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '--;', '<\\/', '；', '>;', '</tool_response>', ';;', '.;', ' -->', '</', ' <$', ' <<<', '<', '";', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', '<<<<', "';", '؛', '`;', './.', ';.', ')', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
