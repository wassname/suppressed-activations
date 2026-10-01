---
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
vjp_checkpoint: None
indirect_donor: false
country_swap: false
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: false
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
donor_reflection: false
equal_donor_norm: false
relation: country_properties
elapsed_seconds: 4.70
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Tokyo to Stockholm. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. No previous-donor comparator. Seed0 random matches the new donor norm and direction sign. 9 conditions across fixed development prompts; this call covers one. Concept family, preparation wording and task changes are recorded in the config selection statement. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v1.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Tokyo toward Stockholm with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:---------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                 |                   0     |         0.987861 |        4.39682e-07 |                0.987861 |    0 |
| role-aligned donor   |                   0.125 |         0.98758  |        3.87908e-07 |                0.987581 |    0 |
| matched-random delta |                  -0.125 |         0.987171 |        4.97877e-07 |                0.987172 |    0 |

[Base](base/run.md)

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

[role-aligned donor](role-aligned-donor/run.md)

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

[matched-random delta](matched-random-delta/run.md)

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
