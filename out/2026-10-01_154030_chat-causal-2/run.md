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
reverse: false
swap_logits: false
plural: false
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
donor_reflection: false
equal_donor_norm: false
relation: arithmetic_control
elapsed_seconds: 4.32
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; arithmetic should preserve4, not maximize a shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. No previous-donor comparator. Seed0 random matches the new donor norm and direction sign. 9 conditions across fixed development prompts; this call covers one. Concept family, preparation wording and task changes are recorded in the config selection statement. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v1.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 and even for every condition; inspect the full continuation.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:---------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                 |                 0       |      2.57153e-10 |        4.92854e-09 |             5.18569e-09 |    0 |
| role-aligned donor   |                 0.03125 |      2.41627e-10 |        4.48849e-09 |             4.73011e-09 |    0 |
| matched-random delta |                -0.125   |      2.27009e-10 |        4.9301e-09  |             5.15711e-09 |    0 |

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

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[role-aligned donor](role-aligned-donor/run.md)

# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', ';', '>;', '；', '4', '++;', '»;', ';</', ';\\', '_;', '**;', '.;', '”;', ';$', ';;', ' {};', '%;', ' [];', ';*', '*;', '__;', '؛', ';"', ');', '6', ';}', ' "";', '5', '";', '};', '`;', ';)']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0655009 | 0.936598    |   0.000222273 |
| <       | -2.8155    | 0.0598747   |   0.000222206 |
| 6       | -6.6905    | 0.00124266  |  -0.124777    |
| >       | -7.6905    | 0.000457149 |   0.000222683 |
| ;       | -7.8155    | 0.000403433 |  -0.124777    |
| <think> | -8.4405    | 0.000215942 |  -0.124778    |
| <s      | -8.5655    | 0.000190568 |   0.000222206 |
| <span   | -8.8155    | 0.000148415 |   0.125222    |
| 2       | -8.878     | 0.000139423 |   0.0627222   |
| ;<      | -9.8155    | 5.45987e-05 |   0.000222206 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', '</', ';', '<think>', '<|im_start|>', '<', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '!', '\\', '<br', '<<<', ' <<<', '<<<<', '”', '\t  \n', ' <$', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '_<', '>>', '.;']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nA visitor from Gothenburg is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '>;', ';', '4', '；', '++;', ';</', '»;', ';\\', '_;', ';$', '**;', '.;', '”;', ';;', ' {};', '%;', ';*', '6', ' [];', '؛', '__;', ';"', '*;', ' "";', '5', ');', ';}', '";', ';d', '`;', '};']

Generation (4 tokens):
```text
4; even<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0654075 | 0.936686    |   0.000315726 |
| <       | -2.81541   | 0.0598803   |   0.000315666 |
| 6       | -6.81541   | 0.00109675  |  -0.249684    |
| >       | -7.69041   | 0.000457192 |   0.000316143 |
| ;       | -7.81541   | 0.00040347  |  -0.124684    |
| <think> | -8.19041   | 0.000277301 |   0.125316    |
| <s      | -8.44041   | 0.000215962 |   0.125316    |
| <span   | -8.94041   | 0.000130988 |   0.000315666 |
| 2       | -9.00291   | 0.000123051 |  -0.0621843   |
| ;<      | -9.81541   | 5.46038e-05 |   0.000315666 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '.', ';', '</', '<think>', '<', '<|im_start|>', '**', '.Category', '>', '<|file_sep|>', '.<', '</tool_response>', '<\\/', ')', '\\n', ',<', '<br', '!', '\\', '<<<', ' <<<', '”', '<<<<', '\t  \n', '.;', ' <$', ';charset', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

Expected properties: ['4', 'even']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.
