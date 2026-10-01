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
expected_answer: 'control'
n_tokens: 4
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.1875
answer_pair_mass: 0.9798875451087952
r2: 0.0
---
# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '**;', ' humanoid', ' mammals', ';;', ';\\', ' humans', ';$', ' Humans', '__;', '四肢', 'Humans', '_;', '*;', ';</', '.;', '»;', '%;', '>;', '人类的', '__:', ' {};', '؛', '人类', '";', ' [];', ' Animals', 'animals', '`;', ' animals']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0203389 | 0.979867    |  -0.000888612 |
| <       | -4.27034   | 0.013977    |  -0.000888824 |
| 2       | -6.27034   | 0.00189159  |   0.124111    |
| 0       | -6.52034   | 0.00147317  |   0.249111    |
| 3       | -7.39534   | 0.000614108 |   0.124111    |
| ;       | -8.14534   | 0.000290084 |   0.186611    |
| Four    | -8.20784   | 0.000272509 |   0.186611    |
| 1       | -8.52034   | 0.000199372 |   0.124111    |
| four    | -8.64534   | 0.000175945 |   0.249111    |
| <think> | -8.83284   | 0.000145864 |   0.0616112   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '`;', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>;', '";', '</tool_response>', ';;', '.;', ';**', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
