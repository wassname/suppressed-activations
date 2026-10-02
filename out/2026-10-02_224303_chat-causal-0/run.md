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
elapsed_seconds: 6.30
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Europe to Asia. Positive answer_log_odds_shift favours first token 'Asia' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Europe toward Asia with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Asia') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|------------------:|--------------------:|------------------------:|-----:|
| Base                          |             2.83122e-07 |       2.98304e-05 |          0.898091   |                0.898121 |    0 |
| raw J-coordinate exchange     |            14.5625      |       0.448727    |          0.00640075 |                0.455128 |    0 |
| raw plain-coordinate exchange |            -0.0624997   |       2.77122e-05 |          0.888129   |                0.888157 |    0 |
| matched-random delta          |             2.83122e-07 |       2.81369e-05 |          0.847106   |                0.847134 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Lyon on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', 'France', ' continents', ' France', 'Asia', ' Europa', '大陆', '欧洲', ' Asia', 'Africa', 'Europa', ' Africa', 'continental', '欧洲的', 'urope', ' EURO', ' continental', '西欧', '在欧洲', ' africa', ' Европа', ' asia', ' FRANCE', ';**', ' Americas', ';', ' continente', ' Oce', '欧盟', ' Countries']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |     log p |           p |   delta log p |
|:---------|----------:|------------:|--------------:|
| Europe   | -0.107484 | 0.898091    |             0 |
| <        | -2.48248  | 0.0835355   |             0 |
| Europe   | -5.48248  | 0.00415899  |             0 |
| E        | -5.73248  | 0.00323902  |             0 |
| ;        | -5.98248  | 0.00252255  |             0 |
| <E       | -6.73248  | 0.00119157  |             0 |
| Europa   | -7.10748  | 0.000818953 |             0 |
| EU       | -7.10748  | 0.000818953 |             0 |
| European | -7.35748  | 0.000637802 |             0 |
| Africa   | -7.35748  | 0.000637802 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '  \n', '.', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '｡', '<\\/', '</', ' **.**', '\n   \n', '\\n', '.<', ';</', '\\.', '<<<<', '-US', '  \n\n', '\t\n', './.', '\n  \n', ' </', ' */']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Lyon on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Africa', 'Africa', ' asia', ' continents', ' Europe', 'Europe', '亚洲', '大陆', ' Americas', ' africa', 'asia', ' Oce', 'continental', ' europe', ' Antarctica', ';**', ';', ' continental', 'India', ';;', ' continente', ' Countries', 'China', '__;', '；', ' Europa', '北美', ' Euras', '东亚', 'Australia']

Generation (5 tokens):
```text
Asia; INR<|im_end|>
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| Asia    | -0.80134 | 0.448727   |       9.61864 |
| <       | -1.05134 | 0.349469   |       1.43114 |
| Africa  | -1.92634 | 0.14568    |       5.43114 |
| ;       | -4.17634 | 0.0153546  |       1.80614 |
| Europe  | -5.05134 | 0.00640075 |      -4.94386 |
| Africa  | -5.17634 | 0.00564864 |       6.24364 |
| Asia    | -5.42634 | 0.00439917 |       9.99364 |
| A       | -5.92634 | 0.00266823 |       5.74364 |
| AS      | -5.92634 | 0.00266823 |       8.93114 |
| >       | -6.05134 | 0.0023547  |       2.74364 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ' incorrect', ' Incorrect', '</', '错误', '**', 'incorrect', '错误的', '  \n', '\\n', ' Wrong', '<|im_start|>', ')', 'Incorrect', ' incorrectly', '错', '错的', '的错误', '</tool_response>', '<think>', '是错误的', '?', ' mistakenly', '\n', ';', ' <--', ' Wait', ' mistake', '\\']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'INR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Lyon on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', 'France', ' France', ' continents', ' Europa', 'Asia', '大陆', '欧洲', 'Africa', 'Europa', ' Asia', ' Africa', '欧洲的', '西欧', 'continental', 'urope', ' EURO', ' continental', '在欧洲', ' Европа', ' FRANCE', ' africa', ';**', ' Americas', ' asia', ';', ' continente', ' Oce', '欧盟', ' Countries']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |     log p |           p |   delta log p |
|:---------|----------:|------------:|--------------:|
| Europe   | -0.118638 | 0.888129    |    -0.0111545 |
| <        | -2.36864  | 0.0936081   |     0.113846  |
| Europe   | -5.61864  | 0.00362958  |    -0.136155  |
| E        | -5.74364  | 0.00320309  |    -0.0111547 |
| ;        | -5.86864  | 0.00282672  |     0.113845  |
| <E       | -6.49364  | 0.00151303  |     0.238845  |
| Europa   | -7.11864  | 0.000809869 |    -0.0111547 |
| EU       | -7.24364  | 0.000714707 |    -0.136155  |
| European | -7.36864  | 0.000630727 |    -0.0111547 |
| <span    | -7.49364  | 0.000556614 |     0.113845  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '  \n', '.', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '｡', '</', '\\n', '<\\/', ' **.**', '\n   \n', '.<', ';</', '\\.', '<<<<', '-US', '  \n\n', '\t\n', './.', '\n  \n', ';charset', '<br']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'INR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Lyon on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', ' France', 'France', ' Europa', ' continents', 'Asia', '欧洲', '大陆', ' Asia', 'Europa', 'Africa', ' Africa', 'urope', '欧洲的', ' EURO', '西欧', 'continental', ' continental', ' FRANCE', '在欧洲', ';**', ' asia', ' Европа', ' africa', ' Americas', ';', '欧盟', ' continente', ' Countries', ';;']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |    log p |           p |   delta log p |
|:---------|---------:|------------:|--------------:|
| Europe   | -0.16593 | 0.847106    |     -0.058446 |
| <        | -2.04093 | 0.129908    |      0.441554 |
| Europe   | -4.79093 | 0.00830473  |      0.691554 |
| ;        | -5.66593 | 0.00346193  |      0.316554 |
| E        | -5.91593 | 0.00269615  |     -0.183446 |
| <E       | -6.54093 | 0.00144315  |      0.191554 |
| <span    | -7.29093 | 0.000681694 |      0.316554 |
| Europa   | -7.29093 | 0.000681694 |     -0.183446 |
| europe   | -7.29093 | 0.000681694 |      0.316554 |
| European | -7.47843 | 0.000565144 |     -0.120946 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', '.', ' -->', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '</', '\n   \n', '｡', '.<', '\\n', ' **.**', '<\\/', '\\.', ';</', '  \n\n', '\n  \n', '<<<<', '\t\n', './.', '-US', ' </', '<br']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.
