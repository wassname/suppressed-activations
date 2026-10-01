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
answer_log_odds_shift: -0.4375
answer_pair_mass: 0.9785536527633667
r2: 0.0
---
# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ' mammals', ' humanoid', ' humans', '四肢', ' Humans', 'Humans', ';', ';\\', '**;', ';;', ';$', '人类', 'animals', '人类的', ' paw', '__;', ' Animals', ' animals', '两只', 'dogs', '动物', '__:', ' claws', ';</', '»;', '_;', '*;', '%;', '.;', '双腿']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0217072 | 0.978527    |   -0.00225691 |
| <       | -4.14671   | 0.0158164   |    0.122743   |
| 2       | -6.52171   | 0.00147116  |   -0.127257   |
| 0       | -6.64671   | 0.00129829  |    0.122743   |
| 3       | -7.39671   | 0.000613269 |    0.122743   |
| ;       | -8.02171   | 0.000328259 |    0.310243   |
| 1       | -8.39671   | 0.000225609 |    0.247743   |
| Four    | -8.52171   | 0.000199099 |   -0.127257   |
| <think> | -8.64671   | 0.000175704 |    0.247743   |
| four    | -8.95921   | 0.000128548 |   -0.0647573  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '`;', '";', '</tool_response>', ';;', '>;', ';**', ' -->', '.;', "';", '*;', '<', '</', ' <<<', '<\\/', '؛', ';<', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
