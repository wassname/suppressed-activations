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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: country_properties
expected_answer: 'Tokyo'
n_tokens: 6
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.987861156463623
r2: 0.0
---
# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Seoul', 'Jakarta', ' Taipei', ' Riyadh', 'London', 'Paris', ' Kyoto', ' Tokio', 'Tok', ' Madrid', ' Nairobi', '東京', ' Honolulu', ' Beijing', '大阪', 'city', ' London', ' Tehran', '首尔', ' Ankara', ' Brasília', ' Paris', ' Islamabad', 'Madrid', ' Caracas', ' Bogotá', '京都', ' Stockholm']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0122136 | 0.987861    |             0 |
| <       | -5.63721   | 0.00356278  |             0 |
| Os      | -5.88721   | 0.0027747   |             0 |
| Ky      | -6.01221   | 0.00244866  |             0 |
| T       | -6.88721   | 0.00102075  |             0 |
| <T      | -7.63721   | 0.00048217  |             0 |
| Tokyo   | -8.76221   | 0.000156538 |             0 |
| Se      | -8.76221   | 0.000156538 |             0 |
| K       | -9.01221   | 0.000121912 |             0 |
| ;       | -9.07471   | 0.000114525 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<think>', '.', ';', '<|im_start|>', '<|file_sep|>', '  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.Category', '\t  \n', '\\n', '\\.', '<\\/', '</', '\x00', '\\', '\r\r\n', '@\\', '\\<', '｡', '.<', '。', '  \n\n', '<', '\t\n', ' -->', '.\\', ' <<<', '\n  \n']

Coverage: 6 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
