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
elapsed_seconds: 5.14
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is North America to Europe. Positive answer_log_odds_shift favours first token 'North' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes North America toward Europe with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='North') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |                  0      |           0.790508 |         0.000151098 |                0.790659 |    0 |
| raw J-coordinate exchange     |                 -4.3125 |           0.726803 |         0.0103673   |                0.737171 |    0 |
| raw plain-coordinate exchange |                  0.3125 |           0.794182 |         0.00011106  |                0.794293 |    0 |
| matched-random delta          |                  0.0625 |           0.824421 |         0.000148033 |                0.824569 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Guadalajara on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Americas', ' continents', ' Europe', 'Europe', ' Africa', '大陆', 'Africa', ' asia', 'continental', ' Oce', ' América', ' Mexico', ' continental', '北美', 'Argentina', '美洲', 'Mexico', ' Argentina', ' Europa', ' mexico', ' continente', ';**', 'Canada', 'Spain', ';', ' Countries', ' Antarctica', ' Spain', ' europe', ' Continental']

Generation (6 tokens):
```text
North America; MXN<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| North   | -0.23508 | 0.790508    |             0 |
| NA      | -1.98508 | 0.13737     |             0 |
| N       | -3.48508 | 0.0306513   |             0 |
| <       | -3.61008 | 0.0270497   |             0 |
| Na      | -5.73508 | 0.00323062  |             0 |
| ;       | -5.86008 | 0.00285102  |             0 |
| <N      | -6.48508 | 0.00152604  |             0 |
| North   | -7.36008 | 0.000636148 |             0 |
| <span   | -7.61008 | 0.000495432 |             0 |
| <br     | -7.79758 | 0.000410728 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<|im_start|>', '</tool_response>', '<think>', '</', ';', '\\n', '**', '<|file_sep|>', '.Category', '\\', '<\\/', ' Incorrect', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\.', '<', '错误的', '?', '  \n', 'incorrect', ')', '<<<<', ' <<<', '\t  \n', '-Americ', '错', ' Disclaimer', '.\\', '@\\']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'MXN']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Guadalajara on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Europe', 'Europe', ' continents', ' Africa', ' Americas', 'Africa', '大陆', ' asia', ' Oce', ' Europa', 'continental', ' América', 'Spain', ' continental', ' Spain', ' europe', 'Argentina', ' Mexico', 'Europa', ' Argentina', '北美', ' continente', ';**', ';', ' africa', ' Countries', 'Mexico', ' Antarctica', '美洲', ' mexico']

Generation (6 tokens):
```text
North America; MXN<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| North   | -0.319099 | 0.726803   |    -0.0840199 |
| NA      | -1.8191   | 0.162172   |     0.16598   |
| <       | -3.0691   | 0.046463   |     0.54098   |
| N       | -3.8191   | 0.0219476  |    -0.33402   |
| Europe  | -4.5691   | 0.0103673  |     4.22848   |
| South   | -4.8191   | 0.00807405 |     2.97848   |
| ;       | -5.0691   | 0.00628808 |     0.79098   |
| Na      | -5.5691   | 0.00381391 |     0.16598   |
| <N      | -6.1941   | 0.00204144 |     0.29098   |
| <span   | -6.5066   | 0.00149355 |     1.10348   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '.', '<think>', '</', ';', '\\n', '**', '<|file_sep|>', '.Category', '\\', '<\\/', ' Incorrect', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\.', '错误的', '<', '?', 'incorrect', '  \n', '<<<<', ')', ' <<<', '\t  \n', '@\\', '错', ' Disclaimer', '.\\', '-Americ']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Guadalajara on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Americas', ' continents', ' Europe', 'Europe', ' Africa', '大陆', ' asia', ' Mexico', 'continental', 'Africa', ' América', ' Oce', '北美', ' continental', 'Mexico', 'Argentina', '美洲', ' Argentina', ' mexico', 'Canada', ' Europa', ';**', ' continente', ' Antarctica', ' Countries', ' Canada', 'Spain', ' Spain', ';', ' europe']

Generation (6 tokens):
```text
North America; MXN<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.230443 | 0.794182    |    0.00463659 |
| NA      | -1.98044  | 0.138008    |    0.00463653 |
| N       | -3.48044  | 0.0307938   |    0.00463653 |
| <       | -3.73044  | 0.0239822   |   -0.120363   |
| Na      | -5.85544  | 0.00286427  |   -0.120363   |
| ;       | -5.98044  | 0.00252771  |   -0.120363   |
| <N      | -6.60544  | 0.00135298  |   -0.120363   |
| North   | -6.98044  | 0.000929891 |    0.379637   |
| <span   | -7.79294  | 0.000412637 |   -0.182863   |
| <br     | -7.85544  | 0.000387636 |   -0.0578632  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '.', '<think>', '</', '**', ';', '\\n', '<|file_sep|>', '.Category', '\\', ' Incorrect', '<\\/', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '错误的', '\\.', 'incorrect', '<', '?', '  \n', '<<<<', '错', ')', ' <<<', '\t  \n', '错误', '-Americ', ' Disclaimer', '.\\']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Guadalajara on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Americas', ' continents', ' Europe', 'Europe', ' Africa', '大陆', ' asia', 'Africa', 'continental', ' Oce', ' América', ' Mexico', ' continental', '北美', 'Argentina', '美洲', 'Mexico', ' Argentina', ' Europa', ' mexico', ';**', ' continente', 'Canada', ';', ' Countries', ' Spain', ' europe', ' Continental', ' Antarctica', 'Spain']

Generation (6 tokens):
```text
North America; MXN<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| North   | -0.193074 | 0.824421    |     0.0420053 |
| NA      | -2.19307  | 0.111573    |    -0.207995  |
| <       | -3.69307  | 0.0248953   |    -0.0829947 |
| N       | -3.69307  | 0.0248953   |    -0.207995  |
| ;       | -5.69307  | 0.00336922  |     0.167006  |
| Na      | -5.94307  | 0.00262395  |    -0.207994  |
| <N      | -6.56807  | 0.0014045   |    -0.0829945 |
| North   | -7.00557  | 0.000906813 |     0.354506  |
| <span   | -7.63057  | 0.000485382 |    -0.0204945 |
| <br     | -7.81807  | 0.000402396 |    -0.0204945 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<|im_start|>', '</tool_response>', '<think>', '</', ';', '\\n', '**', '<|file_sep|>', '.Category', '\\', '<\\/', ' Incorrect', '\\.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '?', '<', '  \n', '错误的', 'incorrect', ')', '\t  \n', '<<<<', ' <<<', '.\\', '-Americ', '错', '@\\', ' Disclaimer']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'MXN']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.
