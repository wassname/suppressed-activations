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
elapsed_seconds: 4.82
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Br' over 'Berlin'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Br') |   p(first='Berlin') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|----------------:|--------------------:|------------------------:|-----:|
| Base                          |                0        |     9.79377e-10 |         3.31319e-09 |             4.29257e-09 |    0 |
| raw J-coordinate exchange     |                0.59375  |     1.01018e-09 |         1.88727e-09 |             2.89745e-09 |    0 |
| raw plain-coordinate exchange |               -0.015625 |     9.63541e-10 |         3.31095e-09 |             4.27449e-09 |    0 |
| matched-random delta          |               -0.125    |     9.65006e-10 |         3.69925e-09 |             4.66425e-09 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Munich is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', ';$', '.;', '”;', ';;', '%;', ' {};', ' [];', ';*', '6', ';"', '__;', '؛', '*;', '5', ';}', ');', ' "";', '};', '";', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.119104 | 0.887716    |             0 |
| <       | -2.2441   | 0.106023    |             0 |
| 6       | -5.8691   | 0.0028254   |             0 |
| >       | -7.6191   | 0.000490982 |             0 |
| ;       | -7.6191   | 0.000490982 |             0 |
| <s      | -7.7441   | 0.00043329  |             0 |
| <think> | -7.8691   | 0.000382377 |             0 |
| <span   | -8.2441   | 0.000262804 |             0 |
| 2       | -8.7441   | 0.000159398 |             0 |
| ;<      | -9.2441   | 9.66801e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '<\\/', '</tool_response>', ')', ',<', '\\n', '<br', '<<<', ' <<<', '!', '\\', ' <$', '<<<<', '”', '="<', '\t  \n', '_<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<-']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Munich is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', ';\\', '**;', '_;', '.;', ';$', '”;', ';;', '%;', ' {};', ' [];', ';*', ';"', '6', '*;', '__;', '؛', ');', ';}', '5', ' "";', '";', '};', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.119387 | 0.887465    |  -0.000282936 |
| <       | -2.24439  | 0.105993    |  -0.000283003 |
| 6       | -5.74439  | 0.0032007   |   0.124717    |
| <s      | -7.74439  | 0.000433167 |  -0.000282764 |
| >       | -7.74439  | 0.000433167 |  -0.125283    |
| ;       | -7.74439  | 0.000433167 |  -0.125283    |
| <think> | -7.86939  | 0.000382269 |  -0.000282764 |
| <span   | -8.11939  | 0.000297711 |   0.124717    |
| 2       | -8.68189  | 0.000169631 |   0.0622168   |
| ;<      | -9.24439  | 9.66527e-05 |  -0.000283241 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '<\\/', '</tool_response>', ')', ',<', '\\n', '<br', '<<<', ' <<<', '!', '\\', ' <$', '”', '<<<<', '\t  \n', '="<', '_<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Munich is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', '”;', ';;', '%;', ' {};', ' [];', '6', ';*', ';"', '؛', '__;', '*;', '5', ');', ';}', ' "";', '";', '};', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.119781 | 0.887115    |  -0.000677042 |
| <       | -2.24478  | 0.105951    |  -0.000677109 |
| 6       | -5.61978  | 0.00362543  |   0.249323    |
| >       | -7.61978  | 0.000490649 |  -0.000677109 |
| ;       | -7.61978  | 0.000490649 |  -0.000677109 |
| <think> | -7.74478  | 0.000432996 |   0.124323    |
| <s      | -7.99478  | 0.000337218 |  -0.250677    |
| <span   | -8.36978  | 0.000231766 |  -0.125677    |
| 2       | -8.68228  | 0.000169564 |   0.0618229   |
| ;<      | -9.24478  | 9.66146e-05 |  -0.000677109 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '\\', ' <<<', '<<<', '!', '”', '<<<<', ' <$', '\t  \n', '="<', '_<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<-']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Munich is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', ';\\', '**;', '_;', '.;', ';$', '”;', ';;', '%;', ' {};', ' [];', '؛', ';*', '__;', ';"', '*;', '6', ');', ';}', '5', ' "";', '};', '";', ';d', ';<']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.133886 | 0.87469     |    -0.0147819 |
| <       | -2.13389  | 0.118376    |     0.110218  |
| 6       | -5.63389  | 0.00357466  |     0.235219  |
| ;       | -7.50889  | 0.000548192 |     0.110219  |
| >       | -7.63389  | 0.000483778 |    -0.0147815 |
| <s      | -7.88389  | 0.000376766 |    -0.139781  |
| <think> | -8.00889  | 0.000332495 |    -0.139781  |
| <span   | -8.32139  | 0.000243259 |    -0.077282  |
| 2       | -8.69639  | 0.000167189 |     0.047718  |
| ;<      | -9.13389  | 0.000107945 |     0.110218  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', ' <<<', '!', '\\', ' <$', '”', '<<<<', '="<', '\t  \n', '_<', ';<', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.
