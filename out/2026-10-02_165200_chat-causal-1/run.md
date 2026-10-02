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
elapsed_seconds: 5.17
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is New Delhi to Paris. Positive answer_log_odds_shift favours first token 'New' over 'Paris'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes New Delhi toward Paris with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='New') |   p(first='Paris') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |                  0      |      0.882671    |        3.72739e-06 |                0.882675 |    0 |
| raw J-coordinate exchange     |                -26.4375 |      7.72159e-07 |        0.988491    |                0.988492 |    0 |
| raw plain-coordinate exchange |                 -0.125  |      0.874021    |        4.18229e-06 |                0.874025 |    0 |
| matched-random delta          |                 -0.125  |      0.862379    |        4.12658e-06 |                0.862383 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Mumbai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Jakarta', 'London', ' Kolkata', ' Delhi', ' Bangkok', ' Hyderabad', ' Nairobi', 'Jakarta', ' London', ' Riyadh', ' Islamabad', ' Tehran', ' Karachi', ' Chennai', ' Tokyo', ' Bombay', ' Maharashtra', 'Paris', 'city', ' Bangalore', ' Madrid', ' Ankara', ' Lagos', ' Beijing', ' Londres', '伦敦', ' london', ' Pune', ' Brasília', ' Johannesburg', ' Dubai', ' Cairo']

Generation (6 tokens):
```text
New Delhi; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| New     | -0.124803 | 0.882671    |             0 |
| <       | -2.6248   | 0.0724541   |             0 |
| Del     | -3.8748   | 0.0207584   |             0 |
| M       | -4.6248   | 0.00980559  |             0 |
| India   | -5.1248   | 0.00594739  |             0 |
| D       | -7.1873   | 0.000756126 |             0 |
| <p      | -7.3748   | 0.00062685  |             0 |
| Ne      | -7.4998   | 0.000553194 |             0 |
| ;       | -7.6873   | 0.000458614 |             0 |
| <M      | -7.6873   | 0.000458614 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<|im_start|>', '</tool_response>', '<think>', '</', '<', ';', '<|file_sep|>', '.Category', '  \n', '**', '\\', '<\\/', '\t  \n', '\\.', '\\<', '.<', ',<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '"<', '\\n', '>', ';<', '/N', "'<", '<br', '<<<<', '="<', ')']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['New Delhi', 'INR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Mumbai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Paris', ' Paris', '巴黎', 'London', ' Madrid', ' PARIS', 'Madrid', ' London', ' Lisbon', ' Londres', ' Berlin', ' Jakarta', ' Barcelona', 'Barcelona', ' Amsterdam', ' Prague', ' Tehran', ' Dublin', '伦敦', ' Ankara', ' París', 'Berlin', ' Budapest', ' Istanbul', ' Riyadh', ' Marseille', ' Bangkok', ' Nairobi', ' Oslo', 'city', 'Jakarta', ' Helsinki']

Generation (4 tokens):
```text
Paris; EUR<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| Paris   | -0.0115759 | 0.988491    |      12.4882  |
| <       | -5.01158   | 0.0066604   |      -2.38677 |
| France  | -6.63658   | 0.00131151  |       8.80073 |
| Par     | -6.88658   | 0.00102141  |       9.05073 |
| French  | -8.44908   | 0.000214098 |       8.51948 |
| Paris   | -8.51158   | 0.000201127 |      11.9726  |
| M       | -8.63658   | 0.000177494 |      -4.01177 |
| ;       | -8.76158   | 0.000156638 |      -1.07427 |
| Frank   | -8.88658   | 0.000138232 |       6.48823 |
| Madrid  | -8.88658   | 0.000138232 |       4.92573 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ' incorrect', ' Incorrect', 'incorrect', '  \n', ' -->', 'Incorrect', '\t  \n', '错误', '</tool_response>', ' incorrectly', ' Wrong', '错误的', '是错误的', ' mistakenly', '的错误', '<|im_start|>', '不正确', '错的', ' mistake', ' <--', ' FALSE', '.', '<think>', ';', '错', 'Wrong', '\\n', ' <<<', '  \n\n']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Paris', 'EUR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Mumbai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Jakarta', 'London', ' Kolkata', ' Delhi', ' Bangkok', ' London', ' Hyderabad', 'Jakarta', ' Nairobi', ' Riyadh', ' Islamabad', ' Tehran', ' Karachi', ' Tokyo', ' Chennai', 'Paris', ' Bombay', ' Madrid', ' Maharashtra', 'city', ' Bangalore', ' Ankara', ' Lagos', ' Beijing', ' Londres', '伦敦', ' Cairo', ' Dubai', ' Johannesburg', 'Madrid', ' Brasília', ' london']

Generation (6 tokens):
```text
New Delhi; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| New     | -0.134651 | 0.874021    |   -0.00984858 |
| <       | -2.63465  | 0.071744    |   -0.00984859 |
| Del     | -3.63465  | 0.0263931   |    0.240151   |
| M       | -4.25965  | 0.0141272   |    0.365151   |
| India   | -5.38465  | 0.00458644  |   -0.259849   |
| D       | -6.94715  | 0.00096137  |    0.240151   |
| <p      | -7.25965  | 0.000703353 |    0.115151   |
| <M      | -7.38465  | 0.000620707 |    0.302651   |
| Ne      | -7.44715  | 0.0005831   |    0.0526514  |
| ;       | -7.50965  | 0.000547772 |    0.177651   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<|im_start|>', '</tool_response>', '<think>', '</', '<', ';', '<|file_sep|>', '.Category', '**', '  \n', '\\', '<\\/', '\t  \n', '\\.', '\\<', ',<', '.<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '"<', '\\n', '>', ';<', "'<", '/N', '<br', '<<<<', '="<', ')']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Paris', 'EUR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Mumbai, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Jakarta', ' Kolkata', ' Delhi', 'London', ' Hyderabad', ' Bangkok', 'Jakarta', ' Nairobi', ' London', ' Islamabad', ' Riyadh', ' Tehran', ' Maharashtra', ' Chennai', ' Bombay', ' Karachi', ' Tokyo', ' Bangalore', 'Paris', 'city', ' Madrid', ' Ankara', ' Pune', ' Beijing', ' Lagos', 'India', ' Londres', ' Cairo', ' Brasília', ' london', '伦敦', ' Johannesburg']

Generation (6 tokens):
```text
New Delhi; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| New     | -0.148061 | 0.862379    |    -0.0232582 |
| <       | -2.39806  | 0.090894    |     0.226742  |
| Del     | -3.89806  | 0.0202812   |    -0.0232584 |
| M       | -4.52306  | 0.0108557   |     0.101742  |
| India   | -5.02306  | 0.00658434  |     0.101742  |
| <p      | -7.14806  | 0.000786388 |     0.226742  |
| D       | -7.33556  | 0.000651938 |    -0.148258  |
| <M      | -7.39806  | 0.000612439 |     0.289242  |
| Ne      | -7.58556  | 0.00050773  |    -0.0857582 |
| ;       | -7.64806  | 0.000476968 |     0.0392418 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<|im_start|>', '</tool_response>', '<think>', '</', '<', ';', '<|file_sep|>', '.Category', '  \n', '\t  \n', '\\', '**', '\\.', '<\\/', '\\<', '.<', ',<', '"<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>', '\\n', ';<', "'<", '/N', '="<', '<br', '<<<<', ')']

Coverage: 6 calls; prompt slice 0:, then one position per decode.

Expected properties: ['New Delhi', 'INR']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.
