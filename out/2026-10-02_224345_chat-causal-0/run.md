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
elapsed_seconds: 6.54
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Europe to North America. Positive answer_log_odds_shift favours first token 'North' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Europe toward North America with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='North') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |             1.30385e-07 |        4.06681e-05 |         0.953547    |                0.953588 |    0 |
| raw J-coordinate exchange     |            18.625       |        0.835057    |         0.000159613 |                0.835216 |    0 |
| raw plain-coordinate exchange |             0.1875      |        4.85252e-05 |         0.943248    |                0.943296 |    0 |
| matched-random delta          |            -0.1875      |        3.28939e-05 |         0.930323    |                0.930356 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Barcelona on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', 'Asia', ' europe', ' continents', ' Asia', ' Europa', '大陆', 'Europa', ' Oce', '欧洲', 'Africa', ' Africa', ' Americas', ' EURO', 'continental', ' continental', '西欧', ' asia', '欧洲的', ';', '在欧洲', 'Spain', ';**', ' Spain', ' Европа', 'urope', ' continente', ';;', ' Antarctica', ' Scandin', ' Europ']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0475663 | 0.953547    |             0 |
| <        | -3.54757   | 0.0287946   |             0 |
| Europe   | -4.67257   | 0.00934825  |             0 |
| ;        | -6.29757   | 0.00184078  |             0 |
| E        | -6.29757   | 0.00184078  |             0 |
| Europa   | -7.42257   | 0.000597613 |             0 |
| EU       | -7.42257   | 0.000597613 |             0 |
| European | -7.67257   | 0.000465422 |             0 |
| <E       | -7.92257   | 0.000362471 |             0 |
| Eu       | -7.92257   | 0.000362471 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '.', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '<\\/', '</', '｡', ' **.**', '\n   \n', '\\n', '.<', ';</', '\\.', '<<<<', '-US', './.', '\t\n', ' **€', ';charset', '  \n\n', ' EUR']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Barcelona on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Americas', ' Asia', ' continents', ' Europe', ' Oce', 'Europe', '大陆', ' América', '北美', ' asia', 'continental', ' Antarctica', ' Africa', 'Argentina', ';', 'Canada', ' continental', 'Africa', ' Argentina', ';**', '美洲', ';;', ' Canada', ' Mexico', ' Countries', ' europe', ' continente', ' Europa', ' USA', 'USA', '__;']

Generation (6 tokens):
```text
North America; MXN<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.180256 | 0.835057    |      9.92981  |
| NA      | -2.68026  | 0.0685456   |     10.6173   |
| <       | -2.93026  | 0.0533834   |      0.617311 |
| N       | -4.05526  | 0.0173311   |     10.0548   |
| South   | -4.55526  | 0.0105118   |      6.61731  |
| ;       | -5.80526  | 0.00301169  |      0.492311 |
| <N      | -6.30526  | 0.00182668  |      6.36731  |
| North   | -6.43026  | 0.00161204  |      8.80481  |
| Na      | -6.43026  | 0.00161204  |      9.36731  |
| Americ  | -7.49276  | 0.000557106 |      6.67981  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', ' Incorrect', ' incorrect', '</think>', '**', '.', '错误', '错误的', 'incorrect', '\\n', '</', '?', ' Wait', '错', 'Incorrect', ' incorrectly', '的错误', ' Wrong', '错的', '是错误的', ';', 'Wait', 'wait', ' wait', ')', ' mistakenly', '错了', '不正确', '\\', ' WRONG', ' isn']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'MXN']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Barcelona on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', 'Asia', ' europe', ' Asia', ' continents', ' Europa', '大陆', ' Oce', 'Europa', '欧洲', ' Americas', 'Africa', ' Africa', 'continental', ' EURO', ' continental', ' asia', '西欧', ';', '欧洲的', '在欧洲', 'Spain', ';**', ' Европа', 'urope', ' continente', ' Antarctica', ' Spain', ';;', ' Scandin', ' Countries']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0584264 | 0.943248    |    -0.0108601 |
| <        | -3.55843   | 0.0284836   |    -0.0108602 |
| Europe   | -3.93343   | 0.0195765   |     0.73914   |
| ;        | -6.18343   | 0.00206335  |     0.11414   |
| E        | -6.30843   | 0.0018209   |    -0.01086   |
| Europa   | -7.43343   | 0.000591158 |    -0.01086   |
| EU       | -7.43343   | 0.000591158 |    -0.01086   |
| European | -7.80843   | 0.000406297 |    -0.13586   |
| <E       | -7.93343   | 0.000358556 |    -0.01086   |
| Eu       | -7.99593   | 0.000336832 |    -0.07336   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '.', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '｡', '</', ' **.**', '<\\/', '\n   \n', '\\n', '.<', ';</', '\\.', '<<<<', './.', '\t\n', '-US', ' **€', ' <--', '  \n\n', ' */']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'MXN']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Barcelona on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', 'Asia', ' Asia', ' Europa', ' continents', '大陆', '欧洲', ' Oce', 'Europa', ' Americas', ' Africa', 'Africa', ' EURO', '西欧', ' continental', 'continental', ' asia', '欧洲的', ';', '在欧洲', 'Spain', 'urope', ';**', ' Spain', ' Европа', ';;', ' continente', ' Scandin', ' Europ', ' Antarctica']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0722238 | 0.930323    |    -0.0246575 |
| <        | -3.32222   | 0.0360725   |     0.225343  |
| Europe   | -3.69722   | 0.0247923   |     0.975343  |
| ;        | -5.94722   | 0.00261309  |     0.350343  |
| E        | -6.44722   | 0.00158492  |    -0.149657  |
| Europa   | -7.57222   | 0.000514547 |    -0.149657  |
| European | -7.75972   | 0.000426574 |    -0.0871572 |
| <span    | -7.82222   | 0.00040073  |     0.225343  |
| EU       | -7.82222   | 0.00040073  |    -0.399657  |
| <E       | -7.88472   | 0.000376451 |     0.0378428 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '.', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', ' **.**', '</', '｡', '<\\/', '\n   \n', '.<', '\\n', ';</', '\\.', './.', '<<<<', '-US', '\t\n', '  \n\n', ' <--', ' **€', '\n  \n']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.
