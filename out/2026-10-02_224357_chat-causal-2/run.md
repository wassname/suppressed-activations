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
elapsed_seconds: 4.62
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'North' over 'Europe'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='North') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |                 0       |        5.96508e-09 |         1.67295e-08 |             2.26946e-08 |    0 |
| raw J-coordinate exchange     |                 0.625   |        6.59932e-09 |         9.90675e-09 |             1.65061e-08 |    0 |
| raw plain-coordinate exchange |                 0       |        6.16176e-09 |         1.72811e-08 |             2.34428e-08 |    0 |
| matched-random delta          |                 0.09375 |        6.95671e-09 |         1.77646e-08 |             2.47213e-08 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Barcelona asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', ';</', '4', '**;', '»;', '++;', ';\\', '_;', '.;', '%;', ';;', '”;', '*;', ' [];', '__;', ' {};', '؛', ';*', ';$', ';"', ');', '6', ' "";', '";', ';}', ';<', '};', '];', '();']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0623444 | 0.939559    |             0 |
| <       | -2.93734   | 0.0530063   |             0 |
| 6       | -5.43734   | 0.00435102  |             0 |
| ;       | -7.06234   | 0.000856767 |             0 |
| <span   | -8.06234   | 0.000315187 |             0 |
| 2       | -8.24984   | 0.000261299 |             0 |
| <s      | -8.24984   | 0.000261299 |             0 |
| >       | -8.31234   | 0.000245468 |             0 |
| <think> | -8.37484   | 0.000230596 |             0 |
| ;<      | -9.31234   | 9.03026e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', '</tool_response>', ')', '.<', '<\\/', '\\n', '!', ';.', '”', '\t  \n', '.;', ',<', ';charset', 'itarian', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\\', ' -->', '<<<', '<br', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Barcelona asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', '4', ';</', '**;', '++;', '.;', '_;', ';\\', '%;', ';;', '__;', ' [];', '”;', '*;', ' {};', '؛', ';*', ';$', ');', ';"', ' "";', '6', '";', '};', '];', ';<', ';}', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0550498 | 0.946438    |    0.00729461 |
| <       | -3.05505   | 0.0471204   |   -0.117705   |
| 6       | -5.68005   | 0.00341339  |   -0.242705   |
| ;       | -7.05505   | 0.00086304  |    0.00729465 |
| <span   | -8.18005   | 0.000280188 |   -0.117705   |
| >       | -8.24255   | 0.000263212 |    0.0697947  |
| <s      | -8.24255   | 0.000263212 |    0.00729465 |
| <think> | -8.43005   | 0.000218211 |   -0.0552053  |
| 2       | -8.49255   | 0.00020499  |   -0.242705   |
| ;<      | -9.24255   | 9.68304e-05 |    0.0697947  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', '”', ';.', '\t  \n', '\\', '.;', ',<', ';charset', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', ' -->', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Barcelona asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', ';</', '4', '»;', '**;', '++;', ';\\', '_;', '.;', '%;', '”;', ';;', '*;', ' [];', '__;', ' {};', '؛', ';*', ';$', ';"', ');', ' "";', '6', '";', ';}', ';<', '};', '];', '();']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0611538 | 0.940679    |    0.00119053 |
| <       | -2.93615   | 0.0530694   |    0.00119042 |
| 6       | -5.68615   | 0.00339262  |   -0.248809   |
| ;       | -7.18615   | 0.000756995 |   -0.123809   |
| 2       | -8.18615   | 0.000278483 |    0.0636911  |
| <span   | -8.18615   | 0.000278483 |   -0.123809   |
| <s      | -8.37365   | 0.000230871 |   -0.123809   |
| <think> | -8.43615   | 0.000216883 |   -0.0613089  |
| >       | -8.49865   | 0.000203743 |   -0.186309   |
| ;<      | -9.37365   | 8.49325e-05 |   -0.0613089  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', '”', ';.', '\t  \n', '.;', '\\', ',<', ';charset', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', ' -->', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Barcelona asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', '»;', ';</', '.;', '++;', '_;', ';\\', '4', '”;', '%;', ';;', '*;', ' [];', '__;', '؛', ' {};', ';*', ';$', ';"', ');', ' "";', '";', '6', '};', ';}', ';<', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0648107 | 0.937245    |   -0.00246631 |
| <       | -2.93981   | 0.0528757   |   -0.00246644 |
| 6       | -5.06481   | 0.00631511  |    0.372534   |
| ;       | -6.81481   | 0.0010974   |    0.247534   |
| <span   | -7.93981   | 0.000356274 |    0.122534   |
| 2       | -8.12731   | 0.000295361 |    0.122534   |
| >       | -8.18981   | 0.000277466 |    0.122534   |
| <s      | -8.18981   | 0.000277466 |    0.0600338  |
| <think> | -8.50231   | 0.000202999 |   -0.127466   |
| ;<      | -9.00231   | 0.000123125 |    0.310034   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', ';.', '”', '\t  \n', '.;', '\\', '<<<', ' -->', ';charset', ',<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '```', '。', 'itarian']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24420, 4994]]; reported probabilities cover only first tokens ('Europe', 'North'), not the full multi-token answers.
