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
expected_answer: '8'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.0625
answer_pair_mass: 0.9806468486785889
r2: 0.0
---
# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', ' mammals', ' humanoid', ';\\', '**;', ';;', ' humans', ';$', ' Humans', '四肢', '__;', 'Humans', '.;', '*;', '_;', ';</', '»;', '%;', '人类的', ' paw', '>;', ' Animals', 'animals', '__:', '؛', 'dogs', '人类', ' animals', '两只', '";']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0195618 | 0.980628    |   -0.00011153 |
| <       | -4.26956   | 0.0139879   |   -0.00011158 |
| 2       | -6.39456   | 0.00167062  |   -0.00011158 |
| 0       | -6.76956   | 0.0011482   |   -0.00011158 |
| 3       | -7.51956   | 0.00054237  |   -0.00011158 |
| ;       | -8.20706   | 0.000272721 |    0.124888   |
| Four    | -8.33206   | 0.000240675 |    0.0623884  |
| 1       | -8.64456   | 0.000176082 |   -0.00011158 |
| <think> | -8.70706   | 0.000165414 |    0.187388   |
| four    | -8.83206   | 0.000145977 |    0.0623884  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '`;', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '";', '>;', ';;', '</tool_response>', ';**', '.;', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
