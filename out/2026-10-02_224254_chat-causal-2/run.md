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
relation: arithmetic_control
elapsed_seconds: 4.84
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Africa' over 'Asia'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Africa') |   p(first='Asia') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|------------------:|------------------------:|-----:|
| Base                          |                 0       |         1.48027e-08 |       3.00736e-09 |             1.78101e-08 |    0 |
| raw J-coordinate exchange     |                 0.6875  |         1.99109e-08 |       2.03403e-09 |             2.19449e-08 |    0 |
| raw plain-coordinate exchange |                -0.0625  |         1.35588e-08 |       2.9323e-09  |             1.64911e-08 |    0 |
| matched-random delta          |                -0.09375 |         1.68613e-08 |       3.76227e-09 |             2.06236e-08 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Shanghai asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', '4', ';</', '**;', '»;', '++;', '_;', ';\\', '.;', ';;', '%;', '”;', '__;', ' [];', ' {};', '*;', '6', ';$', '؛', ';*', ';"', ');', ' "";', '5', '";', '};', ';<', ';}', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0597036 | 0.942044    |             0 |
| <       | -2.9347    | 0.0531465   |             0 |
| 6       | -6.1847    | 0.00206071  |             0 |
| ;       | -7.0597    | 0.000859033 |             0 |
| >       | -7.9347    | 0.000358098 |             0 |
| 2       | -8.4972    | 0.000204038 |             0 |
| <think> | -8.6222    | 0.000180063 |             0 |
| <s      | -8.6847    | 0.000169154 |             0 |
| <span   | -8.8097    | 0.000149277 |             0 |
| ;<      | -9.3722    | 8.50557e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', ';.', '。', '”', '\t  \n', '.;', ';charset', '\\', 'itarian', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', '<<<', ' -->', '<br']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Shanghai asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '**;', '++;', ';\\', '_;', '.;', ';;', '”;', '%;', ' [];', '__;', ' {};', '*;', '6', ';$', '؛', ';*', ';"', ');', ' "";', '5', '";', '};', ';}', ';<', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.044499 | 0.956477    |     0.0152046 |
| <       | -3.2945   | 0.0370866   |    -0.359795  |
| 6       | -5.5445   | 0.0039089   |     0.640205  |
| ;       | -7.2945   | 0.000679265 |    -0.234795  |
| >       | -7.7945   | 0.000411995 |     0.140205  |
| 2       | -8.4195   | 0.000220525 |     0.0777044 |
| <think> | -8.732    | 0.00016134  |    -0.109796  |
| <s      | -8.9195   | 0.000133755 |    -0.234796  |
| <span   | -8.9195   | 0.000133755 |    -0.109796  |
| ;<      | -9.5445   | 7.1594e-05  |    -0.172296  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', '”', ';.', '\t  \n', '.;', '```', ';charset', 'itarian', ',<', '\\', ' -->', '。', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.</']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Shanghai asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', '4', ';</', '»;', '**;', '++;', '_;', ';\\', '.;', ';;', '%;', '”;', '__;', ' {};', ' [];', '6', '*;', ';$', '؛', ';*', ';"', ');', ' "";', '5', '";', ';}', '};', '];', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0537308 | 0.947687    |    0.00597287 |
| <       | -3.05373   | 0.0471826   |   -0.119027   |
| 6       | -6.05373   | 0.00234908  |    0.130973   |
| ;       | -7.05373   | 0.000864179 |    0.00597286 |
| >       | -7.80373   | 0.000408209 |    0.130973   |
| 2       | -8.49123   | 0.00020526  |    0.00597286 |
| <think> | -8.61623   | 0.000181142 |    0.00597286 |
| <s      | -8.80373   | 0.000150172 |   -0.119027   |
| <span   | -8.86623   | 0.000141073 |   -0.0565271  |
| ;<      | -9.36623   | 8.55653e-05 |    0.00597286 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', ';.', '”', '。', '\t  \n', '.;', ';charset', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\', ' -->', 'itarian', ',<', '```', '.</']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Shanghai asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', '4', ';</', '»;', '**;', '++;', '_;', ';\\', ';;', '.;', '”;', '%;', '__;', ' [];', ' {};', '*;', '6', ';$', '؛', ';*', ';"', ');', ' "";', '5', '";', ';<', '};', ';d', ';}']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0857427 | 0.91783     |    -0.0260391 |
| <       | -2.58574   | 0.0753401   |     0.348961  |
| 6       | -5.71074   | 0.00331021  |     0.473961  |
| ;       | -6.71074   | 0.00121776  |     0.348961  |
| >       | -7.71074   | 0.000447989 |     0.223961  |
| <s      | -8.39824   | 0.000225263 |     0.286461  |
| 2       | -8.52324   | 0.000198794 |    -0.0260391 |
| <think> | -8.58574   | 0.000186749 |     0.0364609 |
| <span   | -8.64824   | 0.000175435 |     0.161461  |
| ;<      | -8.96074   | 0.000128351 |     0.411461  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', '.<', ')', '<\\/', '\\n', '!', ';.', '”', '.;', '。', '\t  \n', ';charset', '```', 'itarian', ' -->', './.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\', '.</']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[37186], [71090]]; reported probabilities cover only first tokens ('Asia', 'Africa'), not the full multi-token answers.
