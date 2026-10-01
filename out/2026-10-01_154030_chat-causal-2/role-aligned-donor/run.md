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
expected_answer: '4'
n_tokens: 4
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: 0.03125
answer_pair_mass: 4.730113634110467e-09
r2: 0.0
---
# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', '++;', '»;', ';</', ';\\', '_;', '**;', '.;', '”;', ';$', ';;', ' {};', '%;', ' [];', ';*', '*;', '__;', '؛', ';"', ');', '6', ';}', ' "";', '5', '";', '};', '`;', ';)']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0655009 | 0.936598    |   0.000222273 |
| <       | -2.8155    | 0.0598747   |   0.000222206 |
| 6       | -6.6905    | 0.00124266  |  -0.124777    |
| >       | -7.6905    | 0.000457149 |   0.000222683 |
| ;       | -7.8155    | 0.000403433 |  -0.124777    |
| <think> | -8.4405    | 0.000215942 |  -0.124778    |
| <s      | -8.5655    | 0.000190568 |   0.000222206 |
| <span   | -8.8155    | 0.000148415 |   0.125222    |
| 2       | -8.878     | 0.000139423 |   0.0627222   |
| ;<      | -9.8155    | 5.45987e-05 |   0.000222206 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '!', '\\', '<br', '<<<', ' <<<', '<<<<', '”', '\t  \n', ' <$', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '_<', '>>', '.;']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
