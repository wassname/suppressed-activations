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
elapsed_seconds: 7.73
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Berlin to Brasília. Positive answer_log_odds_shift favours first token 'Br' over 'Berlin'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Berlin toward Brasília with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Br') |   p(first='Berlin') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|----------------:|--------------------:|------------------------:|-----:|
| Base                          |            -1.78814e-07 |     0.00011861  |         0.620536    |             0.620655    |    0 |
| raw J-coordinate exchange     |             9.8125      |     0.000218776 |         6.26805e-05 |             0.000281457 |    0 |
| raw plain-coordinate exchange |            -0.1875      |     9.83865e-05 |         0.620886    |             0.620985    |    0 |
| matched-random delta          |             0.25        |     0.000133547 |         0.544135    |             0.544269    |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Munich, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Berlin', 'Berlin', ' Prague', 'Germany', ' Vienna', 'Paris', ' Germany', ' Frankfurt', 'London', ' München', ' Budapest', ' Madrid', '慕尼黑', 'Madrid', ' Austria', ' Helsinki', '维也纳', ' Paris', ' Amsterdam', ' Stuttgart', ' Zurich', ' London', ' Leipzig', ' Stockholm', 'Barcelona', ' berlin', ' Bav', ' Oslo', ' Bratis', ' Lisbon', ' Hamburg', ' Barcelona']

Generation (4 tokens):
```text
Berlin; EUR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Berlin  | -0.477171 | 0.620536    |             0 |
| M       | -1.22717  | 0.293121    |             0 |
| <       | -3.10217  | 0.0449515   |             0 |
| Germany | -4.60217  | 0.01003     |             0 |
| B       | -4.60217  | 0.01003     |             0 |
| Ber     | -5.10217  | 0.00608353  |             0 |
| Frank   | -6.10217  | 0.002238    |             0 |
| Bern    | -6.60217  | 0.00135742  |             0 |
| Vi      | -6.91467  | 0.000993108 |             0 |
| German  | -7.35217  | 0.000641199 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '  \n', '<|im_start|>', '<think>', '<|file_sep|>', ' -->', '.Category', '.', ';', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n   \n', '\\n', '<\\/', '｡', '  \n\n', ';</', '</', '-US', ' <--', '\t\n', '<<<<', ' **.**', '\\.', '<br', './.', '.;']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Berlin', 'EUR']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Munich, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', ' Bangkok', 'Madrid', ' Jakarta', 'Paris', ' Riyadh', 'London', ' Nairobi', ' Buenos', ' Brasília', ' Barcelona', 'Barcelona', ' Caracas', ' Mumbai', ' London', ' Bogotá', ' Lisbon', ' Prague', ' Ankara', ' Cairo', ' Paris', ' Tehran', ' Tokyo', 'Jakarta', ' Berlin', ' Lagos', 'city', ' Budapest', ' São', ' Mexico', ' Helsinki', ' Istanbul']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Mexico  | -0.114961 | 0.891401   |      10.7997  |
| M       | -3.48996  | 0.0305021  |      -2.26279 |
| Madrid  | -3.86496  | 0.0209637  |       5.29971 |
| <       | -4.48996  | 0.0112211  |      -1.38779 |
| Gu      | -5.11496  | 0.00600621 |       7.98721 |
| Mon     | -5.36496  | 0.00467764 |       3.23721 |
| Mé      | -5.61496  | 0.00364295 |       8.17471 |
| Se      | -5.80246  | 0.00302011 |       6.04971 |
| <span   | -6.11496  | 0.00220956 |       1.92471 |
| Mex     | -6.23996  | 0.00194993 |       8.61221 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '\\n', '**', ' Incorrect', '  \n', ';', '错误', ' incorrect', '错误的', '</tool_response>', 'incorrect', '\\', '<|im_start|>', '</', '错', '<think>', ' <--', '错的', '的错误', ' mistakenly', ' <<<', ' incorrectly', ' -->', ' Wrong', '.\\', ')', '\n', '是错误的', '  \n\n']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Brasília', 'BRL']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Munich, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Berlin', 'Berlin', ' Prague', 'Germany', ' Vienna', 'Paris', ' Frankfurt', 'London', ' Germany', ' München', ' Budapest', ' Madrid', '慕尼黑', 'Madrid', ' Austria', ' Helsinki', ' Amsterdam', ' Paris', ' Stuttgart', '维也纳', ' Zurich', ' London', ' Leipzig', ' Stockholm', 'Barcelona', ' berlin', ' Oslo', ' Bav', ' Lisbon', ' Bratis', '巴黎', ' Barcelona']

Generation (4 tokens):
```text
Berlin; EUR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Berlin  | -0.476607 | 0.620886    |   0.000563741 |
| M       | -1.22661  | 0.293286    |   0.00056386  |
| <       | -3.10161  | 0.0449769   |   0.00056386  |
| Germany | -4.60161  | 0.0100357   |   0.000563622 |
| B       | -4.60161  | 0.0100357   |   0.000563622 |
| Ber     | -5.10161  | 0.00608695  |   0.000563622 |
| Frank   | -6.10161  | 0.00223927  |   0.000563622 |
| Bern    | -6.53911  | 0.00144578  |   0.0630636   |
| Vi      | -7.03911  | 0.000876909 |  -0.124436    |
| German  | -7.35161  | 0.00064156  |   0.000563622 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '\t  \n', '<|im_start|>', '  \n', '<think>', '<|file_sep|>', ' -->', '.Category', '.', ';', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\n', '<\\/', '\n   \n', '｡', ';</', '</', '-US', '  \n\n', ' <--', '\t\n', '<<<<', ' **.**', '\\.', '<br', './.', '-Americ']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Brasília', 'BRL']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Munich, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Berlin', 'Berlin', 'Germany', ' Prague', ' Germany', ' Vienna', 'Paris', ' München', ' Frankfurt', ' Austria', ' Budapest', '慕尼黑', 'London', ' Madrid', 'Madrid', ' Stuttgart', ' Zurich', ' Helsinki', '维也纳', ' Paris', ' Bav', ' Leipzig', ' Amsterdam', ' London', ' berlin', ' Karlsruhe', 'Barcelona', ' Stockholm', ' Bratis', ' Hamburg', ' Luxembourg', ' Oslo']

Generation (4 tokens):
```text
Berlin; EUR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Berlin  | -0.608557 | 0.544135    |   -0.131386   |
| M       | -1.10856  | 0.330035    |    0.118614   |
| <       | -2.73356  | 0.0649877   |    0.368614   |
| Germany | -3.73356  | 0.0239076   |    0.868614   |
| B       | -4.48356  | 0.0112932   |    0.118614   |
| Ber     | -5.10856  | 0.0060448   |   -0.00638628 |
| Frank   | -5.98356  | 0.00251985  |    0.118614   |
| Bern    | -6.67106  | 0.00126706  |   -0.0688863  |
| German  | -6.85856  | 0.00105043  |    0.493614   |
| Vi      | -6.92106  | 0.000986786 |   -0.00638628 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '\t  \n', '  \n', '<|im_start|>', '<think>', '.', ' -->', '<|file_sep|>', '.Category', ';', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n   \n', '\\n', '｡', '<\\/', '  \n\n', ';</', '</', '-US', ' <--', ' **.**', '\t\n', '<<<<', '\\.', '.;', './.', '<br']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Berlin', 'EUR']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.
