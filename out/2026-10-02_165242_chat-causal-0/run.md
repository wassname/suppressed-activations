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

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Madrid to Mexico City. Positive answer_log_odds_shift favours first token 'Mexico' over 'Madrid'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Madrid toward Mexico City with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Mexico') |   p(first='Madrid') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|--------------------:|------------------------:|-----:|
| Base                          |            -1.19209e-07 |         1.54267e-05 |         0.765739    |                0.765755 |    0 |
| raw J-coordinate exchange     |            18.4375      |         0.96902     |         0.000472974 |                0.969493 |    0 |
| raw plain-coordinate exchange |             0.25        |         1.92886e-05 |         0.745652    |                0.745672 |    0 |
| matched-random delta          |             0.3125      |         1.78302e-05 |         0.647514    |                0.647531 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Barcelona, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', 'Madrid', 'Paris', 'London', ' Paris', ' Lisbon', '巴黎', ' PARIS', ' Bogotá', ' Dublin', ' Buenos', ' madrid', ' London', ' Helsinki', 'Berlin', ' Londres', ' Amsterdam', ' Berlin', ' Prague', ' Budapest', ' Caracas', 'Spain', ' Oslo', '巴塞罗那', 'city', '马德里', ' Istanbul', ' Stockholm', ' París', ' Lisboa', ' Ankara', ' Athens']

Generation (4 tokens):
```text
Madrid; EUR<|im_end|>
```

| token     |     log p |           p |   delta log p |
|:----------|----------:|------------:|--------------:|
| Madrid    | -0.266914 | 0.765739    |             0 |
| Barcelona | -1.64191  | 0.193609    |             0 |
| <         | -4.01691  | 0.0180085   |             0 |
| Spain     | -4.89191  | 0.00750704  |             0 |
| Mad       | -5.14191  | 0.00584649  |             0 |
| <span     | -6.51691  | 0.00147822  |             0 |
| ;         | -6.95441  | 0.000954414 |             0 |
| Se        | -6.95441  | 0.000954414 |             0 |
| Bar       | -7.14191  | 0.000791237 |             0 |
| M         | -7.57941  | 0.000510861 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '<|im_start|>', '  \n', '<think>', '<|file_sep|>', '.Category', ';', '.', ' -->', ' <<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.<', '\n   \n', ';</', '｡', '<\\/', '\\n', ' **.**', '</', '\t\n', '.;', '-US', '<<<<', '\\.', ';charset', ' <--', '-Americ', '  \n\n']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Madrid', 'EUR']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Barcelona, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', ' Buenos', 'Madrid', ' Bogotá', ' Caracas', 'Paris', 'city', ' Ciudad', ' Brasília', 'Mexico', ' Mexico', 'London', ' Bangkok', ' Jakarta', ' Guadalajara', ' mexico', ' Paris', ' Lisbon', ' México', ' Riyadh', ' São', ' Tehran', 'São', ' Tokyo', ' NYC', ' madrid', ' Helsinki', ' Toronto', ' PARIS', ' Londres', 'Chicago', ' Seoul']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Mexico  | -0.0314704 | 0.96902     |    11.0479    |
| <       | -4.15647   | 0.0156627   |    -0.139557  |
| Mé      | -5.78147   | 0.00308418  |     8.79794   |
| Mex     | -5.90647   | 0.00272178  |    10.8917    |
| M       | -6.40647   | 0.00165084  |     1.17294   |
| ;       | -6.90647   | 0.00100129  |     0.0479431 |
| Mexico  | -7.15647   | 0.000779802 |    11.3917    |
| <span   | -7.21897   | 0.000732556 |    -0.702057  |
| MX      | -7.21897   | 0.000732556 |     8.61044   |
| Ci      | -7.28147   | 0.000688173 |     6.61044   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\\n', '**', '.', ';', ' Incorrect', '\\', '</', '  \n', ' incorrect', '错误', '.\\', '错误的', '</tool_response>', 'incorrect', ' <--', ' <<<', '<think>', '错', '是错误的', '<|im_start|>', '  \n\n', '\n\n', '<', ')', '<<<', '的错误', '\n', '错的', ' -->']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Mexico City', 'MXN']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Barcelona, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', 'Madrid', 'Paris', 'London', ' Paris', '巴黎', ' Lisbon', ' PARIS', ' Bogotá', ' Buenos', ' Dublin', ' madrid', 'Berlin', ' Budapest', ' Helsinki', ' London', ' Berlin', ' Prague', ' Londres', ' Amsterdam', ' Caracas', 'city', 'Spain', ' Oslo', '巴塞罗那', ' Istanbul', '马德里', ' París', ' Stockholm', ' Lisboa', ' Ankara', ' Munich']

