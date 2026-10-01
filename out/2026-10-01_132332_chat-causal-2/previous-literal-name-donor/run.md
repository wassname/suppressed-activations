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
answer_log_odds_shift: -0.375
answer_pair_mass: 0.7633314728736877
r2: 0.0
---
# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '>;', ';</', '4', '»;', '++;', ';$', ';\\', '_;', '”;', '**;', '%;', '.;', ';;', '__;', ' {};', ';"', ' [];', '*;', ';*', '";', '`;', ' "";', '؛', '6', ');', ';d', ';}', '];', '};']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.270087 | 0.763313    |    -0.0775176 |
| <       | -1.52009  | 0.218693    |     0.297482  |
| 6       | -4.64509  | 0.00960869  |     0.422482  |
| <s      | -6.27009  | 0.00189206  |     0.297482  |
| ;       | -6.39509  | 0.00166974  |     0.297482  |
| >       | -6.64509  | 0.0013004   |     0.297482  |
| <span   | -7.52009  | 0.000542085 |     0.297482  |
| <think> | -8.08259  | 0.000308871 |     0.234982  |
| ;<      | -8.27009  | 0.000256063 |     0.234982  |
| 2       | -8.89509  | 0.000137061 |     0.0474825 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '**', '<|im_start|>', '<', '.Category', '>', '<|file_sep|>', '.<', ')', '</tool_response>', '<\\/', '\\n', '!', '<br', '\\', ',<', ' <<<', '<<<', '”', ' <$', '\t  \n', '<<<<', '"', 'itarian', ';charset', '<-']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
