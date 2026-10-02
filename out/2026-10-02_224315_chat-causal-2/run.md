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
elapsed_seconds: 4.73
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Asia' over 'Europe'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' France', ' India') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' France', ' India').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v2_continent/france_india_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Asia') |   p(first='Europe') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|------------------:|--------------------:|------------------------:|-----:|
| Base                          |                0        |       1.51859e-09 |         1.48653e-08 |             1.63839e-08 |    0 |
| raw J-coordinate exchange     |                0.75     |       2.35345e-09 |         1.08822e-08 |             1.32357e-08 |    0 |
| raw plain-coordinate exchange |                0.046875 |       1.785e-09   |         1.6673e-08  |             1.8458e-08  |    0 |
| matched-random delta          |               -0.03125  |       1.59798e-09 |         1.6139e-08  |             1.7737e-08  |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Lyon asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', ';</', '**;', '++;', '4', '_;', '.;', ';\\', ';;', '%;', '”;', '*;', '__;', ' [];', ' {};', '؛', ';$', ';*', ');', ';"', ' "";', '6', '";', ';<', '};', '];', ';.', ';}']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0867368 | 0.916918    |             0 |
| <       | -2.58674   | 0.0752653   |             0 |
| 6       | -5.46174   | 0.00424618  |             0 |
| ;       | -6.83674   | 0.0010736   |             0 |
| 2       | -7.83674   | 0.000394956 |             0 |
| <s      | -7.96174   | 0.000348547 |             0 |
| >       | -8.14924   | 0.000288956 |             0 |
| <think> | -8.39924   | 0.000225039 |             0 |
| <span   | -8.64924   | 0.000175261 |             0 |
| ;<      | -9.02424   | 0.000120455 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', '.<', ')', '<\\/', '\\n', '!', '”', '\t  \n', ';.', ';charset', ',<', '<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '.;', '\\', 'itarian', ' -->', '<br', '<<<<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Lyon asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', ';</', '**;', '++;', '_;', '.;', '4', ';\\', '%;', ';;', '”;', '*;', '__;', ' [];', '؛', ' {};', ';*', ';$', ');', ';"', ' "";', ';<', '";', '6', '};', '];', ';.', ';}']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0861347 | 0.917471    |   0.000602014 |
| <       | -2.58613   | 0.0753106   |   0.000602007 |
| 6       | -5.71113   | 0.00330892  |  -0.249398    |
| ;       | -6.58613   | 0.00137936  |   0.250602    |
| <s      | -7.83613   | 0.000395194 |   0.125602    |
| >       | -7.96113   | 0.000348757 |   0.188102    |
| 2       | -8.08613   | 0.000307777 |  -0.249398    |
| <think> | -8.52363   | 0.000198716 |  -0.124398    |
| <span   | -8.64863   | 0.000175366 |   0.000601768 |
| ;<      | -8.77363   | 0.00015476  |   0.250602    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', ')', '<\\/', '.<', '\\n', '!', '\t  \n', '”', ';.', ';charset', ',<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<', '.;', '\\', '<br', ' -->', 'itarian', '```']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Lyon asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', ';</', '**;', '++;', '4', '_;', '.;', ';\\', ';;', '%;', '”;', '*;', ' [];', '__;', '؛', ' {};', ';$', ';*', ');', ';"', ' "";', ';<', '6', '";', '};', '];', ';.', ';}']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0969742 | 0.907579    |    -0.0102374 |
| <       | -2.47197   | 0.084418    |     0.114763  |
| 6       | -5.47197   | 0.00420293  |    -0.0102377 |
| ;       | -6.72197   | 0.00120416  |     0.114762  |
| 2       | -7.97197   | 0.000344997 |    -0.135238  |
| <s      | -7.97197   | 0.000344997 |    -0.0102377 |
| >       | -8.03447   | 0.000324095 |     0.114762  |
| <think> | -8.34697   | 0.000237113 |     0.0522623 |
| <span   | -8.53447   | 0.000196573 |     0.114762  |
| ;<      | -8.90947   | 0.000135103 |     0.114762  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', '.<', ')', '<\\/', '\\n', '!', ';.', '\t  \n', '”', ';charset', '.;', ',<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<', '\\', 'itarian', ' -->', '<br', '<<<<']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nSomeone from Lyon asks: what is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '»;', '**;', ';</', '++;', '.;', '_;', '4', ';\\', ';;', '”;', '%;', '*;', ' [];', '__;', '؛', ' {};', ';*', ';$', ');', ';"', ' "";', '";', ';<', '6', '};', '];', ';.', ';}']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0982746 | 0.9064      |    -0.0115378 |
| <       | -2.47327   | 0.0843083   |     0.113462  |
| 6       | -5.22327   | 0.00538965  |     0.238462  |
| ;       | -6.72327   | 0.00120259  |     0.113462  |
| <s      | -7.72327   | 0.000442409 |     0.238462  |
| 2       | -8.03577   | 0.000323674 |    -0.199038  |
| >       | -8.03577   | 0.000323674 |     0.113462  |
| <think> | -8.53577   | 0.000196318 |    -0.136538  |
| <span   | -8.53577   | 0.000196318 |     0.113462  |
| ;<      | -8.91077   | 0.000134927 |     0.113462  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '<think>', '</', '<|im_start|>', '.Category', '**', '<|file_sep|>', '<', '>', '</tool_response>', '.<', ')', '<\\/', '\\n', '!', ';.', '\t  \n', '”', '.;', ';charset', ',<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '<<<', '\\', '```', ' -->', 'itarian', '。']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[29774], [37186]]; reported probabilities cover only first tokens ('Europe', 'Asia'), not the full multi-token answers.
