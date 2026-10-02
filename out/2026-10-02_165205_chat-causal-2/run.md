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
elapsed_seconds: 4.85
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'New' over 'Paris'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='New') |   p(first='Paris') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                          |                 0       |      1.79013e-08 |        2.44682e-08 |             4.23695e-08 |    0 |
| raw J-coordinate exchange     |                 0.28125 |      1.65538e-08 |        1.70793e-08 |             3.36331e-08 |    0 |
| raw plain-coordinate exchange |                -0.03125 |      1.68033e-08 |        2.36964e-08 |             4.04996e-08 |    0 |
| matched-random delta          |                -0.0625  |      1.84268e-08 |        2.68109e-08 |             4.52377e-08 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Lyon is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', '**;', ';\\', '_;', '.;', ';;', ';$', '”;', '%;', ' {};', ' [];', ';*', '*;', '؛', '__;', '6', ';"', ');', ';}', '5', ' "";', '};', '];', '";', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.150891 | 0.859941    |             0 |
| <       | -2.02589  | 0.131876    |             0 |
| 6       | -5.40089  | 0.00451256  |             0 |
| >       | -7.27589  | 0.000692023 |             0 |
| ;       | -7.52589  | 0.000538948 |             0 |
| <s      | -7.65089  | 0.00047562  |             0 |
| <think> | -8.02589  | 0.000326889 |             0 |
| <span   | -8.33839  | 0.000239157 |             0 |
| 2       | -8.46339  | 0.000211055 |             0 |
| ;<      | -9.27589  | 9.36551e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '<|im_start|>', '**', '.Category', '.<', '>', '<|file_sep|>', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', ' <<<', '!', '\\', ' <$', '<<<<', '”', '="<', '\t  \n', '_<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Lyon is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', '”;', ';;', '%;', ' {};', ';*', ' [];', '؛', '*;', ';"', '__;', '6', ');', ';}', ' "";', '5', '};', '";', ';<', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |   log p |           p |   delta log p |
|:--------|--------:|------------:|--------------:|
| 4       | -0.1354 | 0.873367    |     0.0154915 |
| <       | -2.1354 | 0.118197    |    -0.109509  |
| 6       | -5.3854 | 0.00458301  |     0.0154915 |
| >       | -7.2604 | 0.000702827 |     0.0154915 |
| ;       | -7.2604 | 0.000702827 |     0.265491  |
| <s      | -7.6354 | 0.000483045 |     0.0154915 |
| <think> | -8.0104 | 0.000331992 |     0.0154915 |
| <span   | -8.3854 | 0.000228174 |    -0.0470085 |
| 2       | -8.5104 | 0.000201363 |    -0.0470085 |
| ;<      | -9.0729 | 0.000114733 |     0.202991  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', ' <<<', '!', '\\', ' <$', '”', '<<<<', '="<', '\t  \n', '_<', '<-', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Lyon is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '++;', '»;', '**;', ';\\', '_;', '.;', ';$', ';;', '%;', '”;', ' {};', ' [];', ';*', '؛', '*;', '6', '__;', ';"', ');', '5', ';}', ' "";', '};', ';d', '];', '";']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.151692 | 0.859253    |  -0.000801131 |
| <       | -2.02669  | 0.131771    |  -0.000801086 |
| 6       | -5.27669  | 0.0051093   |   0.124199    |
| >       | -7.15169  | 0.000783537 |   0.124199    |
| ;       | -7.27669  | 0.000691469 |   0.249199    |
| <s      | -7.77669  | 0.000419397 |  -0.125801    |
| <think> | -8.02669  | 0.000326627 |  -0.000801086 |
| <span   | -8.27669  | 0.000254377 |   0.0616989   |
| 2       | -8.52669  | 0.000198109 |  -0.0633011   |
| ;<      | -9.15169  | 0.00010604  |   0.124199    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '<think>', '</', ';', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', ' <<<', '\\', '!', ' <$', '<<<<', '”', '="<', '\t  \n', '_<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<-']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Lyon is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '；', '4', ';</', '»;', '++;', '**;', ';\\', '_;', '.;', '”;', ';$', ';;', '%;', ' {};', ' [];', ';*', '*;', '؛', '6', '__;', ');', ';"', '5', ';}', '};', ' "";', '";', '.);', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.153208 | 0.857952    |   -0.00231627 |
| <       | -2.02821  | 0.131571    |   -0.00231624 |
| 6       | -5.02821  | 0.00655054  |    0.372684   |
| >       | -7.15321  | 0.00078235  |    0.122684   |
| <s      | -7.52821  | 0.000537701 |    0.122684   |
| ;       | -7.52821  | 0.000537701 |   -0.00231647 |
| <think> | -8.02821  | 0.000326132 |   -0.00231647 |
| <span   | -8.21571  | 0.000270373 |    0.122684   |
| 2       | -8.40321  | 0.000224147 |    0.0601835  |
| ;<      | -9.27821  | 9.34384e-05 |   -0.00231647 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', ',<', '\\n', '<br', '<<<', ' <<<', '\\', '!', ' <$', '<<<<', '”', '\t  \n', '="<', '_<', '.;', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[57590], [3446, 21318]]; reported probabilities cover only first tokens ('Paris', 'New'), not the full multi-token answers.
