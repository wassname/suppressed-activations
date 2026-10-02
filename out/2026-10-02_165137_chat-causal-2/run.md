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
elapsed_seconds: 4.78
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'C' over 'Be'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' China', ' Egypt') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' China', ' Egypt').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/china_egypt_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='C') |   p(first='Be') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|----------------:|------------------------:|-----:|
| Base                          |                 0       |    4.54103e-07 |     3.80788e-09 |             4.57911e-07 |    0 |
| raw J-coordinate exchange     |                 0.03125 |    4.67622e-07 |     3.80061e-09 |             4.71423e-07 |    0 |
| raw plain-coordinate exchange |                -0.0625  |    4.48221e-07 |     4.00097e-09 |             4.52222e-07 |    0 |
| matched-random delta          |                -0.28125 |    4.69964e-07 |     5.22083e-09 |             4.75185e-07 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Shanghai is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', ';;', '%;', '”;', ' {};', ' [];', ';*', '6', '؛', '*;', ';"', '__;', '5', ';}', ');', ' "";', ';d', '};', '";', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.104943 | 0.900376    |             0 |
| <       | -2.35494  | 0.0948989   |             0 |
| 6       | -6.47994  | 0.0015339   |             0 |
| >       | -7.35494  | 0.000639424 |             0 |
| ;       | -7.47994  | 0.00056429  |             0 |
| <s      | -8.10494  | 0.000302043 |             0 |
| <think> | -8.22994  | 0.000266552 |             0 |
| <span   | -8.47994  | 0.000207591 |             0 |
| 2       | -8.79244  | 0.000151877 |             0 |
| ;<      | -9.29244  | 9.21178e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<think>', '</', ';', '<|im_start|>', '<', '**', '.Category', '<|file_sep|>', '>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '\\', '<<<', '”', ' <<<', '\t  \n', '<<<<', '。', ' <$', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';charset', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Shanghai is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '4', '；', '++;', ';</', '»;', '**;', ';\\', '_;', ';$', ';;', '.;', '%;', '”;', ' {};', ' [];', '6', ';*', '؛', '*;', ';"', '5', '__;', ');', ';}', ' "";', '};', ';)', ';d', '";']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0756054 | 0.927182    |     0.0293373 |
| <       | -2.70061   | 0.0671648   |    -0.345663  |
| 6       | -5.95061   | 0.00260426  |     0.529337  |
| >       | -7.20061   | 0.000746134 |     0.154337  |
| ;       | -7.70061   | 0.000452553 |    -0.220663  |
| <think> | -8.26311   | 0.000257857 |    -0.0331631 |
| <s      | -8.32561   | 0.000242234 |    -0.220663  |
| <span   | -8.51311   | 0.000200819 |    -0.0331631 |
| 2       | -8.82561   | 0.000146922 |    -0.0331631 |
| ;<      | -9.51311   | 7.38773e-05 |    -0.220663  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<|im_start|>', '**', '<', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', '\\', '!', '”', ' <<<', '<<<<', '\t  \n', 'itarian', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <$', '>>', '="<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Shanghai is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', ';;', ';$', '”;', '.;', ' {};', '%;', '6', ' [];', '؛', ';*', '*;', ';"', '__;', '5', ';}', ');', ' "";', '};', ';d', '";', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| 4       | -0.11798 | 0.888714    |    -0.013037  |
| <       | -2.24298 | 0.106142    |     0.111963  |
| 6       | -6.24298 | 0.00194405  |     0.236963  |
| >       | -7.24298 | 0.000715178 |     0.111963  |
| ;       | -7.61798 | 0.000491534 |    -0.138037  |
| <s      | -8.11798 | 0.00029813  |    -0.0130377 |
| <think> | -8.24298 | 0.000263099 |    -0.0130377 |
| <span   | -8.43048 | 0.000218117 |     0.0494623 |
| 2       | -8.74298 | 0.000159578 |     0.0494623 |
| ;<      | -9.36798 | 8.54157e-05 |    -0.0755377 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', '<|im_start|>', ';', '<', '**', '.Category', '<|file_sep|>', '>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', '”', '\t  \n', '<<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' <$', '。', ';charset', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Shanghai is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', '**;', ';\\', '_;', '.;', '”;', ';;', ';$', ' {};', '%;', ' [];', '؛', ';*', '*;', '6', ';"', '__;', '5', ');', ';}', ' "";', '};', '";', ';d', ';<']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| 4       | -0.13311 | 0.875369    |    -0.0281671 |
| <       | -2.13311 | 0.118468    |     0.221833  |
| 6       | -6.00811 | 0.00245873  |     0.471833  |
| >       | -7.25811 | 0.000704438 |     0.0968328 |
| ;       | -7.25811 | 0.000704438 |     0.221833  |
| <s      | -7.88311 | 0.000377059 |     0.221832  |
| <think> | -8.13311 | 0.000293654 |     0.0968323 |
| <span   | -8.38311 | 0.000228698 |     0.0968323 |
| 2       | -8.75811 | 0.000157181 |     0.0343323 |
| ;<      | -9.00811 | 0.000122413 |     0.284332  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<|im_start|>', '<', '**', '.Category', '<|file_sep|>', '>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '<<<', '”', '\\', ' <<<', '\t  \n', '```', '。', '<<<<', ';charset', ';.', '.;']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[3320, 22909], [34, 24736]]; reported probabilities cover only first tokens ('Be', 'C'), not the full multi-token answers.
