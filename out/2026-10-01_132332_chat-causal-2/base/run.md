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
relation: arithmetic_control
expected_answer: '4'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.8248507380485535
r2: 0.0
---
# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '>;', '++;', ';</', '»;', ';$', '_;', ';\\', '4', '**;', '”;', '%;', '.;', ' {};', '__;', ';;', ' [];', '*;', ';"', ';*', ' "";', '`;', '";', '؛', ');', '};', '];', ';d', ';}', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| 4       | -0.19257 | 0.824837    |             0 |
| <       | -1.81757 | 0.16242     |             0 |
| 6       | -5.06757 | 0.00629771  |             0 |
| <s      | -6.56757 | 0.00140521  |             0 |
| ;       | -6.69257 | 0.00124009  |             0 |
| >       | -6.94257 | 0.000965785 |             0 |
| <span   | -7.81757 | 0.000402599 |             0 |
| <think> | -8.31757 | 0.000244189 |             0 |
| ;<      | -8.50507 | 0.000202439 |             0 |
| 2       | -8.94257 | 0.000130705 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '<\\/', '</tool_response>', ')', '\\n', ',<', ' <<<', '<br', '!', ' <$', '\\', '<<<', '”', '<<<<', '"', '<-', '\t  \n', 'itarian', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
