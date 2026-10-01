---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: false
country_swap: false
coordinate_kind: None
reverse: true
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
answer_log_odds_shift: 0.0
answer_pair_mass: 0.980755090713501
r2: 0.0
---
# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ' mammals', ' humanoid', ';', ' humans', '**;', ' Humans', ';\\', ';;', '四肢', ';$', 'Humans', '__;', '人类的', '_;', '__:', ';</', 'animals', '*;', '.;', '»;', '%;', ' Animals', '人类', '>;', 'dogs', ' animals', '两只', ' paw', '动物', '؛']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0194503 | 0.980738    |             0 |
| <       | -4.26945   | 0.0139895   |             0 |
| 2       | -6.39445   | 0.0016708   |             0 |
| 0       | -6.76945   | 0.00114833  |             0 |
| 3       | -7.51945   | 0.000542431 |             0 |
| ;       | -8.33195   | 0.000240702 |             0 |
| Four    | -8.39445   | 0.000226119 |             0 |
| 1       | -8.64445   | 0.000176101 |             0 |
| four    | -8.89445   | 0.000137148 |             0 |
| <think> | -8.89445   | 0.000137148 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', '`;', ';.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>;', '";', ';;', '</tool_response>', ';**', '.;', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
