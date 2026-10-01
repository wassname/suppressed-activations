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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: arithmetic_control
expected_answer: 'control'
n_tokens: 4
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: -0.125
answer_pair_mass: 5.157108073916561e-09
r2: 0.0
---
# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '4', '；', '++;', ';</', '»;', ';\\', '_;', ';$', '**;', '.;', '”;', ';;', ' {};', '%;', ';*', '6', ' [];', '؛', '__;', ';"', '*;', ' "";', '5', ');', ';}', '";', ';d', '`;', '};']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0654075 | 0.936686    |   0.000315726 |
| <       | -2.81541   | 0.0598803   |   0.000315666 |
| 6       | -6.81541   | 0.00109675  |  -0.249684    |
| >       | -7.69041   | 0.000457192 |   0.000316143 |
| ;       | -7.81541   | 0.00040347  |  -0.124684    |
| <think> | -8.19041   | 0.000277301 |   0.125316    |
| <s      | -8.44041   | 0.000215962 |   0.125316    |
| <span   | -8.94041   | 0.000130988 |   0.000315666 |
| 2       | -9.00291   | 0.000123051 |  -0.0621843   |
| ;<      | -9.81541   | 5.46038e-05 |   0.000315666 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', '”', '<<<<', '\t  \n', '.;', ' <$', ';charset', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
