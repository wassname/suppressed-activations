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
elapsed_seconds: 4.37
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Mexico' over 'Madrid'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Spain', ' Mexico') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Spain', ' Mexico').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/spain_mexico_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Mexico') |   p(first='Madrid') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|--------------------:|--------------------:|------------------------:|-----:|
| Base                          |                0        |         4.35604e-10 |         2.8405e-09  |             3.2761e-09  |    0 |
| raw J-coordinate exchange     |                0.421875 |         6.4374e-10  |         2.75292e-09 |             3.39666e-09 |    0 |
| raw plain-coordinate exchange |                0.046875 |         4.56803e-10 |         2.84232e-09 |             3.29913e-09 |    0 |
| matched-random delta          |               -0.109375 |         4.94616e-10 |         3.59809e-09 |             4.0927e-09  |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Barcelona is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', '”;', ';;', '%;', ' {};', ' [];', '6', ';*', '__;', '؛', '*;', ';"', '5', ';}', ');', ' "";', '};', '";', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0855369 | 0.918019    |             0 |
| <       | -2.58554   | 0.0753556   |             0 |
| 6       | -5.58554   | 0.00375173  |             0 |
| >       | -7.58554   | 0.000507742 |             0 |
| <think> | -7.96054   | 0.000348966 |             0 |
| <s      | -8.08554   | 0.000307961 |             0 |
| <span   | -8.08554   | 0.000307961 |             0 |
| ;       | -8.08554   | 0.000307961 |             0 |
| 2       | -8.64804   | 0.000175471 |             0 |
| ;<      | -9.64804   | 6.45522e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '<\\/', '</tool_response>', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', ' <$', '”', '<<<<', '\t  \n', '="<', '_<', '<-', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Barcelona is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', '%;', ';;', ';$', ' {};', ' [];', '”;', '__;', '6', ';*', '*;', '؛', ';"', ');', ';}', '5', ' "";', '};', '];', '";', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0856017 | 0.91796     |  -6.48946e-05 |
| <       | -2.5856    | 0.0753507   |  -6.48499e-05 |
| 6       | -5.5856    | 0.00375149  |  -6.48499e-05 |
| >       | -7.5856    | 0.000507709 |  -6.48499e-05 |
| <s      | -7.9606    | 0.000348943 |   0.124935    |
| ;       | -7.9606    | 0.000348943 |   0.124935    |
| <span   | -8.0856    | 0.000307941 |  -6.48499e-05 |
| <think> | -8.0856    | 0.000307941 |  -0.125065    |
| 2       | -8.7106    | 0.000164829 |  -0.0625648   |
| ;<      | -9.6481    | 6.4548e-05  |  -6.48499e-05 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '**', '<|im_start|>', '.Category', '>', '<|file_sep|>', '.<', '<\\/', '</tool_response>', ')', '\\n', ',<', '<br', '\\', '!', '<<<', ' <<<', '”', '\t  \n', '<<<<', ' <$', '="<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';<', '.;']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Barcelona is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', '%;', ';;', ' {};', '”;', ' [];', '6', ';*', '__;', '*;', '؛', ';"', '5', ';}', ');', ' "";', '};', '";', ';d', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0848935 | 0.91861     |   0.000643365 |
| <       | -2.58489   | 0.0754041   |   0.000643492 |
| 6       | -5.70989   | 0.00331302  |  -0.124357    |
| >       | -7.83489   | 0.000395684 |  -0.249357    |
| <s      | -8.08489   | 0.000308159 |   0.00064373  |
| ;       | -8.08489   | 0.000308159 |   0.00064373  |
| <think> | -8.08489   | 0.000308159 |  -0.124356    |
| <span   | -8.20989   | 0.00027195  |  -0.124356    |
| 2       | -8.64739   | 0.000175584 |   0.00064373  |
| ;<      | -9.70989   | 6.06802e-05 |  -0.0618563   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '<\\/', '</tool_response>', ')', '\\n', ',<', '<br', '!', '<<<', '\\', ' <<<', '”', ' <$', '<<<<', '\t  \n', '="<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '_<', '<-']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Barcelona is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '»;', '++;', '**;', ';\\', '_;', '.;', ';$', ';;', '”;', '%;', ' {};', ' [];', ';*', '؛', '*;', ';"', '6', '__;', ');', ';}', '5', ' "";', '};', '";', '.);', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0991141 | 0.905639    |    -0.0135772 |
| <       | -2.47411   | 0.0842376   |     0.111423  |
| 6       | -4.97411   | 0.00691464  |     0.611423  |
| >       | -7.47411   | 0.000567588 |     0.111423  |
| ;       | -7.72411   | 0.000442038 |     0.361423  |
| <s      | -7.97411   | 0.00034426  |     0.111423  |
| <span   | -8.09911   | 0.000303808 |    -0.0135775 |
| <think> | -8.09911   | 0.000303808 |    -0.138577  |
| 2       | -8.41161   | 0.000222271 |     0.236423  |
| ;<      | -9.47411   | 7.68147e-05 |     0.173923  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', '”', ' <$', '<<<<', '\t  \n', '.;', '```', '="<', '_<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[218787], [66502, 4170]]; reported probabilities cover only first tokens ('Madrid', 'Mexico'), not the full multi-token answers.
