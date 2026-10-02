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
elapsed_seconds: 5.18
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Can' over 'O'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Canada', ' Australia') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Canada', ' Australia').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/canada_australia_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Can') |   p(first='O') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|-----------------:|---------------:|------------------------:|-----:|
| Base                          |                0        |      5.26999e-08 |    1.62327e-07 |             2.15027e-07 |    0 |
| raw J-coordinate exchange     |               -0.249999 |      3.35719e-08 |    1.32779e-07 |             1.66351e-07 |    0 |
| raw plain-coordinate exchange |               -0.250001 |      3.91141e-08 |    1.547e-07   |             1.93814e-07 |    0 |
| matched-random delta          |                0.093749 |      6.85156e-08 |    1.92157e-07 |             2.60673e-07 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Toronto is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', ';</', '++;', '»;', ';\\', '**;', '_;', '.;', ';$', ';;', '%;', '”;', ' {};', ';*', ' [];', '؛', '6', ';"', '*;', '__;', ';}', ');', '5', ' "";', '};', ';<', '";', ';d']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.133652 | 0.874895    |             0 |
| <       | -2.13365  | 0.118404    |             0 |
| 6       | -5.63365  | 0.00357549  |             0 |
| ;       | -7.50865  | 0.00054832  |             0 |
| >       | -7.63365  | 0.000483891 |             0 |
| <think> | -8.00865  | 0.000332573 |             0 |
| <s      | -8.00865  | 0.000332573 |             0 |
| <span   | -8.44615  | 0.000214725 |             0 |
| 2       | -8.82115  | 0.000147578 |             0 |
| ;<      | -9.25865  | 9.52837e-05 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '**', '<|im_start|>', '.Category', '>', '<|file_sep|>', '.<', '<\\/', '</tool_response>', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', ' <$', '”', '<<<<', '\t  \n', '="<', '_<', ';charset', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Toronto is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', ';</', '»;', '++;', '**;', '4', ';\\', '.;', '_;', ';;', ';$', '%;', '”;', ' {};', ';*', ' [];', '؛', '*;', ';"', '__;', ');', ';}', '6', '};', ' "";', '];', ';<', '.);', '";']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0845762 | 0.918902    |     0.0490755 |
| <       | -2.58458   | 0.075428    |    -0.450924  |
| 6       | -5.70958   | 0.00331408  |    -0.0759244 |
| ;       | -7.83458   | 0.00039581  |    -0.325924  |
| >       | -8.20958   | 0.000272036 |    -0.575925  |
| <s      | -8.20958   | 0.000272036 |    -0.200925  |
| <think> | -8.45958   | 0.000211862 |    -0.450925  |
| <span   | -8.52208   | 0.000199026 |    -0.0759249 |
| 2       | -8.77208   | 0.000155001 |     0.0490751 |
| ;<      | -9.52208   | 7.32175e-05 |    -0.263425  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '<\\/', '</tool_response>', ')', '\\n', ',<', '<<<', '<br', '\\', ' <<<', '!', '<<<<', '”', ' <$', '\t  \n', '="<', ';charset', '_<', ';<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Toronto is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', ';</', '4', '»;', '++;', '**;', ';\\', '_;', '.;', ';;', '%;', ';$', '”;', ' {};', ';*', ' [];', '؛', '*;', ';"', '__;', ');', ';}', '6', ' "";', '};', ';<', '5', '";', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.119281 | 0.887558    |     0.0143706 |
| <       | -2.24428  | 0.106004    |    -0.110629  |
| 6       | -5.61928  | 0.00362725  |     0.0143704 |
| ;       | -7.49428  | 0.000556256 |     0.0143704 |
| >       | -7.61928  | 0.000490895 |     0.0143704 |
| <s      | -8.24428  | 0.000262757 |    -0.235629  |
| <think> | -8.36928  | 0.000231882 |    -0.360629  |
| <span   | -8.55678  | 0.000192237 |    -0.110629  |
| 2       | -8.99428  | 0.000124118 |    -0.173129  |
| ;<      | -9.24428  | 9.66629e-05 |     0.0143709 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '\\', '<<<', '!', ' <<<', ' <$', '<<<<', '\t  \n', '”', '="<', '_<', ';charset', '>>']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Toronto is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', ';</', '4', '»;', '**;', '++;', '_;', ';\\', '.;', ';;', '”;', ';$', '%;', ' {};', ' [];', '؛', '*;', ';*', ';"', '__;', ');', ';}', '6', '};', '5', '";', ' "";', ';<', '];']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.152454 | 0.858599    |    -0.0188019 |
| <       | -2.02745  | 0.13167     |     0.106198  |
| 6       | -5.02745  | 0.00655548  |     0.606198  |
| ;       | -7.52745  | 0.000538107 |    -0.0188017 |
| >       | -7.65245  | 0.000474878 |    -0.0188017 |
| <s      | -8.02745  | 0.000326378 |    -0.0188017 |
| <think> | -8.21495  | 0.000270577 |    -0.206302  |
| <span   | -8.33995  | 0.000238783 |     0.106198  |
| 2       | -8.71495  | 0.000164113 |     0.106198  |
| ;<      | -9.21495  | 9.95398e-05 |     0.0436983 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '**', '<|im_start|>', '.Category', '>', '.<', '<|file_sep|>', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', ' <<<', '<<<', '\\', '”', ' <$', '\t  \n', '<<<<', '```', '>>', '="<', '.;']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[46, 5391, 13674], [6503, 60241]]; reported probabilities cover only first tokens ('O', 'Can'), not the full multi-token answers.
