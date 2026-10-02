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
elapsed_seconds: 6.24
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Europe to South America. Positive answer_log_odds_shift favours first token 'South' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Europe toward South America with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='South') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |            -4.24683e-07 |        6.35305e-07 |            0.921584 |                0.921584 |    0 |
| raw J-coordinate exchange     |             9.8125      |        0.0094614   |            0.751612 |                0.761073 |    0 |
| raw plain-coordinate exchange |            -0.0625004   |        6.0542e-07  |            0.934874 |                0.934875 |    0 |
| matched-random delta          |             0.0624996   |        6.58749e-07 |            0.897697 |                0.897697 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Munich on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', 'Asia', ' Europa', ' Asia', '欧洲', ' continents', 'Europa', ' EURO', '大陆', ' Germany', 'Germany', 'urope', '在欧洲', '西欧', '欧洲的', 'continental', 'Africa', ' asia', ' Oce', ' Европа', ' Africa', ' continental', ' Americas', ';', ' Scandin', ' Europ', ' Austria', ';**', ' Antarctica', '欧盟']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0816616 | 0.921584    |             0 |
| <        | -2.83166   | 0.0589149   |             0 |
| Europe   | -4.70666   | 0.00903489  |             0 |
| E        | -6.08166   | 0.00228438  |             0 |
| ;        | -6.33166   | 0.00177908  |             0 |
| Europa   | -6.95666   | 0.00095227  |             0 |
| European | -7.20666   | 0.000741629 |             0 |
| <E       | -7.33166   | 0.000654485 |             0 |
| EU       | -7.33166   | 0.000654485 |             0 |
| europe   | -7.95666   | 0.000350321 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '  \n', '.', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '<\\/', '</', '\\n', '｡', '\n   \n', ' **.**', '.<', '\\.', ';</', '<<<<', './.', '  \n\n', '\t\n', '-US', '\n  \n', ' <--', '<br']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Munich on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Europe', 'Europe', ' continents', 'Africa', ' Oce', ' Africa', ' Americas', ' europe', ' asia', '大陆', ' Europa', 'continental', ' Antarctica', ';', ' continental', ';**', 'asia', '欧洲', ' Countries', ';;', '亚洲', 'Europa', 'urope', ' EURO', ' africa', '__;', ' continente', '；', '北美', ' América']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Europe  | -0.285535 | 0.751612   |     -0.203874 |
| <       | -2.16054  | 0.115263   |      0.671126 |
| Africa  | -3.16054  | 0.042403   |      6.42113  |
| Asia    | -3.41054  | 0.0330235  |      6.04613  |
| ;       | -4.66054  | 0.0094614  |      1.67113  |
| North   | -4.66054  | 0.0094614  |      5.54613  |
| South   | -4.66054  | 0.0094614  |      9.60863  |
| Europe  | -5.53554  | 0.0039441  |     -0.828874 |
| E       | -5.84804  | 0.00288556 |      0.233626 |
| Europa  | -6.53554  | 0.00145095 |      0.421126 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '.', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '</', '<\\/', '｡', '\\n', '\n   \n', ' **.**', '.<', '\\.', ';</', './.', '<<<<', '\t\n', '  \n\n', '-US', '\n  \n', ' */', '***']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['South America', 'BRL']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Munich on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', 'Asia', ' Europa', ' Asia', ' continents', '欧洲', 'Europa', '大陆', ' EURO', 'Germany', ' Germany', 'urope', 'Africa', 'continental', '欧洲的', '西欧', '在欧洲', ' asia', ' Oce', ' Africa', ' Европа', ' continental', ' Americas', ';', ' Europ', ' Scandin', ' Antarctica', ';**', ' Austria', 'ustria']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0673435 | 0.934874    |     0.0143182 |
| <        | -3.06734   | 0.0465446   |    -0.235682  |
| Europe   | -4.69234   | 0.00916518  |     0.0143185 |
| E        | -6.19234   | 0.00204503  |    -0.110682  |
| ;        | -6.44234   | 0.00159267  |    -0.110682  |
| Europa   | -7.06734   | 0.000852495 |    -0.110682  |
| European | -7.31734   | 0.000663924 |    -0.110682  |
| <E       | -7.44234   | 0.000585911 |    -0.110682  |
| EU       | -7.44234   | 0.000585911 |    -0.110682  |
| europe   | -7.94234   | 0.000355373 |     0.0143185 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', ' -->', '.', '  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';', ' <<<', '<\\/', '\\n', '</', '｡', '\n   \n', ' **.**', '.<', '\\.', ';</', '<<<<', '\t\n', '  \n\n', '-US', './.', '<br', '\n  \n', '\\")']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['South America', 'BRL']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Munich on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', ' europe', ' Europa', 'Asia', ' Asia', '欧洲', ' continents', ' Germany', 'Europa', 'Germany', ' EURO', '大陆', 'urope', '欧洲的', '西欧', 'continental', '在欧洲', ' asia', 'Africa', ' Европа', ' Oce', ' Americas', ';', ' Africa', ' continental', ' Europ', ' Austria', ' Scandin', 'ustria', ';**', '欧盟']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |     log p |           p |   delta log p |
|:---------|----------:|------------:|--------------:|
| Europe   | -0.107923 | 0.897697    |    -0.0262615 |
| <        | -2.48292  | 0.0834988   |     0.348738  |
| Europe   | -4.85792  | 0.0077666   |    -0.151261  |
| E        | -6.10792  | 0.00222517  |    -0.0262613 |
| ;        | -6.23292  | 0.0019637   |     0.0987387 |
| Europa   | -6.98292  | 0.000927588 |    -0.0262613 |
| <E       | -6.98292  | 0.000927588 |     0.348739  |
| European | -7.10792  | 0.000818593 |     0.0987387 |
| EU       | -7.73292  | 0.000438161 |    -0.401261  |
| <span    | -7.85792  | 0.000386676 |     0.286238  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '\t  \n', '<|file_sep|>', '<think>', '.Category', '.', ' -->', '  \n', ';', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <<<', '</', '\\n', '<\\/', '｡', '\n   \n', ' **.**', '.<', '\\.', ';</', '  \n\n', '<<<<', '\t\n', '\n  \n', './.', '-US', '<br', '.\\']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.
