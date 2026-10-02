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
elapsed_seconds: 4.38
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'O' over 'North'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='O') |   p(first='North') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|---------------:|-------------------:|------------------------:|-----:|
| Base                          |             0           |    1.32481e-07 |        9.90155e-09 |             1.42383e-07 |    0 |
| raw J-coordinate exchange     |             0.3125      |    1.06583e-07 |        5.828e-09   |             1.12411e-07 |    0 |
| raw plain-coordinate exchange |             0.0625      |    1.05095e-07 |        7.37881e-09 |             1.12474e-07 |    0 |
| matched-random delta          |             1.90735e-06 |    1.47978e-07 |        1.10598e-08 |             1.59038e-07 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Toronto asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', ';</', '»;', '++;', '4', '_;', '.;', ';\\', '%;', ';;', '”;', '*;', '__;', ' [];', ' {};', '؛', ';*', ';$', ';"', ');', ' "";', '6', '";', ';<', ';}', '};', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0868241 | 0.916838    |             0 |
| <       | -2.58682   | 0.0752587   |             0 |
| 6       | -5.33682   | 0.00481113  |             0 |
| ;       | -6.83682   | 0.00107351  |             0 |
| >       | -8.27432   | 0.00025498  |             0 |
| 2       | -8.33682   | 0.000239532 |             0 |
| <s      | -8.46182   | 0.000211386 |             0 |
| <think> | -8.52432   | 0.000198579 |             0 |
| <span   | -8.77432   | 0.000154653 |             0 |
| ;<      | -9.08682   | 0.000113147 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', '</tool_response>', ')', '<\\/', '.<', '\\n', '!', '”', ';.', '\t  \n', ';charset', '\\', ',<', '.;', ' -->', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'itarian', '<br', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Toronto asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', ';</', '»;', '.;', '++;', ';\\', '%;', '_;', ';;', '”;', '4', '__;', '*;', ' [];', ';*', ' {};', '؛', ';$', ';"', ');', ' "";', ';<', ';.', '";', '};', '];', ';}', '.);']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0543423 | 0.947108    |     0.0324818 |
| <       | -3.05434   | 0.0471537   |    -0.467518  |
| 6       | -5.67934   | 0.0034158   |    -0.342518  |
| ;       | -7.17934   | 0.000762169 |    -0.342518  |
| 2       | -8.42934   | 0.000218365 |    -0.0925179 |
| <s      | -8.67934   | 0.000170063 |    -0.217518  |
| <span   | -8.80434   | 0.00015008  |    -0.0300179 |
| <think> | -8.80434   | 0.00015008  |    -0.280018  |
| >       | -8.86684   | 0.000140987 |    -0.592518  |
| ;<      | -9.36684   | 8.5513e-05  |    -0.280018  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '**', '.Category', '<|im_start|>', '<|file_sep|>', '<', '>', ')', '</tool_response>', '<\\/', '.<', '\\n', '!', ';.', '”', '\t  \n', '\\', ';charset', ',<', '.;', '<<<', '```', ' -->', 'itarian', '<br', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Toronto asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', '»;', ';</', '++;', '_;', '.;', ';\\', '4', '%;', ';;', '”;', '*;', ' [];', '__;', '؛', ';*', ' {};', ';$', ';"', ');', ' "";', '";', ';<', '6', '};', ';}', ';.', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0684031 | 0.933884    |     0.018421  |
| <       | -2.8184    | 0.0597012   |    -0.231579  |
| 6       | -5.5684    | 0.00381657  |    -0.231579  |
| ;       | -6.9434    | 0.00096498  |    -0.106579  |
| >       | -8.3184    | 0.000243985 |    -0.0440788 |
| <s      | -8.6309    | 0.000178503 |    -0.169079  |
| 2       | -8.6934    | 0.000167688 |    -0.356579  |
| <span   | -8.8809    | 0.000139019 |    -0.106579  |
| <think> | -8.9434    | 0.000130596 |    -0.419079  |
| ;<      | -9.1934    | 0.000101708 |    -0.106579  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', '<\\/', ')', '.<', '\\n', '!', ';.', '\t  \n', '”', ';charset', '\\', ',<', '.;', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<br', ' -->', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Toronto asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '**;', ';</', '»;', '++;', '.;', '_;', ';;', ';\\', '”;', '%;', '4', '*;', ' [];', '__;', '؛', ' {};', ';*', ';$', ';"', ');', '";', ' "";', ';.', '};', ';<', ';}', '];', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.101201 | 0.903751    |    -0.0143774 |
| <       | -2.4762   | 0.0840619   |     0.110623  |
| 6       | -4.7262   | 0.00886006  |     0.610622  |
| ;       | -6.7262   | 0.00119908  |     0.110622  |
| >       | -8.2262   | 0.000267551 |     0.0481234 |
| <s      | -8.4137   | 0.000221807 |     0.0481234 |
| 2       | -8.4762   | 0.000208369 |    -0.139377  |
| <span   | -8.6012   | 0.000183885 |     0.173123  |
| <think> | -8.6637   | 0.000172744 |    -0.139377  |
| ;<      | -8.9762   | 0.000126382 |     0.110623  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '**', '.Category', '<|file_sep|>', '<', '>', '</tool_response>', '.<', ')', '<\\/', '\\n', '!', ';.', '”', '\t  \n', '.;', ';charset', '```', '\\', ' -->', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', 'itarian', '。', '<<<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[24420, 4994], [46, 341, 8893]]; reported probabilities cover only first tokens ('North', 'O'), not the full multi-token answers.
