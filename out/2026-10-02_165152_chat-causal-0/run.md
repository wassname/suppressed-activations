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
elapsed_seconds: 7.98
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Paris to New Delhi. Positive answer_log_odds_shift favours first token 'New' over 'Paris'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Paris toward New Delhi with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='New') |   p(first='Paris') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |             4.39584e-07 |      6.0525e-07  |         0.934611   |                0.934612 |    0 |
| raw J-coordinate exchange     |            25.625       |      0.835333    |         9.5887e-06 |                0.835342 |    0 |
| raw plain-coordinate exchange |             0.3125      |      8.11956e-07 |         0.9173     |                0.917301 |    0 |
| matched-random delta          |             0.625       |      1.08644e-06 |         0.897979   |                0.897981 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Lyon, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Paris', ' Paris', '巴黎', ' PARIS', 'France', ' Marseille', ' France', 'Madrid', ' Madrid', 'London', ' París', ' Toulouse', '法国', 'Barcelona', ' paris', ' Prague', ' Strasbourg', 'Berlin', ' Berlin', ' FRANCE', ' Пари', ' Barcelona', ' Versailles', 'city', ' Brussels', ' Londres', ' Grenoble', ' Luxembourg', ' Amsterdam', ' London', ' Vienna', ' Munich']

Generation (4 tokens):
```text
Paris; EUR<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Paris   | -0.0676246 | 0.934611    |             0 |
| <       | -3.31762   | 0.0362388   |             0 |
| France  | -4.31762   | 0.0133315   |             0 |
| L       | -5.06762   | 0.00629736  |             0 |
| Frank   | -6.44262   | 0.00159222  |             0 |
| French  | -6.44262   | 0.00159222  |             0 |
| Par     | -6.69262   | 0.00124002  |             0 |
| ;       | -7.06762   | 0.000852255 |             0 |
| Br      | -7.75512   | 0.000428541 |             0 |
| F       | -8.75513   | 0.000157651 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '  \n', '<|im_start|>', '<think>', '<|file_sep|>', '.', ' -->', '.Category', ';', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n   \n', '\\n', '  \n\n', '\t\n', '</', '<\\/', '｡', ';</', '<<<<', '-US', '<br', ' **.**', '\n  \n', '.;', ' <--', '\\.']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Paris', 'EUR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Lyon, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Mumbai', ' Bangkok', 'London', ' Nairobi', ' Jakarta', ' Hyderabad', ' Kolkata', ' Delhi', ' Riyadh', ' Islamabad', ' London', 'Paris', 'Jakarta', 'city', ' Karachi', ' Ankara', ' Bangalore', ' Cairo', ' Tehran', ' Madrid', ' Baghdad', ' Bogotá', 'India', ' Chennai', ' Johannesburg', ' Dubai', ' Bombay', 'Madrid', ' Maharashtra', ' Caracas', ' Tokyo', ' Pune']

Generation (6 tokens):
```text
New Delhi; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| New     | -0.179925 | 0.835333    |     14.1377   |
| <       | -2.42993  | 0.0880434   |      0.887699 |
| Del     | -3.30493  | 0.036702    |     12.7627   |
| India   | -4.30492  | 0.0135019   |     13.0752   |
| M       | -4.55492  | 0.0105153   |      5.8877   |
| <p      | -6.05492  | 0.00234628  |      3.3877   |
| D       | -6.30492  | 0.00182728  |      5.7627   |
| Bang    | -6.74242  | 0.00117978  |      6.8877   |
| new     | -6.99242  | 0.000918816 |      9.4502   |
| Ind     | -7.11742  | 0.000810852 |     11.919    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ' incorrect', ' Incorrect', 'incorrect', '错误', ';', '错误的', '<|im_start|>', '</tool_response>', '<think>', '</', '  \n', ' Wrong', '**', 'Incorrect', '错', '错的', ' incorrectly', ' mistakenly', '不正确', '的错误', '\\n', '是错误的', '<', '\t  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' -->', 'Wrong', '\\']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['New Delhi', 'INR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Lyon, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Paris', ' Paris', '巴黎', ' PARIS', 'France', ' Marseille', ' France', 'Madrid', ' Madrid', ' París', 'London', ' Toulouse', '法国', 'Barcelona', ' Prague', ' paris', ' Strasbourg', 'Berlin', ' Berlin', ' Пари', ' FRANCE', ' Barcelona', ' Versailles', 'city', ' Brussels', ' Londres', ' Grenoble', ' Luxembourg', ' Amsterdam', ' London', ' Vienna', ' Munich']

Generation (4 tokens):
```text
Paris; EUR<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Paris   | -0.0863202 | 0.9173      |    -0.0186956 |
| <       | -3.08632   | 0.0456697   |     0.231304  |
| France  | -4.08632   | 0.0168009   |     0.231304  |
| L       | -4.71132   | 0.0089929   |     0.356304  |
| Frank   | -6.33632   | 0.00177081  |     0.106304  |
| French  | -6.33632   | 0.00177081  |     0.106304  |
| Par     | -6.58632   | 0.00137911  |     0.106304  |
| ;       | -6.83632   | 0.00107405  |     0.231304  |
| Br      | -7.52382   | 0.000540065 |     0.231304  |
| <br     | -8.52382   | 0.000198679 |     0.231305  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '  \n', '<|im_start|>', '<think>', '<|file_sep|>', ' -->', '.', '.Category', ';', ' <<<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\n', '\n   \n', '\t\n', '  \n\n', '</', '<\\/', '｡', ';</', '<<<<', '<br', '-US', ' **.**', ' <--', '\\.', '\n  \n', '.;']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['New Delhi', 'INR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Lyon, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Paris', ' Paris', '巴黎', ' PARIS', 'France', ' France', ' Marseille', 'Madrid', '法国', ' París', ' Madrid', 'London', ' Toulouse', ' FRANCE', ' paris', ' Strasbourg', 'Barcelona', ' Prague', 'city', ' Пари', ' Berlin', ' Versailles', 'Berlin', ' Barcelona', ' france', ' Grenoble', ' Luxembourg', ' Brussels', 'French', ' Londres', ' Amsterdam', ' London']

Generation (4 tokens):
```text
Paris; EUR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Paris   | -0.107608 | 0.897979    |    -0.0399835 |
| <       | -2.85761  | 0.0574059   |     0.460016  |
| France  | -3.73261  | 0.0239303   |     0.585016  |
| L       | -4.85761  | 0.00776904  |     0.210016  |
| Frank   | -6.10761  | 0.00222587  |     0.335016  |
| French  | -6.23261  | 0.00196432  |     0.210016  |
| Par     | -6.60761  | 0.00135006  |     0.0850163 |
| ;       | -6.60761  | 0.00135006  |     0.460016  |
| Br      | -7.60761  | 0.000496658 |     0.147516  |
| <span   | -8.23261  | 0.000265842 |     0.522517  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '\t  \n', '</tool_response>', '  \n', '<|im_start|>', '<think>', '.', '<|file_sep|>', ' -->', '.Category', ';', ' <<<', '.<', '\n   \n', '\\n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n\n', '</', '\t\n', ';</', '<\\/', '｡', '<<<<', ' **.**', '<br', '-US', '\n  \n', ' <--', '.;', '\\.']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Paris', 'EUR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.
