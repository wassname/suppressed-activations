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
relation: country_properties
expected_answer: 'Stockholm'
n_tokens: 5
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: -1.9371509552001953e-07
answer_pair_mass: 0.8041914105415344
r2: 0.0
---
# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', ' Prague', 'Paris', 'Berlin', ' Budapest', 'Sweden', ' Madrid', ' Munich', ' Zurich', ' Rotterdam', ' Jakarta', ' Minneapolis', ' Lisbon', ' London', ' Bratis', 'Madrid', 'openhagen', 'Barcelona', ' Edinburgh', ' Vienna', ' Barcelona', '瑞典', ' Sweden', ' Paris', ' Frankfurt', ' Bangkok']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Stock   | -0.217921 | 0.804189    |             0 |
| <       | -1.71792  | 0.179439    |             0 |
| Go      | -5.71792  | 0.00328654  |             0 |
| ;       | -5.84292  | 0.00290036  |             0 |
| Os      | -6.21792  | 0.00199338  |             0 |
| St      | -6.40542  | 0.00165257  |             0 |
| O       | -7.21792  | 0.000733325 |             0 |
| Sweden  | -7.40542  | 0.000607948 |             0 |
| <p      | -7.90542  | 0.000368739 |             0 |
| <span   | -8.09292  | 0.000305695 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '<|file_sep|>', '\t  \n', '.Category', ';**', '</tool_response>', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', ' **.**', '.', '</', ';', '.<', ';<', '<\\/', '**', ';</', ',<', ' <<<', '@\\', '<<<<', '="<', './.', '<<<', '\t\n', ' **■', '#/', ' <$']

Coverage: 5 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
