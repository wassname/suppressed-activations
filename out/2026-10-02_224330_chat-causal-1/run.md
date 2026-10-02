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
elapsed_seconds: 4.94
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is South America to Europe. Positive answer_log_odds_shift favours first token 'South' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes South America toward Europe with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='South') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |                  0      |        0.952392    |         9.1536e-05  |                0.952484 |    0 |
| raw J-coordinate exchange     |                -16.25   |        0.000874965 |         0.959516    |                0.960391 |    0 |
| raw plain-coordinate exchange |                 -0.25   |        0.959332    |         0.000118391 |                0.95945  |    0 |
| matched-random delta          |                 -0.0625 |        0.936365    |         9.57998e-05 |                0.936461 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Rio de Janeiro on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' continents', ' Americas', '大陆', ' Oce', 'Asia', ' Europe', ' Asia', ' Africa', 'Europe', 'Africa', ' Antarctica', 'Argentina', ' América', ' Argentina', ' continental', 'continental', ' Brazil', ' continente', '美洲', ' asia', ' africa', ' europe', ';', ' Caribbean', ' Countries', ' Europa', ';**', '南美', ';;', ' Continental', ' Hemisphere', ' Brasil']

Generation (6 tokens):
```text
South America; BRL<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| South   | -0.0487782 | 0.952392    |             0 |
| <       | -3.54878   | 0.0287598   |             0 |
| S       | -4.92378   | 0.00727161  |             0 |
| SA      | -5.79878   | 0.00303126  |             0 |
| <S      | -5.92378   | 0.00267507  |             0 |
| ;       | -6.79878   | 0.00111514  |             0 |
| South   | -6.92378   | 0.000984105 |             0 |
| America | -7.29878   | 0.000676365 |             0 |
| Americ  | -7.54878   | 0.000526753 |             0 |
| <span   | -8.11128   | 0.000300135 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '</tool_response>', '<|file_sep|>', '.', '</', ';', '.Category', '  \n', '\\n', '**', '\t  \n', '\\', '\n   \n', '<br', '\\.', '<\\/', '"<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<<', '  \n\n', ';.', ' **.**', '<', '.ht', '@\\', '-Americ', ' -->']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['South America', 'BRL']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Rio de Janeiro on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' continents', ' europe', ' Europa', '大陆', '欧洲', 'Asia', ' Asia', 'Europa', ' continental', ' Americas', 'continental', ' Germany', 'Germany', ' Oce', 'Africa', ' Africa', ' Antarctica', '西欧', ' EURO', '欧洲的', 'urope', '在欧洲', ' continente', ';', ';**', ';;', ' Европа', ' Continental', ' Countries', ' France']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0413267 | 0.959516    |    9.25745    |
| <        | -3.54133   | 0.0289749   |    0.00745153 |
| Europe   | -5.91633   | 0.00269508  |    8.81995    |
| E        | -6.41633   | 0.00163465  |    7.06995    |
| Europa   | -6.79133   | 0.00112348  |    7.50745    |
| ;        | -7.04133   | 0.000874965 |   -0.242548   |
| South    | -7.04133   | 0.000874965 |   -6.99255    |
| Eu       | -7.29133   | 0.000681424 |    8.69495    |
| EU       | -7.41633   | 0.000601354 |    8.7887     |
| European | -7.41633   | 0.000601354 |    8.9137     |

Final-decode readout: ['<|im_end|>', '<|endoftext|>', ' Incorrect', ' incorrect', '是错误的', ' Wrong', '错误', 'incorrect', '的错误', 'Incorrect', '</think>', '错误的', ' <--', ' incorrectly', ' WRONG', ' FALSE', ' -->', '错', '\\n', '**', '错的', ' ERROR', '  \n', ' mistakenly', '不正确', 'Wrong', '.', ' mistake', ' �', ' wrong', ' <<<', ' Error']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Rio de Janeiro on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Americas', ' continents', ' Europe', 'Asia', '大陆', ' Oce', ' Asia', ' Africa', 'Europe', 'Africa', ' Antarctica', 'Argentina', ' América', ' Argentina', ' continental', 'continental', ' Brazil', ' continente', '美洲', ' asia', ' africa', ' europe', ';', ' Europa', ' Caribbean', ' Countries', ';;', ';**', ' Continental', ' Hemisphere', '南美', 'Latin']

Generation (6 tokens):
```text
South America; BRL<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| South   | -0.0415185 | 0.959332    |    0.00725966 |
| <       | -3.79152   | 0.0225613   |   -0.24274    |
| S       | -4.91652   | 0.00732459  |    0.00725937 |
| SA      | -5.91652   | 0.00269456  |   -0.117741   |
| <S      | -6.16652   | 0.00209853  |   -0.242741   |
| ;       | -6.66652   | 0.00127282  |    0.132259   |
| South   | -6.66652   | 0.00127282  |    0.257259   |
| America | -7.41652   | 0.000601239 |   -0.117741   |
| Americ  | -7.79152   | 0.000413225 |   -0.242741   |
| <span   | -8.22902   | 0.000266798 |   -0.11774    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '</tool_response>', '<|file_sep|>', '.', '</', ';', '.Category', '  \n', '\\n', '**', '\t  \n', '\\', '<br', '\n   \n', '<\\/', '\\.', '"<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.<', '<<<<', ';.', '  \n\n', '<', ' **.**', '@\\', '-Americ', ' -->', '.ht']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Rio de Janeiro on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Americas', ' continents', 'Asia', '大陆', ' Asia', ' Europe', ' Africa', ' Oce', 'Europe', 'Africa', 'Argentina', ' Argentina', ' América', ' Antarctica', ' Brazil', ' continental', 'continental', ' continente', '美洲', ' asia', ';', ' africa', ' Caribbean', ' europe', ' Countries', ';;', ';**', ' Brasil', '南美', ' Europa', ' Continental', 'Latin']

Generation (6 tokens):
```text
South America; BRL<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| South   | -0.06575 | 0.936365    |    -0.0169718 |
| <       | -3.19075 | 0.041141    |     0.358028  |
| S       | -4.81575 | 0.00810114  |     0.108028  |
| <S      | -5.44075 | 0.00433623  |     0.483028  |
| SA      | -6.19075 | 0.00204829  |    -0.391972  |
| South   | -6.31575 | 0.00180761  |     0.608028  |
| ;       | -6.44075 | 0.00159521  |     0.358028  |
| America | -7.19075 | 0.000753524 |     0.108028  |
| Americ  | -7.56575 | 0.000517889 |    -0.0169721 |
| <span   | -7.75325 | 0.000429345 |     0.358028  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '</tool_response>', '<|file_sep|>', '.', '</', ';', '.Category', '  \n', '\\n', '\\', '**', '\t  \n', '<br', '\n   \n', '\\.', '"<', '.<', '<\\/', ';.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n\n', '<<<<', '<', ' **.**', ' -->', '`;', '.ht', '@\\']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['South America', 'BRL']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.
