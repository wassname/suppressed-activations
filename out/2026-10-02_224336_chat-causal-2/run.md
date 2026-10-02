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
elapsed_seconds: 4.43
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'South' over 'Europe'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='South') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-------------------:|--------------------:|------------------------:|-----:|
| Base                          |                 0       |        1.8244e-08  |         1.37713e-08 |             3.20153e-08 |    0 |
| raw J-coordinate exchange     |                 0.4375  |        2.73407e-08 |         1.33248e-08 |             4.06655e-08 |    0 |
| raw plain-coordinate exchange |                -0.03125 |        1.89573e-08 |         1.47639e-08 |             3.37212e-08 |    0 |
| matched-random delta          |                -0.0625  |        1.90525e-08 |         1.53091e-08 |             3.43615e-08 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Munich asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', ';</', '**;', '++;', '_;', '.;', ';\\', '4', '%;', '”;', ';;', ' [];', '*;', '__;', '؛', ';*', ' {};', ';$', ';"', ');', ' "";', '";', ';<', '6', '};', ';}', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0694288 | 0.932927    |             0 |
| <       | -2.81943   | 0.05964     |             0 |
| 6       | -5.44443   | 0.00432031  |             0 |
| ;       | -6.81943   | 0.00109234  |             0 |
| >       | -8.19443   | 0.000276188 |             0 |
| 2       | -8.44443   | 0.000215095 |             0 |
| <s      | -8.44443   | 0.000215095 |             0 |
| <think> | -8.56943   | 0.000189821 |             0 |
| <span   | -8.63193   | 0.00017832  |             0 |
| ;<      | -9.19443   | 0.000101604 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', '</tool_response>', ')', '.<', '<\\/', '\\n', '!', '”', ';.', '.;', ',<', '\t  \n', ';charset', '<<<', '<br', '\\', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' -->', 'itarian', '<<<<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Munich asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', ';</', '**;', '.;', '++;', '_;', '4', ';\\', ';;', '%;', '”;', '*;', ' [];', '__;', '؛', ';*', ' {};', ';$', ';"', ');', ' "";', '";', '6', ';<', ';}', '};', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0711402 | 0.931331    |   -0.00171144 |
| <       | -2.82114   | 0.059538    |   -0.00171161 |
| 6       | -5.19614   | 0.0055379   |    0.248289   |
| ;       | -6.69614   | 0.00123567  |    0.123289   |
| >       | -8.13364   | 0.000293498 |    0.0607882  |
| 2       | -8.25864   | 0.000259011 |    0.185788   |
| <span   | -8.25864   | 0.000259011 |    0.373288   |
| <s      | -8.32114   | 0.000243318 |    0.123288   |
| <think> | -8.38364   | 0.000228576 |    0.185788   |
| ;<      | -9.00864   | 0.000122348 |    0.185788   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '**', '<|im_start|>', '.Category', '<|file_sep|>', '<', '>', ')', '</tool_response>', '.<', '<\\/', '\\n', '!', '”', '\t  \n', ';.', '\\', '.;', ';charset', ',<', ' -->', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', 'itarian', ' <<<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Munich asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', '**;', ';</', '.;', '++;', ';\\', '_;', '4', '”;', '%;', ';;', '*;', ' [];', '__;', '؛', ';*', ' {};', ';$', ';"', ');', ' "";', '";', '6', ';<', '};', ';}', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0623285 | 0.939574    |    0.00710033 |
| <       | -2.93733   | 0.0530072   |   -0.1179     |
| 6       | -5.43733   | 0.00435109  |    0.00710058 |
| ;       | -6.81233   | 0.00110013  |    0.00710058 |
| >       | -8.31233   | 0.000245472 |   -0.1179     |
| <think> | -8.37483   | 0.000230599 |    0.1946     |
| 2       | -8.37483   | 0.000230599 |    0.0696001  |
| <s      | -8.62483   | 0.000179591 |   -0.1804     |
| <span   | -8.68733   | 0.00016871  |   -0.0553999  |
| ;<      | -9.24983   | 9.61282e-05 |   -0.0553999  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '**', '<|im_start|>', '.Category', '<|file_sep|>', '<', '>', ')', '</tool_response>', '<\\/', '.<', '\\n', '!', '”', ';.', '\t  \n', ',<', '\\', ';charset', '.;', '<br', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' -->', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Munich asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', ';</', '»;', '++;', '_;', '.;', ';\\', '4', ';;', '%;', '”;', '*;', ' [];', '__;', '؛', ' {};', ';*', ';$', ';"', ');', ' "";', '";', ';<', '6', '};', ';}', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0885703 | 0.915239    |    -0.0191415 |
| <       | -2.58857   | 0.0751274   |     0.230858  |
| 6       | -5.08857   | 0.00616683  |     0.355859  |
| ;       | -6.71357   | 0.00121432  |     0.105859  |
| >       | -8.08857   | 0.000307028 |     0.105858  |
| <s      | -8.27607   | 0.000254535 |     0.168358  |
| 2       | -8.46357   | 0.000211017 |    -0.0191422 |
| <think> | -8.52607   | 0.000198232 |     0.0433578 |
| <span   | -8.52607   | 0.000198232 |     0.105858  |
| ;<      | -9.02607   | 0.000120234 |     0.168358  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', '</tool_response>', ')', '.<', '<\\/', '\\n', '!', ';.', '.;', '”', '\t  \n', '\\', ';charset', ',<', ' -->', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [24225, 4994]]; reported probabilities cover only first tokens ('Europe', 'South'), not the full multi-token answers.
