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
elapsed_seconds: 6.85
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Oceania to North America. Positive answer_log_odds_shift favours first token 'O' over 'North'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Oceania toward North America with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='O') |   p(first='North') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|-------------------:|------------------------:|-----:|
| Base                          |                  0      |    0.396013    |         0.0018339  |                0.397847 |    0 |
| raw J-coordinate exchange     |                -16.875  |    9.52491e-06 |         0.940259   |                0.940269 |    0 |
| raw plain-coordinate exchange |                 -0.625  |    0.409571    |         0.00354348 |                0.413114 |    0 |
| matched-random delta          |                  0.1875 |    0.288408    |         0.00110725 |                0.289515 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Sydney on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Australia', ' Oce', 'Australia', ' continents', ' Antarctica', '大陆', ' Americas', ' Europe', ' australia', 'Europe', ' Africa', ' asia', 'Africa', 'continental', 'ustralia', ' continente', ';', ';**', ' Austral', ' continental', ' Австра', '；', 'Canada', '北美', ';;', '澳洲', ' Countries', '亚洲', '澳大利亚', ' Australien']

Generation (6 tokens):
```text
Oceania; AUD<|im_end|>
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| O         | -0.926308 | 0.396013   |             0 |
| Australia | -1.17631  | 0.308415   |             0 |
| <         | -1.80131  | 0.165083   |             0 |
| Oce       | -2.67631  | 0.0688168  |             0 |
| OC        | -4.42631  | 0.0119586  |             0 |
| ;         | -5.17631  | 0.00564882 |             0 |
| Asia      | -5.30131  | 0.00498507 |             0 |
| >         | -5.42631  | 0.00439931 |             0 |
| >O        | -5.42631  | 0.00439931 |             0 |
| Australia | -5.73881  | 0.0032186  |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '</tool_response>', '.Category', '\t  \n', '<think>', '.', '<\\/', '\t\n', '</', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.<', '<<<<', '  \n', ';', '\\n', ' \n\n', ' -->', '或未', '/AP', '/A', ' \n', '\\.', '-Americ', ' <<<', '<br', '/OR', '/.', '<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Oceania', 'AUD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Sydney on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Canada', ' Canada', 'Asia', '北美', ' Americas', ' continents', ' Asia', '大陆', ' Oce', ' Antarctica', ' Australia', ' Europe', 'continental', 'Australia', 'Europe', ';;', ' continental', ' canada', ';', ';**', ' América', ' continente', ' Africa', ' Countries', ' asia', ' Canadá', ' Amérique', 'USA', '__;', 'Africa', ' USA', 'America']

Generation (5 tokens):
```text
North America; CAD<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| North   | -0.0615995 | 0.940259    |      6.23971  |
| <       | -3.5616    | 0.0283934   |     -1.76029  |
| NA      | -4.0616    | 0.0172215   |      6.48971  |
| North   | -5.3116    | 0.00493403  |      6.55221  |
| N       | -5.6866    | 0.00339111  |      5.11471  |
| ;       | -6.5616    | 0.00141362  |     -1.38529  |
| <N      | -7.1866    | 0.000756658 |      3.05221  |
| >       | -7.5616    | 0.000520043 |     -2.13529  |
| <br     | -8.4366    | 0.000216786 |     -0.385291 |
| South   | -8.5616    | 0.000191313 |     -1.57279  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ' Incorrect', ' Wait', ' incorrect', '错误', ' <--', '错', 'wait', 'incorrect', ' -->', '错误的', ' Note', ' Wrong', 'Incorrect', ' wait', '是错误的', '的错误', ' incorrectly', '.', '  \n', 'Wait', '错的', ' WRONG', ' mistakenly', '.*', ' ERROR', '.--', '.<', ' Disclaimer', '**']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'CAD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Sydney on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' Oce', ' Australia', ' continents', 'Australia', ' Antarctica', '大陆', ' Americas', ' Europe', 'Europe', ' Africa', ' australia', ' asia', 'Africa', 'continental', 'Canada', '北美', ';', ' continente', ';**', 'ustralia', ' continental', ';;', '；', ' Austral', ' Countries', ' Австра', ' Canada', '亚洲', '__;', '澳洲']

Generation (6 tokens):
```text
Oceania; AUD<|im_end|>
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| O         | -0.892645 | 0.409571   |     0.0336631 |
| Australia | -1.26765  | 0.281494   |    -0.091337  |
| <         | -1.76765  | 0.170735   |     0.033663  |
| Oce       | -2.64265  | 0.0711728  |     0.033663  |
| OC        | -4.39264  | 0.012368   |     0.0336633 |
| ;         | -4.89264  | 0.00750156 |     0.283663  |
| Asia      | -5.39264  | 0.00454992 |    -0.0913367 |
| >         | -5.39264  | 0.00454992 |     0.0336633 |
| >O        | -5.39264  | 0.00454992 |     0.0336633 |
| Australia | -5.64264  | 0.00354348 |     0.0961633 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '</tool_response>', '.Category', '\t  \n', '<think>', '.', '<\\/', '\t\n', '</', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', '<<<<', '.<', ';', '\\n', '或未', ' -->', ' \n\n', '/A', ' \n', '/AP', '\\.', '-Americ', '<br', ' <<<', '/OR', ' <![', '/.']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['North America', 'CAD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Sydney on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Australia', 'Asia', ' Asia', 'Australia', ' Oce', ' continents', ' Antarctica', '大陆', ' Americas', ' australia', ' Europe', ' Africa', 'Europe', ' asia', 'ustralia', ';**', ';', 'continental', ' Austral', 'Africa', ' Австра', ' continente', ';;', '；', '澳洲', 'Canada', '澳大利亚', ' continental', ' Countries', '北美', ' Australien', ' Canada']

Generation (6 tokens):
```text
Oceania; AUD<|im_end|>
```

| token     |    log p |          p |   delta log p |
|:----------|---------:|-----------:|--------------:|
| Australia | -1.24338 | 0.288408   |    -0.0670711 |
| O         | -1.24338 | 0.288408   |    -0.317071  |
| Oce       | -1.61838 | 0.19822    |     1.05793   |
| <         | -1.86838 | 0.154374   |    -0.0670711 |
| Australia | -4.24338 | 0.014359   |     1.49543   |
| ;         | -4.61838 | 0.00986878 |     0.557929  |
| OC        | -4.86838 | 0.00768581 |    -0.442071  |
| >         | -5.24338 | 0.00528238 |     0.182929  |
| >O        | -5.24338 | 0.00528238 |     0.182929  |
| Asia      | -5.43088 | 0.00437924 |    -0.129571  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '</tool_response>', '.Category', '\t  \n', '.', '<think>', '<\\/', '\t\n', '</', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.<', ';', '  \n', '<<<<', ' -->', '\\n', ' \n\n', '\\.', '或未', ' \n', '/A', '/AP', '-Americ', ' <<<', '<br', '/.', '/OR', '<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Oceania', 'AUD']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.
