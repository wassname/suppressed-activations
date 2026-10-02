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
elapsed_seconds: 12.58
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Ottawa to Canberra. Positive answer_log_odds_shift favours first token 'Can' over 'O'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Ottawa toward Canberra with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Can') |   p(first='O') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|---------------:|------------------------:|-----:|
| Base                          |            -1.32248e-07 |      4.15152e-05 |      0.97341   |                0.973451 |    0 |
| raw J-coordinate exchange     |            13.5625      |      0.444097    |      0.0134106 |                0.457508 |    0 |
| raw plain-coordinate exchange |             0.0624999   |      4.41667e-05 |      0.972835  |                0.97288  |    0 |
| matched-random delta          |             0.4375      |      6.34781e-05 |      0.960967  |                0.96103  |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Toronto, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Ottawa', 'Canada', ' Montreal', 'London', ' Montréal', ' Canada', ' Winnipeg', ' London', ' Vancouver', ' Ontario', '多伦多', ' Calgary', 'Paris', ' canada', 'Canadian', ' Edmonton', 'ancouver', ' Canadá', ' Quebec', ' Québec', '伦敦', ' Bogotá', 'city', '北京', ' Canberra', '首都', ' Londres', ' london', ' Westminster', ' Dublin', ' لندن', '石家庄']

Generation (6 tokens):
```text
Ottawa; CAD<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| O       | -0.02695 | 0.97341     |             0 |
| <       | -4.02695 | 0.0178286   |             0 |
| Toronto | -6.02695 | 0.00241284  |             0 |
| Ont     | -6.40195 | 0.00165832  |             0 |
| Canada  | -6.77695 | 0.00113975  |             0 |
| >O      | -7.83945 | 0.000393886 |             0 |
| <span   | -8.15195 | 0.000288173 |             0 |
| Ot      | -8.15195 | 0.000288173 |             0 |
| <p      | -8.46445 | 0.000210832 |             0 |
| Mont    | -8.65195 | 0.000174786 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '<|im_start|>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', '.Category', '<br', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', '\t  \n', ' -->', ';<', '"<', '。<', '<', '.', '\t\n', '<<<<', '="<', '\r\r\n', '\\n', '｡', '  \n', '/C', ')<', '\\<', '.--', ';']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Ottawa', 'CAD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Toronto, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['London', ' London', ' Canberra', ' Melbourne', '伦敦', ' Jakarta', ' Londres', ' Sydney', ' Nairobi', ' Dublin', ' london', ' Auckland', ' Londra', 'Paris', ' لندن', ' Johannesburg', ' Bangkok', '悉尼', 'Jakarta', '首都', ' Westminster', 'city', ' Tokyo', 'uckland', ' Madrid', ' Islamabad', ' Riyadh', ' Brisbane', '北京', ' Bogotá', ' Amsterdam', ' Brasília']

Generation (5 tokens):
```text
Canberra; AUD<|im_end|>
```

| token      |     log p |          p |   delta log p |
|:-----------|----------:|-----------:|--------------:|
| Can        | -0.811712 | 0.444097   |       9.27774 |
| <          | -1.31171  | 0.269359   |       2.71524 |
| Sy         | -1.93671  | 0.144177   |      12.1527  |
| Australia  | -3.68671  | 0.0250542  |      10.2777  |
| A          | -4.18671  | 0.0151962  |       8.21524 |
| Australian | -4.18671  | 0.0151962  |      12.3402  |
| O          | -4.31171  | 0.0134106  |      -4.28476 |
| Well       | -4.43671  | 0.0118348  |       7.59024 |
| Canberra   | -4.99921  | 0.00674326 |      11.4652  |
| Canada     | -5.06171  | 0.0063347  |       1.71524 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<|file_sep|>', '\t  \n', '.', '</tool_response>', '<think>', '.Category', '\t\n', '  \n', '<\\/', '</', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';', '.<', ' -->', '\\n', '<<<<', ' <<<', ' \n', '/A', '<br', '-Americ', '/AP', '<', '\\.', ' \n\n', ' <--', '/UI', '/.']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Canberra', 'AUD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Toronto, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Ottawa', 'Canada', 'London', ' Montreal', ' Montréal', ' Canada', ' London', ' Winnipeg', ' Vancouver', ' Ontario', '多伦多', ' Calgary', 'Paris', 'ancouver', ' canada', ' Edmonton', '伦敦', 'Canadian', ' Canadá', 'city', ' Quebec', '北京', ' Londres', ' Canberra', '首都', ' Québec', ' Bogotá', ' london', ' Westminster', ' Dublin', ' لندن', ' Sydney']

Generation (6 tokens):
```text
Ottawa; CAD<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| O       | -0.0275402 | 0.972835    |  -0.000590235 |
| <       | -4.02754   | 0.0178181   |  -0.000590324 |
| Toronto | -5.90254   | 0.00273249  |   0.12441     |
| Ont     | -6.27754   | 0.00187801  |   0.12441     |
| Canada  | -6.77754   | 0.00113907  |  -0.000590324 |
| >O      | -7.77754   | 0.000419042 |   0.0619097   |
| Ot      | -8.09004   | 0.000306577 |   0.0619097   |
| <span   | -8.21504   | 0.000270554 |  -0.0630903   |
| <p      | -8.46504   | 0.000210707 |  -0.000590324 |
| Mont    | -8.71504   | 0.000164099 |  -0.0630903   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '<|im_start|>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', '.Category', '<br', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', '\t  \n', ' -->', ';<', '.', '"<', '\t\n', '\r\r\n', '。<', '<', '/C', '  \n', '\\n', '<<<<', '｡', '="<', ';', '\\<', '\\C', '\x00']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Canberra', 'AUD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Toronto, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Canada', ' Ottawa', ' Montreal', ' Canada', 'London', ' Montréal', ' Winnipeg', ' Ontario', ' Vancouver', ' London', '多伦多', ' Calgary', ' canada', 'Canadian', ' Canadá', ' Quebec', ' Edmonton', 'Paris', 'ancouver', ' Québec', 'city', '首都', ' Bogotá', '伦敦', ' Canberra', '北京', ' Kanada', ' Londres', ' Canadian', ' canadian', ' london', ' Westminster']

Generation (6 tokens):
```text
Ottawa; CAD<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| O       | -0.0398157 | 0.960967    |    -0.0128657 |
| <       | -3.66482   | 0.0256089   |     0.362134  |
| Toronto | -5.41482   | 0.00445016  |     0.612134  |
| Ont     | -6.03982   | 0.002382    |     0.362134  |
| Canada  | -6.28982   | 0.0018551   |     0.487134  |
| >O      | -7.66482   | 0.000469043 |     0.174634  |
| <span   | -7.85232   | 0.00038885  |     0.299634  |
| Ot      | -8.03982   | 0.000322368 |     0.112134  |
| <p      | -8.22732   | 0.000267253 |     0.237134  |
| Mont    | -8.35232   | 0.00023585  |     0.299634  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '.<', '<|file_sep|>', '<|im_start|>', '</tool_response>', '<\\/', '.Category', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', ',<', '\t  \n', '.', ' -->', ';<', '"<', '\t\n', '。<', '  \n', '<', ';', '\r\r\n', '="<', '.--', '<<<<', '/C', '｡', '\\<', '\x00', '\\n']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Ottawa', 'CAD']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.
