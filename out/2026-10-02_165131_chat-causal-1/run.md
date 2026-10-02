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
elapsed_seconds: 5.47
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Cairo to Beijing. Positive answer_log_odds_shift favours first token 'C' over 'Be'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Cairo toward Beijing with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='C') |   p(first='Be') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|----------------:|------------------------:|-----:|
| Base                          |                  0      |    0.52833     |     0.000399405 |                0.52873  |    0 |
| raw J-coordinate exchange     |                -15      |    0.000283499 |     0.700612    |                0.700896 |    0 |
| raw plain-coordinate exchange |                 -0.1875 |    0.555781    |     0.000506806 |                0.556287 |    0 |
| matched-random delta          |                 -0.125  |    0.398012    |     0.000340951 |                0.398353 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Alexandria, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Cairo', 'Paris', 'London', ' Riyadh', ' Nairobi', ' Beirut', ' Egypt', ' Paris', 'Egypt', ' Madrid', ' London', ' Ankara', ' Islamabad', ' Istanbul', ' Baghdad', 'Madrid', ' Oslo', ' Tehran', ' Caracas', ' Jerusalem', ' Budapest', '埃及', ' Berlin', ' PARIS', '巴黎', ' Vienna', ' Dubai', ' Prague', ' Athens', ' Moscow', ' Jakarta', 'city']

Generation (6 tokens):
```text
Cairo; EGP<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| C       | -0.638034 | 0.52833    |             0 |
| Egypt   | -1.26303  | 0.282795   |             0 |
| Alex    | -2.26303  | 0.104034   |             0 |
| <       | -3.63803  | 0.026304   |             0 |
| The     | -5.13803  | 0.00586922 |             0 |
| Ab      | -5.57553  | 0.00378945 |             0 |
| <C      | -5.82553  | 0.00295123 |             0 |
| ;       | -5.88803  | 0.00277242 |             0 |
| <p      | -6.01303  | 0.00244666 |             0 |
| Dub     | -6.07553  | 0.00229842 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '  \n', '.', '<think>', '</tool_response>', '<|im_start|>', '<|file_sep|>', '\\', ';', '.Category', '\t  \n', '\t\n', '。', '<', '.<', ' -->', '\\n', '</', '**', ' **.**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' \n', ',<', '\n  \n', '\n', '.\\', '  \n\n', '/AFP', '\n   \n', '.ht']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Cairo', 'EGP']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Alexandria, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Beijing', ' Jakarta', ' Bangkok', ' Tokyo', ' Seoul', ' Taipei', ' Tehran', ' Riyadh', 'London', ' Moscow', ' Madrid', ' Islamabad', ' Shanghai', '杭州', ' London', 'Jakarta', ' Nairobi', '北京', 'China', 'Paris', ' Cairo', 'city', ' Prague', ' Shenzhen', ' Pyongyang', ' Caracas', 'Madrid', ' Ankara', ' Berlin', ' Lisbon', ' Paris', ' Oslo']

Generation (6 tokens):
```text
Beijing; CNY<|im_end|>
```

| token   |   log p |          p |   delta log p |
|:--------|--------:|-----------:|--------------:|
| Be      | -0.3558 | 0.700612   |      7.46973  |
| China   | -1.8558 | 0.156328   |     11.8135   |
| P       | -3.2308 | 0.0395259  |      7.71973  |
| <       | -3.8558 | 0.0211567  |     -0.217767 |
| Sh      | -3.9808 | 0.0186707  |      6.65723  |
| <p      | -5.2308 | 0.00534924 |      0.782233 |
| Ch      | -5.4808 | 0.00416599 |      6.21973  |
| Tai     | -5.5433 | 0.00391359 |      5.59473  |
| Gu      | -5.7308 | 0.00324448 |      5.34473  |
| S       | -6.0433 | 0.00237371 |      0.907233 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '  \n', '**', '</', '<think>', '</tool_response>', '<|im_start|>', '\\n', ' Incorrect', ';', '\\', '错误', ',<', '<', 'incorrect', ' -->', '\t  \n', '.<', ' incorrect', '错误的', '.Category', '错', '<br', '<|file_sep|>', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' Disclaimer', '<\\/', 'Incorrect', ')']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Beijing', 'CNY']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Alexandria, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Cairo', 'Paris', 'London', ' Riyadh', ' Nairobi', ' Beirut', ' Paris', ' Madrid', ' Egypt', ' London', ' Ankara', 'Egypt', ' Tehran', ' Istanbul', ' Islamabad', 'Madrid', ' Baghdad', ' Caracas', ' Oslo', ' Budapest', ' Jerusalem', ' Berlin', ' PARIS', '巴黎', ' Prague', ' Vienna', ' Moscow', ' Dubai', ' Athens', ' Jakarta', '埃及', 'city']

Generation (6 tokens):
```text
Cairo; EGP<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| C       | -0.587382 | 0.555781   |     0.0506519 |
| Egypt   | -1.33738  | 0.262532   |    -0.074348  |
| Alex    | -2.33738  | 0.0965802  |    -0.074348  |
| <       | -3.71238  | 0.0244193  |    -0.074348  |
| The     | -4.89988  | 0.00744746 |     0.238152  |
| Ab      | -5.52488  | 0.00398634 |     0.0506516 |
| Dub     | -5.89988  | 0.00273977 |     0.175652  |
| ;       | -5.96238  | 0.00257377 |    -0.0743484 |
| <C      | -6.02488  | 0.00241784 |    -0.199348  |
| <p      | -6.14988  | 0.00213373 |    -0.136848  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '  \n', '.', '</tool_response>', '<think>', '<|im_start|>', '<|file_sep|>', '\\', '.Category', ';', '\t  \n', '\t\n', '。', '.<', ' -->', '<', '\\n', ' **.**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '</', '**', ' \n', '\n', '\n  \n', '.\\', ',<', '/AFP', '\n   \n', '  \n\n', '.ht']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Beijing', 'CNY']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Alexandria, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Cairo', 'Paris', ' Egypt', ' Riyadh', ' Nairobi', 'London', 'Egypt', ' Beirut', ' Paris', ' Ankara', ' Madrid', ' London', ' Baghdad', ' Tehran', '埃及', ' Caracas', ' Istanbul', ' Islamabad', ' Oslo', ' PARIS', ' Jerusalem', ' Budapest', ' Athens', ' Berlin', ' Dubai', 'Madrid', 'city', ' Moscow', ' Vienna', '巴黎', ' Tunis', ' Jakarta']

Generation (6 tokens):
```text
Cairo; EGP<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| C       | -0.921273 | 0.398012   |      -0.28324 |
| Egypt   | -0.921273 | 0.398012   |       0.34176 |
| Alex    | -2.42127  | 0.0888085  |      -0.15824 |
| <       | -3.17127  | 0.0419502  |       0.46676 |
| The     | -5.42127  | 0.00442151 |      -0.28324 |
| <C      | -5.54627  | 0.00390197 |       0.27926 |
| <p      | -5.67127  | 0.00344348 |       0.34176 |
| ;       | -5.67127  | 0.00344348 |       0.21676 |
| Ab      | -5.73377  | 0.00323485 |      -0.15824 |
| S       | -5.79627  | 0.00303886 |       1.15426 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '  \n', '</tool_response>', '<think>', '<|im_start|>', ';', '<|file_sep|>', '\\', '.Category', '\t  \n', '\t\n', '。', '.<', '<', ' -->', '</', ' **.**', '\\n', '**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', ' \n', '\n  \n', '\n', '.\\', '/AFP', '  \n\n', '\n   \n', '.ht']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Cairo', 'EGP']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.
