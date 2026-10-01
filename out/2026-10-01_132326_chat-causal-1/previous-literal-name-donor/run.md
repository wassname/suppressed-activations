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
expected_answer: '4'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.2500001788139343
answer_pair_mass: 0.9354551434516907
r2: 0.0
---
# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', ';**', 'Spider', ' insects', '昆虫', ' Spider', ';\\', ' claws', '；', '**;', ' venom', '爬', ' crawling', ' mammals', '/web', '两只', ' insect', ' humanoid', '四肢', '*;', '万只', '肢', ' rept', '-web', '蚣', '爬虫', '触角', ' Creatures', '爬行']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0713423 | 0.931143    |     0.0112929 |
| 6       | -3.07134   | 0.0463589   |    -0.238707  |
| <       | -4.44634   | 0.0117214   |     0.0112929 |
| 4       | -5.44634   | 0.00431205  |     0.261293  |
| eight   | -6.07134   | 0.00230807  |     0.261293  |
| Eight   | -6.82134   | 0.00109026  |     0.386293  |
| 0       | -7.69634   | 0.000454486 |     0.261293  |
| <think> | -7.94634   | 0.000353954 |    -0.113707  |
| 1       | -8.13384   | 0.000293439 |     0.0112925 |
| <span   | -8.32134   | 0.000243269 |    -0.0512075 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '；', '--;', '>;', '<\\/', '.;', ';;', '</tool_response>', ' -->', ' <$', '</', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', "';", '؛', '`;', '。', '<<<<', ';.', './.', '.<']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
