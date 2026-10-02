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
elapsed_seconds: 27.48
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is North America to Oceania. Positive answer_log_odds_shift favours first token 'O' over 'North'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes North America toward Oceania with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='O') |   p(first='North') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|-------------------:|------------------------:|-----:|
| Base                          |            -1.78814e-07 |    3.80324e-06 |           0.900634 |                0.900638 |    0 |
| raw J-coordinate exchange     |            10.5         |    0.0307183   |           0.200309 |                0.231027 |    0 |
| raw plain-coordinate exchange |             0.125       |    4.32718e-06 |           0.9043   |                0.904305 |    0 |
| matched-random delta          |            -0.0625002   |    3.56289e-06 |           0.898131 |                0.898135 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Toronto on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Canada', ' Canada', '北美', 'Asia', ' Americas', ' continents', '大陆', ' Asia', ' Europe', ' canada', 'Europe', 'continental', ' Oce', ' Canadá', ' Kanada', ' Antarctica', ' continental', ';;', ';', 'Africa', ' Africa', ';**', 'USA', 'North', ' continente', ' América', ' USA', ' asia', ' Australia', ' Countries', ' europe', 'Australia']

Generation (5 tokens):
```text
North America; CAD<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.104656 | 0.900634    |             0 |
| NA      | -3.10466  | 0.0448399   |             0 |
| <       | -3.22966  | 0.0395711   |             0 |
| N       | -5.22966  | 0.00535537  |             0 |
| ;       | -6.35466  | 0.00173863  |             0 |
| <N      | -6.35466  | 0.00173863  |             0 |
| North   | -6.97966  | 0.000930623 |             0 |
| >       | -7.10466  | 0.000821272 |             0 |
| <br     | -7.66716  | 0.000467947 |             0 |
| <span   | -7.97966  | 0.000342357 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '<think>', '</tool_response>', '.Category', '.<', '<\\/', '.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', ';', ',<', '\t  \n', '\\<', '"<', ' -->', '<', '\\.', '\\n', '</', '.\\', ';<', '\\C', '/C', '<<<<', '｡', ' <--', '\x00', '="<']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'CAD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Toronto on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' continents', ' Europe', ' Oce', 'Europe', '大陆', ' Australia', ' Americas', 'Australia', ' Antarctica', ' Africa', 'Africa', '北美', 'continental', ' asia', 'Canada', ';', ';**', ' europe', ';;', ' continental', ' continente', '亚洲', ' australia', ' Canada', ' Europa', '__;', '；', ' Countries', 'asia', ' africa']

Generation (6 tokens):
```text
<North America>; AUD<|im_end|>
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| <         | -0.732896 | 0.480515   |       2.49676 |
| North     | -1.6079   | 0.200309   |      -1.50324 |
| Australia | -2.7329   | 0.0650307  |       9.49676 |
| Europe    | -2.7329   | 0.0650307  |       5.93426 |
| ;         | -3.2329   | 0.0394431  |       3.12176 |
| O         | -3.4829   | 0.0307183  |       8.99676 |
| Africa    | -3.6079   | 0.0271088  |       5.55926 |
| Asia      | -4.2329   | 0.0145103  |       6.37176 |
| Oce       | -4.4204   | 0.0120295  |      11.1843  |
| >         | -4.6704   | 0.00936856 |       2.43426 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ' incorrect', ' Incorrect', '错误', '错', 'incorrect', ' incorrectly', '错误的', ' -->', 'Incorrect', '</tool_response>', ' mistakenly', '错的', '<|im_start|>', ' Wrong', '的错误', ' \n\n', '<|file_sep|>', '.', ' WRONG', ' <--', ' FALSE', '</', '是错误的', '不正确', ' �', 'Wrong', ';', ' ERROR', '=false']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Oceania', 'AUD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Toronto on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Canada', ' Canada', '北美', 'Asia', ' Americas', ' continents', ' Asia', '大陆', ' Europe', 'Europe', ' canada', ' Oce', 'continental', ' Canadá', ' Antarctica', ' Kanada', ';;', ';', ' continental', ' Africa', 'Africa', ';**', 'USA', ' Australia', ' continente', ' América', 'Australia', ' USA', ' europe', 'North', ' asia', ' Countries']

Generation (5 tokens):
```text
North America; CAD<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.100594 | 0.9043      |    0.00406273 |
| NA      | -3.22559  | 0.0397322   |   -0.120937   |
| <       | -3.22559  | 0.0397322   |    0.00406289 |
| N       | -5.22559  | 0.00537717  |    0.00406265 |
| ;       | -6.10059  | 0.00224154  |    0.254063   |
| <N      | -6.35059  | 0.00174571  |    0.00406265 |
| North   | -6.47559  | 0.00154058  |    0.504063   |
| >       | -7.10059  | 0.000824615 |    0.00406265 |
| <br     | -7.78809  | 0.000414643 |   -0.120937   |
| <span   | -8.03809  | 0.000322924 |   -0.0584373  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '<think>', '</tool_response>', '.Category', '.<', '<\\/', '.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';', '<br', '\t  \n', ',<', '\\<', '\\.', ' -->', '\\n', '"<', '<', '.\\', '\\C', '｡', ';<', '</', '/C', '<<<<', '\x00', '="<', '\\']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Oceania', 'AUD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Toronto on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Canada', ' Canada', '北美', 'Asia', ' Americas', ' continents', ' Asia', '大陆', ' canada', ' Europe', 'Europe', 'continental', ' Oce', ' Canadá', ' Kanada', ';;', ';', ' Antarctica', ' continental', ';**', ' Africa', ' USA', ' Australia', 'USA', 'Africa', ' Countries', 'North', ' América', 'Australia', ' europe', ' continente', ' Кана']

Generation (5 tokens):
```text
North America; CAD<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.107439 | 0.898131    |   -0.00278264 |
| <       | -3.10744  | 0.0447153   |    0.122217   |
| NA      | -3.35744  | 0.0348243   |   -0.252783   |
| North   | -4.98244  | 0.00685732  |    1.99722    |
| N       | -5.35744  | 0.00471296  |   -0.127783   |
| ;       | -5.73244  | 0.00323917  |    0.622217   |
| <N      | -6.35744  | 0.0017338   |   -0.00278282 |
| >       | -6.98244  | 0.000928037 |    0.122217   |
| <br     | -7.54494  | 0.00052878  |    0.122217   |
| <span   | -7.85744  | 0.000386863 |    0.122217   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '<think>', '</tool_response>', '.<', '.Category', '<\\/', '.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';', '\t  \n', '<br', ',<', '"<', '\\.', ' -->', '\\<', '.\\', '<', '\\n', '</', '｡', ';<', '/C', '\\C', '<<<<', '\x00', '="<', '\\']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'CAD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.
