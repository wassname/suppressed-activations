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
elapsed_seconds: 4.90
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Mexico City to Madrid. Positive answer_log_odds_shift favours first token 'Mexico' over 'Madrid'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Mexico City toward Madrid with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Mexico') |   p(first='Madrid') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|--------------------:|------------------------:|-----:|
| Base                          |                  0      |            0.893307 |         0.000867127 |                0.894174 |    0 |
| raw J-coordinate exchange     |                 -5.1875 |            0.768455 |         0.133537    |                0.901993 |    0 |
| raw plain-coordinate exchange |                  0.1875 |            0.912031 |         0.000733942 |                0.912765 |    0 |
| matched-random delta          |                 -0.125  |            0.886761 |         0.000975384 |                0.887736 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Guadalajara, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', ' Bogotá', 'Madrid', ' Caracas', ' Brasília', ' Buenos', ' Ciudad', ' Mexico', 'Mexico', ' Jakarta', ' Barcelona', ' Ankara', 'Paris', 'Barcelona', ' México', ' Riyadh', 'city', ' mexico', ' Bangkok', ' Havana', ' madrid', ' Lisbon', ' Lagos', ' Guatemala', ' Paris', 'Jakarta', '墨西哥', '马德里', ' São', ' Prague', ' Nairobi', ' Albuquerque']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Mexico  | -0.112825 | 0.893307   |             0 |
| <       | -3.23782  | 0.0392492  |             0 |
| Gu      | -3.61282  | 0.0269755  |             0 |
| Mé      | -4.61282  | 0.00992374 |             0 |
| Mex     | -5.23782  | 0.0053118  |             0 |
| <p      | -6.11282  | 0.00221429 |             0 |
| Ci      | -6.23782  | 0.0019541  |             0 |
| Mon     | -6.48782  | 0.00152186 |             0 |
| <span   | -6.55032  | 0.00142965 |             0 |
| ;       | -6.61282  | 0.00134303 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</tool_response>', '<|im_start|>', '</', '**', '\\', '\\n', '<|file_sep|>', '.Category', '<', '<\\/', '\\.', '  \n', '-Americ', '@\\', ',<', '\t  \n', '<<<<', ')', ';<', '-US', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<', '\\<', '\\:', ' <<<', '.<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Mexico City', 'MXN']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Guadalajara, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', 'Madrid', ' Bogotá', ' Barcelona', ' Caracas', 'Paris', 'Barcelona', ' Buenos', ' Ciudad', ' Brasília', ' Ankara', ' Jakarta', ' Lisbon', ' Paris', ' madrid', '马德里', 'Mexico', ' Mexico', ' Prague', ' Riyadh', ' Istanbul', ' Berlin', 'London', 'city', 'Jakarta', ' Bangkok', ' Bilbao', 'Berlin', ' Budapest', 'Spain', '太原', ' Warsaw']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Mexico  | -0.263373 | 0.768455   |    -0.150548  |
| Madrid  | -2.01337  | 0.133537   |     5.03695   |
| <       | -3.38837  | 0.0337636  |    -0.150548  |
| Gu      | -4.01337  | 0.0180723  |    -0.400548  |
| Mé      | -4.63837  | 0.00967342 |    -0.0255485 |
| <span   | -5.13837  | 0.00586723 |     1.41195   |
| Mex     | -5.51337  | 0.00403248 |    -0.275548  |
| Spain   | -5.76337  | 0.0031405  |     4.66195   |
| ;       | -6.20087  | 0.00202766 |     0.411952  |
| M       | -6.70087  | 0.00122984 |     0.349452  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '<|im_start|>', '</tool_response>', '</', '**', '\\', '\\n', '<|file_sep|>', '.Category', '<\\/', '<', '@\\', '  \n', '\\.', '-Americ', ',<', '\t  \n', ';<', ')', '<<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<', '\\<', '-US', ' <<<', '\\:', '.<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Madrid', 'EUR']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Guadalajara, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', ' Bogotá', 'Madrid', ' Caracas', ' Brasília', ' Ciudad', ' Buenos', ' Mexico', 'Mexico', ' Jakarta', ' Ankara', 'Paris', ' Barcelona', 'Barcelona', ' México', 'city', ' Riyadh', ' mexico', ' Bangkok', ' madrid', ' Havana', ' Lisbon', ' Lagos', 'Jakarta', ' Paris', ' Guatemala', '墨西哥', '马德里', ' São', ' Albuquerque', ' Москва', ' Prague']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |      log p |          p |   delta log p |
|:--------|-----------:|-----------:|--------------:|
| Mexico  | -0.0920809 | 0.912031   |     0.0207441 |
| <       | -3.46708   | 0.031208   |    -0.229256  |
| Gu      | -3.84208   | 0.0214489  |    -0.229256  |
| Mé      | -4.71708   | 0.00894124 |    -0.104256  |
| Mex     | -5.34208   | 0.0047859  |    -0.104256  |
| <p      | -6.27958   | 0.00187419 |    -0.166756  |
| Ci      | -6.34208   | 0.00176063 |    -0.104256  |
| Mon     | -6.77958   | 0.00113675 |    -0.291756  |
| ;       | -6.77958   | 0.00113675 |    -0.166756  |
| <span   | -6.84208   | 0.00106788 |    -0.291756  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '<|im_start|>', '</tool_response>', '</', '**', '\\', '\\n', '<|file_sep|>', '.Category', '<', '<\\/', '  \n', '-Americ', '\\.', '@\\', '\t  \n', ',<', '<<<<', ')', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';<', '<<<', '-US', ' <<<', '\\<', '\\:', '.<']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Madrid', 'EUR']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Guadalajara, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Madrid', ' Bogotá', 'Madrid', ' Caracas', ' Brasília', ' Buenos', ' Mexico', ' Ciudad', 'Mexico', ' Jakarta', ' Ankara', ' Barcelona', 'Paris', ' México', 'Barcelona', 'city', ' Riyadh', ' mexico', ' Bangkok', ' madrid', ' Havana', ' Lagos', ' Guatemala', ' Paris', ' Lisbon', '墨西哥', 'Jakarta', ' São', '马德里', ' Albuquerque', ' Nairobi', ' Istanbul']

Generation (6 tokens):
```text
Mexico City; MXN<|im_end|>
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| Mexico  | -0.12018 | 0.886761   |    -0.0073547 |
| Gu      | -3.37018 | 0.0343835  |     0.242645  |
| <       | -3.37018 | 0.0343835  |    -0.132355  |
| Mé      | -4.49518 | 0.0111627  |     0.117645  |
| Mex     | -5.12018 | 0.00597495 |     0.117645  |
| Mon     | -6.18268 | 0.00206489 |     0.305145  |
| Ci      | -6.18268 | 0.00206489 |     0.0551453 |
| <p      | -6.24518 | 0.00193978 |    -0.132355  |
| ;       | -6.43268 | 0.00160814 |     0.180145  |
| <span   | -6.68268 | 0.00125242 |    -0.132355  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '<|im_start|>', '</tool_response>', '</', '**', '\\', '\\n', '<|file_sep|>', '.Category', '<', '<\\/', '\\.', '  \n', '-Americ', '@\\', '\t  \n', ',<', ')', ';<', '\\:', '<<<<', '<<<', '-US', '\\<', ' <<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';**']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Mexico City', 'MXN']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.
