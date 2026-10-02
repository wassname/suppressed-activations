---
raw_coordinate_exchange: true
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
prompt_slice: '0:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: None
donor_reflection: false
equal_donor_norm: false
relation: country_properties
elapsed_seconds: 9.20
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Tokyo to Stockholm. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Sweden', ' Japan') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v2_allpos.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Tokyo toward Stockholm with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |                   0     |         0.987861 |        4.39682e-07 |                0.987861 |    0 |
| raw J-coordinate exchange     |                  -3     |         0.952846 |        8.51822e-06 |                0.952854 |    0 |
| raw plain-coordinate exchange |                   0     |         0.987804 |        4.39657e-07 |                0.987805 |    0 |
| matched-random delta          |                  -0.125 |         0.987013 |        4.97798e-07 |                0.987014 |    0 |

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

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', 'London', ' Stockholm', 'Paris', ' Riyadh', ' Madrid', ' Oslo', 'Jakarta', '东京', ' Seoul', ' Berlin', ' London', ' Prague', ' Nairobi', ' Paris', 'Madrid', 'city', ' Amsterdam', ' Taipei', ' Helsinki', ' Vienna', ' Brasília', '大阪', 'Berlin', ' Budapest', ' Ankara', '成都', ' Kyoto', ' Bogotá', ' Caracas']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0483023 | 0.952846    |    -0.0360887 |
| Os      | -3.4233    | 0.0326046   |     2.46391   |
| <       | -5.2983    | 0.00500008  |     0.338912  |
| T       | -5.5483    | 0.00389406  |     1.33891   |
| Ky      | -6.4233    | 0.00162329  |    -0.411088  |
| O       | -7.2983    | 0.000676687 |     2.15141   |
| <T      | -7.5483    | 0.000527004 |     0.0889115 |
| Tokyo   | -8.1733    | 0.000282085 |     0.588911  |
| Se      | -8.3608    | 0.000233857 |     0.401411  |
| Japan   | -8.3608    | 0.000233857 |     0.713911  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '</tool_response>', '.', '  \n', '<|im_start|>', ';', '<|file_sep|>', '.Category', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\t  \n', '\\n', '\\.', '<\\/', '\x00', '</', '\r\r\n', '\\', '\\<', '@\\', '｡', '  \n\n', '.<', ' -->', '<', '\t\n', '\n  \n', ' <<<', ' \n', '。']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Seoul', 'Jakarta', ' Taipei', ' Riyadh', 'London', 'Paris', ' Kyoto', ' Tokio', 'Tok', ' Madrid', ' Nairobi', ' Honolulu', ' Beijing', '東京', '大阪', 'city', ' London', ' Tehran', ' Ankara', ' Brasília', '首尔', ' Paris', ' Islamabad', ' Caracas', 'Madrid', ' Stockholm', ' Bogotá', '杭州']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0122708 | 0.987804    |  -5.72307e-05 |
| <       | -5.63727   | 0.00356258  |  -5.72205e-05 |
| Os      | -5.76227   | 0.00314396  |   0.124943    |
| Ky      | -6.13727   | 0.00216081  |  -0.125057    |
| T       | -6.88727   | 0.0010207   |  -5.72205e-05 |
| <T      | -7.63727   | 0.000482142 |  -5.72205e-05 |
| Tokyo   | -8.69977   | 0.000166624 |   0.0624428   |
| Se      | -8.88727   | 0.000138136 |  -0.125057    |
| K       | -9.07477   | 0.000114519 |  -0.0625572   |
| Japan   | -9.07477   | 0.000114519 |  -5.72205e-05 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '</tool_response>', '.', ';', '<|im_start|>', '  \n', '<|file_sep|>', '.Category', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\t  \n', '\\n', '\\.', '<\\/', '</', '\x00', '\\', '\r\r\n', '@\\', '｡', '\\<', '.<', '  \n\n', ' -->', '<', '\t\n', '。', '.ht', '.\\', '\n  \n']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Osaka, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Seoul', 'Jakarta', ' Taipei', ' Riyadh', 'London', ' Kyoto', 'Paris', ' Tokio', 'Tok', ' Nairobi', ' Madrid', ' Honolulu', '東京', 'city', ' Beijing', '大阪', ' London', ' Tehran', ' Ankara', ' Brasília', '首尔', ' Paris', ' Islamabad', ' Bogotá', ' Caracas', ' Stockholm', '京都', ' Berlin']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Tok     | -0.0130718 | 0.987013    |  -0.000858236 |
| <       | -5.63807   | 0.00355973  |  -0.000858307 |
| Os      | -5.76307   | 0.00314145  |   0.124142    |
| Ky      | -5.88807   | 0.00277232  |   0.124142    |
| T       | -6.88807   | 0.00101988  |  -0.000858307 |
| <T      | -7.76307   | 0.000425149 |  -0.125858    |
| Tokyo   | -8.63807   | 0.000177228 |   0.124142    |
| Se      | -8.70057   | 0.000166491 |   0.0616417   |
| ;       | -8.70057   | 0.000166491 |   0.374142    |
| K       | -8.88807   | 0.000138026 |   0.124142    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<think>', '.', ';', '  \n', '<|im_start|>', '<|file_sep|>', '.Category', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\t  \n', '\\n', '\\.', '<\\/', '</', '\x00', '\r\r\n', '\\', '@\\', '｡', '\\<', '  \n\n', '.<', ' -->', '。', '\t\n', '<', '\n  \n', '.\\', ' \n']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.
