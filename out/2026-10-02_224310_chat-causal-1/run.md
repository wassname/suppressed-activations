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
elapsed_seconds: 4.82
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Asia to Europe. Positive answer_log_odds_shift favours first token 'Asia' over 'Europe'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Asia toward Europe with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Asia') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|------------------:|--------------------:|------------------------:|-----:|
| Base                          |                  0      |       0.834732    |         0.00104041  |                0.835773 |    0 |
| raw J-coordinate exchange     |                -15.3125 |       0.000174556 |         0.97213     |                0.972304 |    0 |
| raw plain-coordinate exchange |                 -0.4375 |       0.815182    |         0.00157367  |                0.816756 |    0 |
| matched-random delta          |                  0.3125 |       0.804905    |         0.000733978 |                0.805639 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Mumbai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' asia', ' Africa', ' Oce', 'Africa', '亚洲', ' continents', ' Europe', 'India', 'Europe', 'asia', ' India', ' Americas', '大陆', ' Antarctica', ';', 'continental', '南亚', ';**', ' africa', '东南亚', '__;', ';;', ' Arabia', ' Countries', ' Euras', '东亚', ' ASEAN', ' europe', '；', '*;']

Generation (5 tokens):
```text
Asia; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Asia    | -0.180644 | 0.834732    |             0 |
| <       | -2.05564  | 0.12801     |             0 |
| Africa  | -4.55564  | 0.0105077   |             0 |
| Asia    | -4.93064  | 0.00722185  |             0 |
| ;       | -4.93064  | 0.00722185  |             0 |
| AS      | -5.80564  | 0.00301052  |             0 |
| Europe  | -6.86814  | 0.00104041  |             0 |
| >       | -7.18064  | 0.000761178 |             0 |
| As      | -7.43064  | 0.000592806 |             0 |
| Asian   | -7.43064  | 0.000592806 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '<think>', '.', '</', '<|file_sep|>', '.Category', ';', '  \n', '\\', '\t  \n', '<', '**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<\\/', '\\.', '*', '?', '\\n', '\\<', '\n', ' Disclaimer', '或未', ')', '\x00', ' -->', '!', '@\\', '\t\n']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'INR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Mumbai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Europe', 'Europe', 'Asia', ' Asia', ' continents', ' europe', 'Africa', ' Africa', ' Oce', ' Europa', '大陆', ' asia', ' France', '欧洲', 'continental', 'France', 'Europa', ' EURO', ' continental', ' Americas', ';', ' africa', '西欧', ';**', 'urope', ' Antarctica', '欧洲的', '__;', ' continente', ' Countries', ';;', '在欧洲']

Generation (4 tokens):
```text
Europe; EUR<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Europe   | -0.0282658 | 0.97213     |       6.83988 |
| <        | -4.15327   | 0.015713    |      -2.09762 |
| E        | -5.90327   | 0.00273051  |       5.33988 |
| Europe   | -6.27827   | 0.00187665  |       5.33988 |
| Africa   | -6.52827   | 0.00146154  |      -1.97262 |
| ;        | -7.15327   | 0.000782305 |      -2.22262 |
| EU       | -7.27827   | 0.000690382 |       6.21488 |
| Europa   | -7.27827   | 0.000690382 |       4.71488 |
| European | -7.27827   | 0.000690382 |       6.33988 |
| <E       | -7.52827   | 0.00053767  |       3.15238 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', ' Incorrect', ' incorrect', '</think>', '是错误的', ' Wrong', ' -->', ' <--', ' incorrectly', '错误', ' FALSE', 'incorrect', '的错误', ' WRONG', '  \n', 'Incorrect', '错误的', '\\n', '错', '**', '.', '错的', ' �', ' mistakenly', ' ERROR', ' wrong', '  \n\n', '不正确', ' *(', '***', ';']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Mumbai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' asia', ' Africa', ' Oce', 'Africa', ' continents', '亚洲', ' Europe', 'Europe', 'asia', 'India', ' Americas', '大陆', ' Antarctica', ';', 'continental', ' India', ';**', ' africa', '南亚', '__;', '东南亚', ';;', ' Arabia', ' Countries', ' europe', '；', ' Euras', ' ASEAN', '*;', '东亚']

Generation (5 tokens):
```text
Asia; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Asia    | -0.204344 | 0.815182    |       -0.0237 |
| <       | -1.95434  | 0.141657    |        0.1013 |
| Africa  | -4.20434  | 0.0149306   |        0.3513 |
| ;       | -4.70434  | 0.00905585  |        0.2263 |
| Asia    | -5.32934  | 0.00484725  |       -0.3987 |
| AS      | -5.70434  | 0.00333146  |        0.1013 |
| Europe  | -6.45434  | 0.00157367  |        0.4138 |
| >       | -6.89184  | 0.00101604  |        0.2888 |
| Asian   | -7.26684  | 0.000698313 |        0.1638 |
| As      | -7.32934  | 0.000656004 |        0.1013 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '<think>', '.', '</', '<|file_sep|>', ';', '.Category', '  \n', '\\', '\t  \n', '<', '**', '*', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<\\/', '\\.', '?', '\\n', '\\<', '\n', ' Disclaimer', ')', '\x00', ' -->', '@\\', '/OR', '!', '\t\n']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Europe', 'EUR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Mumbai on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Asia', 'Asia', ' asia', ' Africa', '亚洲', ' Oce', ' continents', 'Africa', 'India', ' Europe', ' India', 'Europe', 'asia', ' Americas', ' Antarctica', ';', '大陆', '南亚', 'continental', ';**', ' africa', ';;', '东南亚', ' Countries', '__;', ' Arabia', '东亚', ' Australia', ' ASEAN', '；', ' Euras', ' europe']

Generation (5 tokens):
```text
Asia; INR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Asia    | -0.217031 | 0.804905    |     -0.036387 |
| <       | -1.84203  | 0.158495    |      0.213613 |
| Asia    | -4.59203  | 0.0101323   |      0.338613 |
| Africa  | -4.96703  | 0.00696379  |     -0.411387 |
| ;       | -4.96703  | 0.00696379  |     -0.036387 |
| AS      | -5.96703  | 0.00256184  |     -0.161387 |
| >       | -6.71703  | 0.00121013  |      0.463613 |
| Europe  | -7.21703  | 0.000733978 |     -0.348887 |
| As      | -7.27953  | 0.000689509 |      0.151113 |
| India   | -7.40453  | 0.000608489 |      0.213613 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '.', '<think>', '</', '<|file_sep|>', ';', '.Category', '  \n', '\\', '\t  \n', '<', '**', '\\.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '*', '<\\/', '?', '\\n', '\\<', '\n', ')', '\x00', ' Disclaimer', '或未', '!', '@\\', '\t\n', ' -->']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'INR']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.
