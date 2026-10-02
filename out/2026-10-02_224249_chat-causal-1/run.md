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
elapsed_seconds: 4.97
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Africa to Asia. Positive answer_log_odds_shift favours first token 'Africa' over 'Asia'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Africa toward Asia with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Africa') |   p(first='Asia') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|------------------:|------------------------:|-----:|
| Base                          |                  0      |           0.761192  |        0.00156422 |                0.762756 |    0 |
| raw J-coordinate exchange     |                 -9.0625 |           0.0409397 |        0.725673   |                0.766612 |    0 |
| raw plain-coordinate exchange |                 -0.1875 |           0.741363  |        0.00183766 |                0.743201 |    0 |
| matched-random delta          |                 -0.25   |           0.735608  |        0.00194099 |                0.737549 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Alexandria on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Africa', 'Africa', 'Asia', ' Europe', 'Europe', ' continents', ' Egypt', ' Asia', '大陆', ' africa', '埃及', 'Egypt', ' Oce', ' Americas', ' Antarctica', ' Greece', ' continental', 'continental', ' Europa', ' continente', ' europe', ';**', ' Arabia', ';', 'Europa', ' asia', ' Caribbean', ' Romania', '非洲', ' Tunisia', ' Libya', 'frica']

Generation (5 tokens):
```text
Africa; EGP<|im_end|>
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| Africa  | -0.27287 | 0.761192   |             0 |
| Europe  | -2.27287 | 0.103016   |             0 |
| <       | -2.64787 | 0.0708018  |             0 |
| ;       | -4.14787 | 0.015798   |             0 |
| Africa  | -4.64787 | 0.00958199 |             0 |
| A       | -4.77287 | 0.00845608 |             0 |
| Af      | -5.39787 | 0.00452621 |             0 |
| <a      | -5.52287 | 0.00399437 |             0 |
| AF      | -5.89787 | 0.00274529 |             0 |
| <A      | -6.14787 | 0.00213803 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '<think>', '.', '  \n', '<|file_sep|>', '.Category', '\\', '。', ' -->', ' **.**', '\t  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\n', '**', '</', ';', '\t\n', '.ht', '/AFP', '\n  \n', '.<', '<', '\n   \n', '$\\', '/E', '.\\', '  \n\n', '\\E']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Africa', 'EGP']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Alexandria on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: ['Asia', ' Asia', ' continents', ' Europe', ' Oce', ' Africa', ' asia', 'Europe', '大陆', 'Africa', ' Antarctica', ' Americas', '亚洲', 'China', 'continental', ' continental', 'asia', ' China', '-China', ' europe', ' continente', ' Europa', ' Countries', ' Euras', '东亚', ';', '；', ' Greece', ' africa', ';**', '__;', 'Europa']

Generation (5 tokens):
```text
Asia; CNY<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Asia    | -0.320656 | 0.725673   |     6.13971   |
| <       | -1.94566  | 0.142893   |     0.702214  |
| Africa  | -3.19566  | 0.0409397  |    -2.92279   |
| Europe  | -3.32066  | 0.0361291  |    -1.04779   |
| ;       | -4.19566  | 0.0150609  |    -0.0477858 |
| Asia    | -5.19566  | 0.00554058 |     6.76471   |
| North   | -5.57066  | 0.00380798 |     0.702214  |
| >       | -5.69566  | 0.00336053 |     1.51471   |
| AS      | -5.69566  | 0.00336053 |     6.26471   |
| A       | -5.94566  | 0.00261719 |    -1.17279   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '<|im_start|>', '</tool_response>', '</', '.', '**', '  \n', ' Incorrect', ' incorrect', 'incorrect', '<|file_sep|>', '\\', '错误', '\\n', '.Category', '错误的', '*', '\t  \n', '?', ';', ' Note', '注', ' Wait', '  \n\n', 'wait', 'Incorrect', '错', '<', 'Note']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'CNY']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Alexandria on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Africa', 'Africa', 'Asia', ' Europe', 'Europe', ' continents', ' Asia', ' Egypt', '大陆', ' africa', '埃及', ' Oce', ' Americas', 'Egypt', ' Antarctica', ' Greece', ' continental', 'continental', ' Europa', ' europe', ' continente', ';**', ' Arabia', ';', 'Europa', ' asia', ' Romania', ' Caribbean', '非洲', ' Tunisia', '大陆的', ' Countries']

Generation (5 tokens):
```text
Africa; EGP<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Africa  | -0.299265 | 0.741363   |    -0.0263949 |
| Europe  | -2.17427  | 0.113692   |     0.0986052 |
| <       | -2.54927  | 0.0781391  |     0.0986052 |
| ;       | -4.17426  | 0.0153865  |    -0.0263948 |
| Africa  | -4.67426  | 0.00933238 |    -0.0263948 |
| A       | -4.79926  | 0.0082358  |    -0.0263948 |
| Af      | -5.29926  | 0.00499526 |     0.0986052 |
| <a      | -5.54926  | 0.00389032 |    -0.0263948 |
| AF      | -5.79926  | 0.00302978 |     0.0986052 |
| E       | -6.17426  | 0.00208234 |     0.286105  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '</tool_response>', '<think>', '.', '  \n', '<|file_sep|>', '.Category', '\\', '。', ' **.**', ' -->', '\t  \n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\n', '**', '</', ';', '\t\n', '\n  \n', '.ht', '/AFP', '<', '.<', '\n   \n', '$\\', '/E', '.\\', '  \n\n', '\\E']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Asia', 'CNY']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nWhich continent is the country with the city of Alexandria on, and what is that country's three-letter currency code? Reply only as '<continent>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Africa', 'Africa', ' Egypt', ' Europe', 'Asia', 'Europe', ' continents', ' Asia', '大陆', ' africa', '埃及', 'Egypt', ' Americas', ' Greece', ' Oce', ' Antarctica', ' continental', 'continental', ' Europa', ' europe', ' Arabia', ';**', ' continente', ';', ' Caribbean', ' Romania', 'Europa', ' asia', ' Tunisia', '非洲', 'gypt', ' مصر']

Generation (5 tokens):
```text
Africa; EGP<|im_end|>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Africa  | -0.307058 | 0.735608   |    -0.0341878 |
| <       | -2.30706  | 0.0995537  |     0.340812  |
| Europe  | -2.43206  | 0.0878558  |    -0.159188  |
| ;       | -3.93206  | 0.0196033  |     0.215812  |
| Africa  | -4.30706  | 0.0134731  |     0.340812  |
| A       | -4.80706  | 0.00817187 |    -0.0341878 |
| <a      | -5.18206  | 0.00561644 |     0.340812  |
| Af      | -5.43206  | 0.00437409 |    -0.0341878 |
| <A      | -5.80706  | 0.00300626 |     0.340812  |
| AF      | -6.05706  | 0.00234128 |    -0.159188  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '</tool_response>', '<|im_start|>', '<think>', '.', '  \n', '<|file_sep|>', '.Category', '\\', '。', ' **.**', ' -->', '\t  \n', ';', '\\n', '**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '</', '.ht', '\n  \n', '\t\n', '<', '.<', '/AFP', '\n   \n', '.\\', '/E', '$\\', '\\E', '  \n\n']

Coverage: 5 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Africa', 'EGP']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.
