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
elapsed_seconds: 10.40
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Canberra to Ottawa. Positive answer_log_odds_shift favours first token 'Can' over 'O'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Canberra toward Ottawa with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Can') |   p(first='O') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|---------------:|------------------------:|-----:|
| Base                          |                  0      |      0.688116    |    9.03972e-05 |                0.688207 |    0 |
| raw J-coordinate exchange     |                -18.5625 |      6.50783e-05 |    0.985191    |                0.985256 |    0 |
| raw plain-coordinate exchange |                 -0.1875 |      0.68697     |    0.000108858 |                0.687079 |    0 |
| matched-random delta          |                 -0.625  |      0.631151    |    0.000154903 |                0.631306 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Sydney, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['London', ' London', ' Canberra', ' Melbourne', ' Jakarta', '悉尼', '伦敦', ' Londres', 'Paris', ' Toronto', 'Toronto', ' Buenos', ' Brisbane', ' Tokyo', ' Nairobi', ' Johannesburg', ' london', ' Auckland', ' Bangkok', ' Dublin', 'city', 'Jakarta', ' Riyadh', ' Westminster', 'uckland', ' لندن', ' Brasília', ' Madrid', ' Londra', '首都', ' Paris', '杭州']

Generation (5 tokens):
```text
Canberra; AUD<|im_end|>
```

| token      |     log p |           p |   delta log p |
|:-----------|----------:|------------:|--------------:|
| Can        | -0.373797 | 0.688116    |             0 |
| <          | -1.8738   | 0.15354     |             0 |
| Sy         | -1.9988   | 0.135498    |             0 |
| Canberra   | -5.6238   | 0.0036109   |             0 |
| Australian | -5.8738   | 0.00281218  |             0 |
| C          | -6.4363   | 0.00160233  |             0 |
| Camb       | -6.4988   | 0.00150525  |             0 |
| Australia  | -6.5613   | 0.00141405  |             0 |
| Mel        | -6.9363   | 0.000971862 |             0 |
| CAN        | -6.9363   | 0.000971862 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '\t  \n', '.', '</tool_response>', '<think>', '.Category', '<\\/', '\t\n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', '</', '.<', '<<<<', ';', ' <<<', '\\n', '<br', ' \n', ' -->', '/AP', '-Americ', '<', '\\.', './.', ' <![', '/.', ' \n\n', '/A']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Canberra', 'AUD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Sydney, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Toronto', 'Toronto', 'London', ' Ottawa', ' Montreal', ' London', ' Montréal', 'Paris', 'Canada', ' Buenos', ' Canberra', ' Winnipeg', ' Vancouver', ' Londres', 'city', '伦敦', ' Paris', ' Bogotá', ' NYC', ' Brasília', ' Tokyo', ' Calgary', ' Canada', '北京', ' Jakarta', ' Melbourne', '多伦多', ' london', ' Madrid', '首都', '悉尼', 'ancouver']

Generation (6 tokens):
```text
Ottawa; CAD<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| O       | -0.0149197 | 0.985191    |      9.29638  |
| <       | -4.63992   | 0.00965847  |     -2.76612  |
| Mont    | -6.88992   | 0.001018    |      7.26513  |
| Canada  | -7.26492   | 0.000699657 |      0.358877 |
| Toronto | -7.51492   | 0.000544894 |      3.35888  |
| Ont     | -7.63992   | 0.000480867 |      5.67138  |
| >O      | -8.51492   | 0.000200455 |      6.54638  |
| 'O      | -8.63992   | 0.000176901 |      7.10888  |
| <span   | -8.63992   | 0.000176901 |     -0.828622 |
| <p      | -8.82742   | 0.000146656 |     -1.26612  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '</tool_response>', '.<', '<|file_sep|>', ' -->', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<\\/', '.Category', ';', '.', ' Incorrect', ',<', '<br', '/C', ' <--', '  \n', '\t  \n', '</', '<', '\x00', 'incorrect', ';<', '-Americ', '\t\n', '<<<<', '.--', '\\n', '"<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Ottawa', 'CAD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Sydney, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['London', ' London', ' Canberra', ' Melbourne', ' Jakarta', '悉尼', '伦敦', ' Londres', 'Paris', 'Toronto', ' Toronto', ' Buenos', ' Tokyo', ' london', ' Johannesburg', ' Nairobi', 'city', ' Dublin', ' Bangkok', ' Brisbane', ' Auckland', 'Jakarta', ' لندن', ' Madrid', ' Brasília', ' Riyadh', ' Westminster', 'uckland', ' Londra', '首都', ' Paris', ' Bogotá']

Generation (5 tokens):
```text
Canberra; AUD<|im_end|>
```

| token      |     log p |          p |   delta log p |
|:-----------|----------:|-----------:|--------------:|
| Can        | -0.375464 | 0.68697    |   -0.00166678 |
| <          | -1.87546  | 0.153284   |   -0.00166678 |
| Sy         | -2.00046  | 0.135273   |   -0.00166678 |
| Canberra   | -5.62546  | 0.00360489 |   -0.00166702 |
| Australian | -5.75046  | 0.0031813  |    0.123333   |
| C          | -6.37546  | 0.00170283 |    0.060833   |
| Australia  | -6.43796  | 0.00159966 |    0.123333   |
| Camb       | -6.43796  | 0.00159966 |    0.060833   |
| CAN        | -6.68796  | 0.00124582 |    0.248333   |
| A          | -6.87546  | 0.00103282 |    0.123333   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '\t  \n', '</tool_response>', '.Category', '.', '<think>', '<\\/', '\t\n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', '</', '.<', '<<<<', ';', ' <<<', '\\n', '<br', ' \n', ' -->', '-Americ', '/AP', '\\.', './.', '<', ' <![', '/.', ' \n\n', '/A']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Ottawa', 'CAD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Sydney, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['London', ' London', ' Canberra', ' Melbourne', ' Jakarta', '悉尼', '伦敦', ' Londres', 'Paris', ' Toronto', ' Buenos', 'Toronto', ' Brisbane', ' Tokyo', ' Auckland', ' Nairobi', ' Dublin', ' london', ' Bangkok', 'city', ' Johannesburg', ' Westminster', 'uckland', 'Jakarta', ' لندن', ' Riyadh', '首都', ' Brasília', ' Paris', ' Madrid', ' Londra', 'Australia']

Generation (5 tokens):
```text
Canberra; AUD<|im_end|>
```

| token      |    log p |          p |   delta log p |
|:-----------|---------:|-----------:|--------------:|
| Can        | -0.46021 | 0.631151   |    -0.0864128 |
| Sy         | -1.71021 | 0.180828   |     0.288587  |
| <          | -1.83521 | 0.15958    |     0.0385872 |
| Australian | -5.33521 | 0.0048189  |     0.538587  |
| Canberra   | -5.46021 | 0.00425266 |     0.163587  |
| Australia  | -6.08521 | 0.00227629 |     0.476087  |
| Camb       | -6.27271 | 0.00188711 |     0.226087  |
| C          | -6.58521 | 0.00138064 |    -0.148913  |
| ;          | -6.77271 | 0.00114459 |     0.226087  |
| Mel        | -6.77271 | 0.00114459 |     0.163587  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '.', '\t  \n', '</tool_response>', '<think>', '.Category', '\t\n', '<\\/', '  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '</', '.<', '<<<<', ';', ' <<<', '<br', '\\n', ' \n', ' -->', '\\.', '-Americ', '/AP', './.', '<', ' \n\n', '\n   \n', ' <![', '/.']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Canberra', 'AUD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.
