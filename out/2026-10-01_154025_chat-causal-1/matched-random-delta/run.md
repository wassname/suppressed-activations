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
expected_answer: 'control'
n_tokens: 6
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: -0.125
answer_pair_mass: 0.9871717095375061
r2: 0.0
---
# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Seoul', 'Jakarta', ' Taipei', ' Riyadh', 'London', ' Kyoto', 'Paris', ' Tokio', ' Nairobi', ' Madrid', ' Honolulu', 'Tok', ' Beijing', 'city', ' London', '大阪', '東京', ' Tehran', ' Ankara', ' Paris', '首尔', ' Brasília', ' Islamabad', ' Caracas', ' Stockholm', ' Bogotá', '京都', '杭州']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0129118 | 0.987171    |  -0.000698204 |
| <       | -5.63791   | 0.0035603   |  -0.00069809  |
| Os      | -5.76291   | 0.00314195  |   0.124302    |
| Ky      | -6.01291   | 0.00244695  |  -0.00069809  |
| T       | -6.76291   | 0.00115586  |   0.124302    |
| <T      | -7.63791   | 0.000481834 |  -0.00069809  |
| Se      | -8.63791   | 0.000177257 |   0.124302    |
| Tokyo   | -8.70041   | 0.000166517 |   0.0618019   |
| ;       | -8.88791   | 0.000138048 |   0.186802    |
| K       | -8.95041   | 0.000129684 |   0.0618019   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '</tool_response>', '.', ';', '<|im_start|>', '  \n', '<|file_sep|>', '.Category', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\t  \n', '\\n', '\\.', '<\\/', '\x00', '\\', '</', '\r\r\n', '@\\', '\\<', '｡', '  \n\n', '.<', '。', ' -->', '\n  \n', '.\\', '\t\n', '<', '.ht']

Coverage: 6 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

Written by PI/OpenAI.
