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
expected_answer: 'Stockholm'
n_tokens: 6
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9875806570053101
r2: 0.0
---
# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Seoul', 'Jakarta', ' Taipei', ' Riyadh', 'London', ' Kyoto', ' Tokio', 'Paris', ' Madrid', ' Nairobi', 'Tok', ' Honolulu', ' Beijing', 'city', '東京', '大阪', ' London', ' Tehran', ' Ankara', ' Paris', '首尔', ' Brasília', ' Islamabad', ' Caracas', 'Madrid', ' Bogotá', ' Stockholm', '杭州']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0124976 | 0.98758     |  -0.000284002 |
| Os      | -5.7625    | 0.00314325  |   0.124716    |
| <       | -5.7625    | 0.00314325  |  -0.125284    |
| Ky      | -5.8875    | 0.00277391  |   0.124716    |
| T       | -6.8875    | 0.00102046  |  -0.000283718 |
| <T      | -7.6375    | 0.000482033 |  -0.000283718 |
| Tokyo   | -8.7625    | 0.000156493 |  -0.000284195 |
| Se      | -8.825     | 0.000147012 |  -0.0627842   |
| ;       | -8.95      | 0.000129737 |   0.124716    |
| K       | -8.95      | 0.000129737 |   0.0622158   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '</tool_response>', '.', ';', '<|im_start|>', '<|file_sep|>', '  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.Category', '\t  \n', '\\n', '\\.', '<\\/', '</', '\x00', '\\', '\r\r\n', '@\\', '｡', '\\<', ' -->', '。', '.<', '  \n\n', '\t\n', '<', '.ht', '.\\', '\n  \n']

Coverage: 6 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