Generation (4 tokens):
```text
Madrid; EUR<|im_end|>
```

| token     |     log p |           p |   delta log p |
|:----------|----------:|------------:|--------------:|
| Madrid    | -0.293496 | 0.745652    |    -0.0265825 |
| Barcelona | -1.5435   | 0.213633    |     0.0984175 |
| <         | -4.0435   | 0.0175361   |    -0.0265827 |
| Spain     | -4.7935   | 0.00828345  |     0.0984173 |
| Mad       | -5.1685   | 0.00569312  |    -0.0265827 |
| <span     | -6.5435   | 0.00143945  |    -0.0265827 |
| ;         | -6.981    | 0.000929377 |    -0.0265827 |
| Se        | -6.981    | 0.000929377 |    -0.0265827 |
| Bar       | -7.106    | 0.000820172 |     0.0359173 |
| Madrid    | -7.5435   | 0.000529543 |     0.0359173 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '<|im_start|>', '  \n', '<think>', '<|file_sep|>', '.Category', ';', '.', ' -->', ' <<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.<', '\n   \n', ';</', '｡', ' **.**', '<\\/', '\\n', '</', '\t\n', '-US', '.;', '<<<<', '\\.', '-Americ', ' <--', './.', '  \n\n']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Mexico City', 'MXN']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Barcelona, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', 'Madrid', 'Paris', ' Paris', 'London', ' Lisbon', '巴黎', ' PARIS', ' Bogotá', ' Buenos', ' Dublin', ' madrid', ' London', ' Helsinki', ' Berlin', ' Amsterdam', 'city', ' Budapest', ' Londres', 'Berlin', 'Spain', ' Prague', ' Caracas', '巴塞罗那', ' Oslo', ' Istanbul', '马德里', ' París', ' Stockholm', ' Lisboa', ' Athens', ' Munich']

Generation (4 tokens):
```text
Madrid; EUR<|im_end|>
```

| token     |     log p |           p |   delta log p |
|:----------|----------:|------------:|--------------:|
| Madrid    | -0.434616 | 0.647514    |    -0.167702  |
| Barcelona | -1.18462  | 0.305864    |     0.457298  |
| <         | -3.93462  | 0.0195532   |     0.0822978 |
| Spain     | -4.55962  | 0.0104661   |     0.332298  |
| Mad       | -5.55962  | 0.00385026  |    -0.417702  |
| <span     | -6.18462  | 0.00206089  |     0.332298  |
| Se        | -6.43462  | 0.00160503  |     0.519798  |
| ;         | -6.55962  | 0.00141643  |     0.394798  |
| Bar       | -6.68462  | 0.00125     |     0.457298  |
| M         | -7.37212  | 0.000628537 |     0.207298  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '<|im_start|>', '  \n', '<think>', '<|file_sep|>', '.Category', '.', ';', ' -->', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n   \n', ';</', ' **.**', '｡', '\\n', '</', '<\\/', '.;', '-US', '\t\n', '\\.', '<<<<', ' <--', '-Americ', '  \n\n', ';charset']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Madrid', 'EUR']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.
