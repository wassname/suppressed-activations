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
expected_answer: 'control'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.25
answer_pair_mass: 0.8056339621543884
r2: 0.0
---
# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', ';</', '++;', '»;', '_;', ';$', '**;', ';\\', '”;', '%;', '4', '.;', ' {};', '__;', ' [];', ';;', '*;', ';"', ';*', '`;', ');', ' "";', '";', '؛', '};', '];', ';}', ';d', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.216147 | 0.805617    |    -0.0235776 |
| <       | -1.71615  | 0.179757    |     0.101422  |
| 6       | -4.84115  | 0.00789799  |     0.226422  |
| <s      | -6.59115  | 0.00137246  |    -0.0235777 |
| ;       | -6.59115  | 0.00137246  |     0.101422  |
| >       | -6.96615  | 0.00094328  |    -0.0235777 |
| <span   | -7.71615  | 0.000445574 |     0.101422  |
| <think> | -8.34115  | 0.000238499 |    -0.0235777 |
| ;<      | -8.52865  | 0.000197722 |    -0.0235777 |
| 2       | -8.84115  | 0.000144657 |     0.101422  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', ')', '<\\/', '\\n', ',<', '!', ' <<<', '\\', '<br', ' <$', '”', '<<<', '"', '<<<<', '\t  \n', '<-', 'itarian', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
