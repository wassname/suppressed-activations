---
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
reverse: true
swap_logits: false
plural: false
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_132306_jlens-one-pass/donors.pt
donor_reflection: false
equal_donor_norm: false
relation: arithmetic_control
elapsed_seconds: 5.08
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours 4 over 8; arithmetic should preserve4, not maximize a shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. Previous literal-name donor retains its own norm; seed0 random matches the new donor norm and direction sign. Twelve conditions across three fixed development prompts; this call covers one. Both task frame and donor preparation changed. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for Base, both donors and matched random; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition                   |   answer_log_odds_shift |     p(4) |        p(8) |   answer_pair_mass |   r2 |
|:----------------------------|------------------------:|---------:|------------:|-------------------:|-----:|
| Base                        |                  0      | 0.824837 | 1.37762e-05 |           0.824851 |    0 |
| role-aligned donor          |                 -0.3125 | 0.784508 | 1.79092e-05 |           0.784526 |    0 |
| previous literal-name donor |                 -0.375  | 0.763313 | 1.85491e-05 |           0.763331 |    0 |
| matched-random delta        |                 -0.25   | 0.805617 | 1.72768e-05 |           0.805634 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '>;', '++;', ';</', '»;', ';$', '_;', ';\\', '4', '**;', '”;', '%;', '.;', ' {};', '__;', ';;', ' [];', '*;', ';"', ';*', ' "";', '`;', '";', '؛', ');', '};', '];', ';d', ';}', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |    log p |           p |   delta log p |
|:--------|---------:|------------:|--------------:|
| 4       | -0.19257 | 0.824837    |             0 |
| <       | -1.81757 | 0.16242     |             0 |
| 6       | -5.06757 | 0.00629771  |             0 |
| <s      | -6.56757 | 0.00140521  |             0 |
| ;       | -6.69257 | 0.00124009  |             0 |
| >       | -6.94257 | 0.000965785 |             0 |
| <span   | -7.81757 | 0.000402599 |             0 |
| <think> | -8.31757 | 0.000244189 |             0 |
| ;<      | -8.50507 | 0.000202439 |             0 |
| 2       | -8.94257 | 0.000130705 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '<\\/', '</tool_response>', ')', '\\n', ',<', ' <<<', '<br', '!', ' <$', '\\', '<<<', '”', '<<<<', '"', '<-', '\t  \n', 'itarian', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[role-aligned donor](role-aligned-donor/run.md)

# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '>;', ';</', '++;', '»;', ';\\', ';$', '4', '_;', '”;', '**;', '.;', '%;', ';;', ' {};', ' [];', '__;', ';"', '*;', '`;', '";', ' "";', ';*', '؛', ');', '};', '];', ';}', ';d', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.242699 | 0.784508    |    -0.0501291 |
| <       | -1.6177   | 0.198355    |     0.199871  |
| 6       | -4.6177   | 0.0098755   |     0.449871  |
| <s      | -6.4927   | 0.00151446  |     0.0748711 |
| ;       | -6.4927   | 0.00151446  |     0.199871  |
| >       | -6.7427   | 0.00117946  |     0.199871  |
| <span   | -7.8052   | 0.00040761  |     0.0123711 |
| <think> | -8.1177   | 0.000298214 |     0.199871  |
| ;<      | -8.4927   | 0.000204959 |     0.0123711 |
| 2       | -8.8677   | 0.000140866 |     0.0748711 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '<\\/', '</tool_response>', ')', '\\n', '!', ',<', '\\', '<br', ' <<<', '<<<', '”', ' <$', '<<<<', '"', 'itarian', '\t  \n', '<-', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[previous literal-name donor](previous-literal-name-donor/run.md)

# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '>;', ';</', '4', '»;', '++;', ';$', ';\\', '_;', '”;', '**;', '%;', '.;', ';;', '__;', ' {};', ';"', ' [];', '*;', ';*', '";', '`;', ' "";', '؛', '6', ');', ';d', ';}', '];', '};']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.270087 | 0.763313    |    -0.0775176 |
| <       | -1.52009  | 0.218693    |     0.297482  |
| 6       | -4.64509  | 0.00960869  |     0.422482  |
| <s      | -6.27009  | 0.00189206  |     0.297482  |
| ;       | -6.39509  | 0.00166974  |     0.297482  |
| >       | -6.64509  | 0.0013004   |     0.297482  |
| <span   | -7.52009  | 0.000542085 |     0.297482  |
| <think> | -8.08259  | 0.000308871 |     0.234982  |
| ;<      | -8.27009  | 0.000256063 |     0.234982  |
| 2       | -8.89509  | 0.000137061 |     0.0474825 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '**', '<|im_start|>', '<', '.Category', '>', '<|file_sep|>', '.<', ')', '</tool_response>', '<\\/', '\\n', '!', '<br', '\\', ',<', ' <<<', '<<<', '”', ' <$', '\t  \n', '<<<<', '"', 'itarian', ';charset', '<-']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nAn animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '；', '>;', ';</', '++;', '»;', '_;', ';$', '**;', ';\\', '”;', '%;', '4', '.;', ' {};', '__;', ' [];', ';;', '*;', ';"', ';*', '`;', ');', ' "";', '";', '؛', '};', '];', ';}', ';d', ' ;']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| 4       | -0.216147 | 0.805617    |    -0.0235776 |
| <       | -1.71615  | 0.179757    |     0.101422  |
| 6       | -4.84115  | 0.00789799  |     0.226422  |
| <s      | -6.59115  | 0.00137246  |    -0.0235777 |
| ;       | -6.59115  | 0.00137246  |     0.101422  |
| >       | -6.96615  | 0.00094328  |    -0.0235777 |
| <span   | -7.71615  | 0.000445574 |     0.101422  |
| <think> | -8.34115  | 0.000238499 |    -0.0235777 |
| ;<      | -8.52865  | 0.000197722 |    -0.0235777 |
| 2       | -8.84115  | 0.000144657 |     0.101422  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', '<think>', ';', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', ')', '<\\/', '\\n', ',<', '!', ' <<<', '\\', '<br', ' <$', '”', '<<<', '"', '<<<<', '\t  \n', '<-', 'itarian', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.
