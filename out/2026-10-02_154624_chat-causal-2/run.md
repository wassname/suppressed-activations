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
elapsed_seconds: 24.00
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Sweden', ' Japan') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v2_allpos.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |                0        |      2.57153e-10 |        4.92854e-09 |             5.18569e-09 |    0 |
| raw J-coordinate exchange     |                1.09375  |      5.11171e-10 |        3.28157e-09 |             3.79274e-09 |    0 |
| raw plain-coordinate exchange |                0.03125  |      2.65242e-10 |        4.92717e-09 |             5.19241e-09 |    0 |
| matched-random delta          |                0.171875 |      3.04964e-10 |        4.92187e-09 |             5.22683e-09 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', ';\\', '_;', '**;', '.;', '”;', ';$', ';;', ' {};', '%;', ' [];', ';*', '*;', '__;', '؛', ';"', '6', ');', ' "";', ';}', '5', '";', '};', '`;', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0657232 | 0.93639     |             0 |
| <       | -2.81572   | 0.0598614   |             0 |
| 6       | -6.56572   | 0.00140781  |             0 |
| >       | -7.69072   | 0.000457047 |             0 |
| ;       | -7.69072   | 0.000457047 |             0 |
| <think> | -8.31572   | 0.00024464  |             0 |
| <s      | -8.56572   | 0.000190526 |             0 |
| 2       | -8.94072   | 0.000130946 |             0 |
| <span   | -8.94072   | 0.000130946 |             0 |
| ;<      | -9.81572   | 5.45865e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '<|im_start|>', '<', '**', '.Category', '<|file_sep|>', '>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '\\', '!', '<br', '<<<', '”', ' <<<', '\t  \n', '<<<<', '.;', ' <$', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';charset', ';.']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', '4', '++;', ';</', '»;', ';\\', '_;', '**;', '.;', '”;', '%;', ';;', ' {};', ' [];', ';$', '؛', '__;', '*;', ';*', ';"', ');', '6', ' "";', ';}', '5', '";', '};', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0661934 | 0.93595     |  -0.000470176 |
| <       | -2.81619   | 0.0598333   |  -0.000470161 |
| 6       | -6.31619   | 0.00180681  |   0.24953     |
| ;       | -7.69119   | 0.000456833 |  -0.000470161 |
| >       | -7.81619   | 0.000403153 |  -0.12547     |
| <think> | -8.06619   | 0.000313976 |   0.24953     |
| <s      | -8.62869   | 0.000178898 |  -0.0629702   |
| 2       | -8.81619   | 0.000148312 |   0.12453     |
| <span   | -8.94119   | 0.000130885 |  -0.000470161 |
| ;<      | -9.62869   | 6.5813e-05  |   0.18703     |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', ')', '<\\/', '\\n', ',<', '!', '\\', '<br', '<<<', '”', ' <<<', '\t  \n', '.;', '<<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';charset', '>>', ' <$']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', '++;', '»;', ';</', ';\\', '_;', '**;', '.;', '”;', ';$', ';;', '%;', ' {};', ' [];', '؛', ';*', '__;', '*;', ';"', '6', ');', ' "";', ';}', '5', '";', '};', '`;', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.066001 | 0.93613     |  -0.000277802 |
| <       | -2.816    | 0.0598448   |  -0.000277758 |
| 6       | -6.441    | 0.00159481  |   0.124722    |
| >       | -7.566    | 0.000517759 |   0.124722    |
| ;       | -7.691    | 0.000456921 |  -0.000277519 |
| <think> | -8.316    | 0.000244572 |  -0.000277519 |
| <s      | -8.566    | 0.000190473 |  -0.000277519 |
| <span   | -8.8785   | 0.000139353 |   0.0622225   |
| 2       | -9.0035   | 0.000122979 |  -0.0627775   |
| ;<      | -9.691    | 6.18375e-05 |   0.124722    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '<', '**', '.Category', '<|file_sep|>', '>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '!', '\\', '<br', '<<<', '”', ' <<<', '\t  \n', '<<<<', '.;', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';.', ' <$', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', '_;', '**;', ';\\', '.;', '”;', ';;', ';$', ' {};', '%;', ' [];', '*;', ';*', '؛', ';"', '__;', ');', '6', ';}', ' "";', '5', '};', '";', '`;', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0670782 | 0.935122    |   -0.00135501 |
| <       | -2.81708   | 0.0597804   |   -0.00135493 |
| 6       | -5.94208   | 0.00262657  |    0.623645   |
| ;       | -7.56708   | 0.000517201 |    0.123645   |
| >       | -7.69208   | 0.000456429 |   -0.00135469 |
| <think> | -8.44208   | 0.000215602 |   -0.126355   |
| <s      | -8.50458   | 0.000202539 |    0.0611448  |
| 2       | -8.87958   | 0.000139203 |    0.0611448  |
| <span   | -8.87958   | 0.000139203 |    0.0611448  |
| ;<      | -9.62958   | 6.57547e-05 |    0.186145   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', ')', '<\\/', '\\n', ',<', '!', '\\', '<br', '”', '<<<', '.;', ' <<<', '\t  \n', ';.', '<<<<', ';charset', '>>', ' <$']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.
