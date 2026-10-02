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
elapsed_seconds: 6.51
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Asia to Africa. Positive answer_log_odds_shift favours first token 'Africa' over 'Asia'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Asia toward Africa with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Africa') |   p(first='Asia') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|------------------:|------------------------:|-----:|
| Base                          |             1.19209e-07 |          0.00343608 |          0.57786  |                0.581296 |    0 |
| raw J-coordinate exchange     |             6           |          0.422885   |          0.176285 |                0.59917  |    0 |
| raw plain-coordinate exchange |             0.375       |          0.00498596 |          0.576298 |                0.581284 |    0 |
| matched-random delta          |            -0.125       |          0.00239938 |          0.457241 |                0.45964  |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Shanghai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' continents', ' asia', '亚洲', 'China', '大陆', ' Africa', ' China', '-China', 'Africa', ' Europe', ' Oce', 'Europe', ' Antarctica', ' Americas', 'continental', '东亚', 'asia', ' continental', '；', ' Euras', ' Countries', ' continente', ' africa', 'Asian', ';;', ';', ' europe', '中国大陆', ' Азии', ';**']

Generation (5 tokens):
```text
Asia; CNY<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Asia    | -0.548424 | 0.57786     |             0 |
| <       | -0.923424 | 0.397157    |             0 |
| >       | -5.29842  | 0.00499947  |             0 |
| ;       | -5.42342  | 0.00441201  |             0 |
| Africa  | -5.67342  | 0.00343608  |             0 |
| AS      | -5.79842  | 0.00303233  |             0 |
| Asia    | -6.29842  | 0.0018392   |             0 |
| As      | -7.36092  | 0.000635611 |             0 |
| <br     | -7.61092  | 0.000495014 |             0 |
| Asian   | -7.61092  | 0.000495014 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '.', '<think>', '</tool_response>', '<|file_sep|>', '</', '.Category', ';', '\\', '\\n', '  \n', '**', '<', '<\\/', '/C', '\t  \n', '"<', '.<', '\\.', ',<', '@\\', '\\C', '/Y', '\\<', ' -->', '-Americ', '*', '<br', '<<<<']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'CNY']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Shanghai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' continents', ' Africa', 'Africa', '大陆', ' Europe', 'Europe', ' asia', 'continental', ' Americas', ' Antarctica', ' Oce', ' africa', ' continental', '亚洲', ' continente', ' europe', 'asia', ' Countries', ';**', ';', '；', ';;', '大陆的', ' Continental', '大陸', ' Euras', 'Argentina', ' Europa', 'China', ' Hemisphere']

Generation (5 tokens):
```text
Africa; ZAR<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Africa  | -0.860654 | 0.422885   |       4.81277 |
| <       | -1.11065  | 0.329344   |      -0.18723 |
| Asia    | -1.73565  | 0.176285   |      -1.18723 |
| Africa  | -3.73565  | 0.0238576  |       5.87527 |
| ;       | -4.86065  | 0.00774542 |       0.56277 |
| Af      | -5.11065  | 0.00603214 |       4.87527 |
| A       | -5.11065  | 0.00603214 |       2.62527 |
| Europe  | -5.36065  | 0.00469783 |       2.75027 |
| >       | -5.73565  | 0.00322877 |      -0.43723 |
| <A      | -5.98565  | 0.00251457 |       1.75027 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', ' Incorrect', ' incorrect', '</think>', 'incorrect', '错误', ' Wrong', ' incorrectly', 'Incorrect', '错误的', '**', '错', '</', '的错误', '是错误的', ' mistakenly', '错的', '  \n', ' WRONG', ' mistake', 'Wrong', ' wrong', '错了', '\n', '<think>', '.', ')', '<|im_start|>', ' False', ' ERROR', ' \n']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Africa', 'EGP']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Shanghai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' continents', ' asia', '亚洲', '大陆', ' Africa', 'China', 'Africa', ' Oce', ' Europe', ' China', 'Europe', ' Antarctica', ' Americas', '-China', 'continental', '东亚', 'asia', ' continental', '；', ' Euras', ' africa', ' Countries', ' continente', ';;', ';', ' europe', ';**', 'Asian', ' Азии', '大陸']

Generation (5 tokens):
```text
Asia; CNY<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| Asia    | -0.55113 | 0.576298    |   -0.00270635 |
| <       | -0.92613 | 0.396084    |   -0.00270635 |
| ;       | -5.30113 | 0.00498596  |    0.122294   |
| Africa  | -5.30113 | 0.00498596  |    0.372294   |
| >       | -5.42613 | 0.00440009  |   -0.127706   |
| AS      | -5.80113 | 0.00302414  |   -0.00270605 |
| Asia    | -6.05113 | 0.0023552   |    0.247294   |
| As      | -7.30113 | 0.000674776 |    0.0597939  |
| A       | -7.55113 | 0.000525516 |    0.184794   |
| <br     | -7.55113 | 0.000525516 |    0.0597939  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '.', '<think>', '</tool_response>', '<|file_sep|>', '</', '.Category', '\\', ';', '\\n', '  \n', '**', '<', '<\\/', '/C', '\t  \n', '"<', '.<', '\\.', '@\\', ',<', '\\C', '/Y', ' -->', '\\<', '-Americ', '*', '<br', '<<<<']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Africa', 'EGP']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Shanghai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Asia', 'Asia', ' asia', ' continents', 'China', '亚洲', '大陆', ' China', ' Africa', '-China', 'Africa', ' Europe', ' Americas', ' Oce', 'Europe', ' Antarctica', 'continental', '东亚', 'asia', '；', ' continental', ' Euras', ' Countries', ';;', 'Asian', ' africa', ' continente', ';', '中国大陆', ' Азии', 'Japan', ';**']

Generation (6 tokens):
```text
<Asia>; CNY<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| <       | -0.657546 | 0.518121    |     0.265878  |
| Asia    | -0.782546 | 0.457241    |    -0.234122  |
| ;       | -5.28255  | 0.00507948  |     0.140878  |
| >       | -5.40755  | 0.00448263  |    -0.109122  |
| AS      | -6.03255  | 0.00239938  |    -0.234122  |
| Asia    | -6.03255  | 0.00239938  |     0.265878  |
| Africa  | -6.03255  | 0.00239938  |    -0.359122  |
| <br     | -7.28255  | 0.000687433 |     0.328378  |
| As      | -7.40755  | 0.000606658 |    -0.0466218 |
| <A      | -7.47005  | 0.000569902 |     0.265878  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</', '<|im_start|>', '.', '<think>', '</tool_response>', '<|file_sep|>', '\\', '<', '.Category', '<\\/', '\\n', '  \n', '/C', '.<', '"<', '\t  \n', ',<', '<br', '\\C', '\\.', ')', '**', ' -->', '。', '\\<', ';', '\n   \n', '<<<<', '>']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'CNY']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.
