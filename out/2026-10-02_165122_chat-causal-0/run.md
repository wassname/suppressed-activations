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
elapsed_seconds: 8.69
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Beijing to Cairo. Positive answer_log_odds_shift favours first token 'C' over 'Be'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Beijing toward Cairo with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='C') |   p(first='Be') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|----------------:|------------------------:|-----:|
| Base                          |            -4.47035e-07 |    1.79983e-05 |       0.83926   |               0.839278  |    0 |
| raw J-coordinate exchange     |            11.125       |    0.0213475   |       0.0146719 |               0.0360194 |    0 |
| raw plain-coordinate exchange |             0.375       |    2.5918e-05  |       0.830629  |               0.830655  |    0 |
| matched-random delta          |             0.3125      |    2.28822e-05 |       0.780632  |               0.780655  |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Shanghai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Beijing', ' Jakarta', ' Taipei', ' Seoul', '北京', ' Tokyo', '杭州', '南京', 'London', ' Tehran', 'Jakarta', ' Moscow', ' Bangkok', 'city', ' London', 'China', ' Berlin', 'Paris', ' Islamabad', ' Shenzhen', ' Riyadh', ' Madrid', ' Pyongyang', ' Paris', '-China', ' Amsterdam', ' Delhi', ' Buenos', '台北', ' Bogotá', '东京', ' Kolkata']

Generation (6 tokens):
```text
Beijing; CNY<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Be      | -0.175234 | 0.83926    |             0 |
| <       | -2.55023  | 0.0780634  |             0 |
| Sh      | -3.92523  | 0.0197375  |             0 |
| P       | -3.92523  | 0.0197375  |             0 |
| China   | -4.42523  | 0.0119714  |             0 |
| <P      | -5.67523  | 0.00342987 |             0 |
| <p      | -5.92523  | 0.00267118 |             0 |
| PR      | -6.17523  | 0.00208032 |             0 |
| Pe      | -6.36273  | 0.00172464 |             0 |
| Tai     | -6.36273  | 0.00172464 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<think>', '<|im_start|>', '</', '</tool_response>', '<', '  \n', '\\', '\\n', '<|file_sep|>', ';', '.<', '<\\/', '**', ',<', '.Category', '"<', '<br', '/C', '\t  \n', '\\<', '@\\', '\\.', '.\\', '。', '/Y', '<<<<', ' -->', '/OR']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Beijing', 'CNY']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Shanghai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Paris', 'London', ' Berlin', ' Paris', ' London', ' Jakarta', ' Tehran', ' Cairo', ' Amsterdam', ' Madrid', ' Buenos', ' Riyadh', ' Moscow', ' Ankara', 'city', ' Jerusalem', 'Berlin', ' Bogotá', ' Oslo', '巴黎', ' Caracas', ' Nairobi', ' Islamabad', ' Tokyo', ' Johannesburg', ' Budapest', ' Beijing', ' Istanbul', ' Baghdad', 'Jakarta', ' Kolkata', ' Seoul']

Generation (5 tokens):
```text
Israel; ILS<|im_end|>
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| Israel  | -1.59682 | 0.202539  |     12.0784   |
| Ab      | -1.72182 | 0.17874   |     10.3909   |
| Jer     | -1.97182 | 0.139203  |     10.3909   |
| <       | -2.72182 | 0.0657549 |     -0.171587 |
| Tel     | -2.84682 | 0.0580285 |     10.5159   |
| R       | -3.34682 | 0.0351961 |      7.20341  |
| T       | -3.53432 | 0.0291786 |      6.51591  |
| C       | -3.84682 | 0.0213475 |      7.07841  |
| Sh      | -3.90932 | 0.0200541 |      0.015913 |
| Paris   | -4.03432 | 0.0176977 |      4.70341  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', ' Incorrect', '\\n', '  \n', '</think>', '**', ' incorrect', '.', ' Wrong', ' <--', '</', ' -->', '错误', 'incorrect', ';', 'Incorrect', '  \n\n', '错误的', ' mistakenly', ')', '\n   \n', '<br', '\n', ' ERROR', '的错误', '\\', '.\\', ' Sorry', '错', '\n\n', '.<']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Cairo', 'EGP']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Shanghai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Beijing', ' Jakarta', ' Taipei', ' Seoul', ' Tokyo', '北京', ' Tehran', '杭州', 'London', '南京', ' Moscow', ' London', 'Jakarta', ' Bangkok', 'city', ' Berlin', 'Paris', ' Islamabad', ' Riyadh', ' Madrid', ' Amsterdam', ' Paris', ' Buenos', ' Bogotá', ' Pyongyang', ' Kolkata', ' Delhi', ' Ankara', '东京', ' Jerusalem', ' Москва', ' Mumbai']

Generation (6 tokens):
```text
Beijing; CNY<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Be      | -0.185572 | 0.830629   |    -0.0103379 |
| <       | -2.56057  | 0.0772605  |    -0.0103378 |
| P       | -3.68557  | 0.0250828  |     0.239662  |
| Sh      | -3.81057  | 0.0221355  |     0.114662  |
| China   | -4.56057  | 0.0104561  |    -0.135338  |
| <P      | -5.62307  | 0.00361352 |     0.0521622 |
| <p      | -5.81057  | 0.00299572 |     0.114662  |
| Tai     | -5.93557  | 0.00264371 |     0.427162  |
| Ch      | -6.31057  | 0.00181699 |     0.177162  |
| PR      | -6.31057  | 0.00181699 |    -0.135338  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<think>', '<|im_start|>', '</', '</tool_response>', '  \n', '<', '<|file_sep|>', '\\n', '\\', ';', '.<', '<\\/', '**', ',<', '.Category', '"<', '<br', '/C', '\t  \n', '\\<', '@\\', '\\.', '.\\', '<<<<', '/Y', '。', ' -->', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Cairo', 'EGP']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Shanghai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Beijing', ' Jakarta', ' Taipei', ' Seoul', ' Tokyo', '北京', '杭州', 'city', '南京', ' Tehran', 'China', 'London', 'Jakarta', ' Moscow', ' London', ' Bangkok', 'Paris', ' Berlin', ' Shenzhen', '-China', ' China', ' Islamabad', ' Pyongyang', ' Riyadh', ' Paris', ' Madrid', ' Delhi', ' Amsterdam', ' Buenos', ' Kolkata', ' Bogotá', '东京']

Generation (6 tokens):
```text
Beijing; CNY<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Be      | -0.247651 | 0.780632   |    -0.0724168 |
| <       | -2.24765  | 0.105647   |     0.302583  |
| Sh      | -3.49765  | 0.0302684  |     0.427583  |
| P       | -3.74765  | 0.0235731  |     0.177583  |
| China   | -3.99765  | 0.0183587  |     0.427583  |
| <P      | -5.24765  | 0.00525986 |     0.427583  |
| <p      | -5.49765  | 0.00409638 |     0.427583  |
| PR      | -5.81015  | 0.00299698 |     0.365083  |
| Ch      | -5.93515  | 0.00264482 |     0.552583  |
| People  | -5.93515  | 0.00264482 |     0.552583  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<think>', '<|im_start|>', '</', '</tool_response>', '  \n', '<', ';', '<|file_sep|>', '\\', '\\n', '.<', '**', '<\\/', ',<', '"<', '.Category', '<br', '/C', '\t  \n', '\\<', '。', '@\\', '.\\', '\\.', '/Y', ' -->', '<<<<', './.']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Beijing', 'CNY']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.
