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
reverse: false
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
elapsed_seconds: 10.23
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Stockholm to Tokyo. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Sweden', ' Japan') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v2_allpos.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Stockholm toward Tokyo with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |            -1.93715e-07 |      2.81536e-06 |        0.804189    |                0.804191 |    0 |
| raw J-coordinate exchange     |            27.25        |      0.991324    |        4.14491e-07 |                0.991324 |    0 |
| raw plain-coordinate exchange |             0.0624998   |      2.99459e-06 |        0.80356     |                0.803563 |    0 |
| matched-random delta          |             0.25        |      3.67193e-06 |        0.816855    |                0.816858 |    0 |

[Base](base/run.md)

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

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Tokyo', ' Jakarta', ' Bangkok', '东京', ' Taipei', 'Jakarta', ' Seoul', ' Osaka', ' Honolulu', ' Tokio', ' Riyadh', 'London', 'Tok', ' Nairobi', ' Madrid', '東京', 'Paris', ' Kyoto', '大阪', ' Beijing', ' Tehran', ' Oslo', ' Ankara', 'city', ' Caracas', ' Surabaya', ' Kuala', ' Helsinki', ' London', ' Mumbai', ' Amsterdam', '首尔']

Generation (6 tokens):
```text
Tokyo; JPY<|im_end|>
```

| token   |       log p |           p |   delta log p |
|:--------|------------:|------------:|--------------:|
| Tok     | -0.00871415 | 0.991324    |     12.7717   |
| <       | -5.38371    | 0.00459074  |     -3.66579  |
| Os      | -6.63371    | 0.00131527  |     -0.415793 |
| T       | -7.38371    | 0.000621289 |      3.45921  |
| Ky      | -7.75871    | 0.000427005 |      6.27171  |
| <T      | -7.88371    | 0.000376831 |      2.58421  |
| Japan   | -8.75871    | 0.000157087 |     10.178    |
| Tokyo   | -9.00871    | 0.000122339 |     12.2092   |
| O       | -9.50871    | 7.42024e-05 |     -2.29079  |
| Tai     | -9.57121    | 6.97067e-05 |      5.64671  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\\n', '  \n', ' Incorrect', '错误', '</tool_response>', '  \n\n', '错', ' incorrect', ' Note', '.\\', '<think>', '错误的', 'incorrect', '.', '**', ' Sorry', ' ERROR', '\\', '</', ' \n\n', ' Wrong', '的错误', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <--', ' -->', ' Disclaimer', ' <<<', 'Incorrect', 'Note']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', 'Paris', 'Berlin', ' Prague', ' Budapest', ' Madrid', ' Munich', 'Sweden', ' Zurich', ' Jakarta', ' Rotterdam', ' London', ' Lisbon', 'Madrid', ' Minneapolis', ' Bratis', 'Barcelona', ' Vienna', ' Barcelona', 'openhagen', ' Paris', ' Edinburgh', ' Frankfurt', ' Bangkok', '瑞典', ' Sweden']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Stock   | -0.218703 | 0.80356     |  -0.000781864 |
| <       | -1.7187   | 0.179298    |  -0.000781775 |
| Go      | -5.7187   | 0.00328397  |  -0.000782013 |
| ;       | -5.8437   | 0.00289809  |  -0.000782013 |
| Os      | -5.9687   | 0.00255756  |   0.249218    |
| St      | -6.4062   | 0.00165128  |  -0.000782013 |
| O       | -7.0937   | 0.000830317 |   0.124218    |
| Sweden  | -7.2812   | 0.000688357 |   0.124218    |
| <p      | -7.9687   | 0.000346128 |  -0.063282    |
| <span   | -8.0937   | 0.000305456 |  -0.000782013 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '<|file_sep|>', '\t  \n', '.Category', ';**', '</tool_response>', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', ' **.**', '.', ';', '</', ';<', '.<', '<\\/', ',<', '**', ';</', ' <<<', '@\\', '="<', '<<<<', './.', '<<<', '\t\n', ' **■', '#/', ' <$']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', 'Sweden', 'Paris', ' Prague', ' Budapest', 'Berlin', ' Munich', ' Zurich', ' Sweden', ' Madrid', ' Rotterdam', '瑞典', ' Minneapolis', ' Jakarta', ' London', ' Bratis', ' Lisbon', 'openhagen', ' Edinburgh', ' Vienna', 'Barcelona', ' Barcelona', ' Paris', ' Bangkok', 'Madrid', 'city']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Stock   | -0.202294 | 0.816855    |     0.0156273 |
| <       | -1.82729  | 0.160848    |    -0.109373  |
| ;       | -5.32729  | 0.00485719  |     0.515627  |
| Go      | -5.45229  | 0.00428646  |     0.265627  |
| Os      | -5.70229  | 0.0033383   |     0.515627  |
| St      | -6.26479  | 0.0019021   |     0.140627  |
| O       | -6.82729  | 0.00108379  |     0.390627  |
| Sweden  | -7.20229  | 0.000744875 |     0.203127  |
| <span   | -7.88979  | 0.000374547 |     0.203127  |
| <p      | -7.95229  | 0.000351854 |    -0.0468731 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '<|file_sep|>', '\t  \n', '.Category', '</tool_response>', '  \n', ';**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' **.**', '.', ';', '</', '.<', ';<', ',<', '<\\/', '**', ';</', ' <<<', '@\\', '="<', '<<<<', './.', '<<<', '\t\n', ' **■', ' <$', '  \n\n']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.
