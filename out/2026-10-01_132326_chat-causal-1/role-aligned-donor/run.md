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
answer_log_odds_shift: 0.12500019371509552
answer_pair_mass: 0.9242722988128662
r2: 0.0
---
# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ';**', ' insects', '昆虫', ' Spider', ' claws', ';\\', '爬', ' venom', ' crawling', '；', '两只', '**;', '/web', '四肢', ' insect', ' mammals', '万只', '-web', '爬虫', 'bugs', ' rept', ' humanoid', '肢', '触角', '爬行', '蚣', '�']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0828269 | 0.92051     |  -0.000191726 |
| 6       | -2.83283   | 0.0588463   |  -0.000191689 |
| <       | -4.45783   | 0.0115875   |  -0.000191689 |
| 4       | -5.58283   | 0.00376192  |   0.124808    |
| eight   | -6.45783   | 0.0015682   |  -0.125192    |
| Eight   | -7.20783   | 0.000740765 |  -0.000191689 |
| 0       | -7.70783   | 0.000449297 |   0.249808    |
| <think> | -8.08283   | 0.000308797 |  -0.250191    |
| 1       | -8.08283   | 0.000308797 |   0.0623083   |
| <span   | -8.39533   | 0.000225921 |  -0.125192    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '<\\/', '；', '--;', '>;', '</tool_response>', ';;', '.;', '</', ' -->', ' <$', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', '<<<<', "';", '。', '`;', './.', '؛', ')', ';.']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
