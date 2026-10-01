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
relation: country_properties
elapsed_seconds: 6.07
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Stockholm to Tokyo. Positive answer_log_odds_shift favours first token 'Tok' over 'Stock'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. No previous-donor comparator. Seed0 random matches the new donor norm and direction sign. 9 conditions across fixed development prompts; this call covers one. Concept family, preparation wording and task changes are recorded in the config selection statement. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' Sweden', ' Japan').

Selection: /workspace/2026/suppressed-activations/data/sweden_japan_joint_chat_v1.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Stockholm toward Tokyo with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |   p(first='Tok') |   p(first='Stock') |   first_token_pair_mass |   r2 |
|:---------------------|------------------------:|-----------------:|-------------------:|------------------------:|-----:|
| Base                 |            -1.93715e-07 |      2.81536e-06 |           0.804189 |                0.804191 |    0 |
| role-aligned donor   |            -1.93715e-07 |      2.88326e-06 |           0.823586 |                0.823589 |    0 |
| matched-random delta |            -0.25        |      2.20044e-06 |           0.807063 |                0.807065 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', ' Prague', 'Paris', 'Berlin', ' Budapest', 'Sweden', ' Madrid', ' Munich', ' Zurich', ' Rotterdam', ' Jakarta', ' Minneapolis', ' Lisbon', ' London', ' Bratis', 'Madrid', 'openhagen', 'Barcelona', ' Edinburgh', ' Vienna', ' Barcelona', '瑞典', ' Sweden', ' Paris', ' Frankfurt', ' Bangkok']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Stock   | -0.217921 | 0.804189    |             0 |
| <       | -1.71792  | 0.179439    |             0 |
| Go      | -5.71792  | 0.00328654  |             0 |
| ;       | -5.84292  | 0.00290036  |             0 |
| Os      | -6.21792  | 0.00199338  |             0 |
| St      | -6.40542  | 0.00165257  |             0 |
| O       | -7.21792  | 0.000733325 |             0 |
| Sweden  | -7.40542  | 0.000607948 |             0 |
| <p      | -7.90542  | 0.000368739 |             0 |
| <span   | -8.09292  | 0.000305695 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '<|file_sep|>', '\t  \n', '.Category', ';**', '</tool_response>', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', ' **.**', '.', '</', ';', '.<', ';<', '<\\/', '**', ';</', ',<', ' <<<', '@\\', '<<<<', '="<', './.', '<<<', '\t\n', ' **■', '#/', ' <$']

Coverage: 5 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[role-aligned donor](role-aligned-donor/run.md)

# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', 'Paris', 'Berlin', ' Prague', ' Budapest', 'Sweden', ' Madrid', ' Munich', ' Zurich', ' Jakarta', ' Rotterdam', ' Minneapolis', 'Madrid', ' Bratis', ' London', ' Lisbon', 'Barcelona', ' Vienna', '瑞典', 'openhagen', ' Sweden', ' Edinburgh', ' Barcelona', ' Paris', ' Bangkok', ' Riyadh']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Stock   | -0.194088 | 0.823586    |     0.0238338 |
| <       | -1.81909  | 0.162174    |    -0.101166  |
| Go      | -5.81909  | 0.00297031  |    -0.101166  |
| ;       | -6.06909  | 0.00231328  |    -0.226166  |
| Os      | -6.31909  | 0.00180159  |    -0.101166  |
| St      | -6.63159  | 0.00131807  |    -0.226166  |
| O       | -7.25659  | 0.000705511 |    -0.0386662 |
| Sweden  | -7.44409  | 0.00058489  |    -0.0386662 |
| <p      | -8.13159  | 0.000294101 |    -0.226167  |
| <span   | -8.25659  | 0.000259543 |    -0.163667  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<|im_start|>', '<think>', '<|file_sep|>', '\t  \n', ';**', '.Category', '</tool_response>', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', ' **.**', '.', '</', ';', '.<', ';<', '<\\/', '**', ',<', ' <<<', ';</', '@\\', '<<<<', '="<', './.', '<<<', '\t\n', ' **■', '#/', ' <$']

Coverage: 5 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Tokyo', 'JPY']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Gothenburg, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Stockholm', ' Oslo', ' Helsinki', ' Copenhagen', ' Amsterdam', ' Berlin', 'London', 'Berlin', 'Paris', ' Prague', ' Budapest', 'Sweden', ' Madrid', ' Munich', ' Zurich', ' Rotterdam', ' Minneapolis', ' Jakarta', ' Lisbon', 'Madrid', ' Bratis', ' London', 'openhagen', 'Barcelona', ' Edinburgh', ' Vienna', ' Barcelona', '瑞典', ' Sweden', ' Paris', ' Frankfurt', ' Bangkok']

Generation (5 tokens):
```text
Stockholm; SEK<|im_end|>
```

| token     |     log p |           p |   delta log p |
|:----------|----------:|------------:|--------------:|
| Stock     | -0.214353 | 0.807063    |    0.00356829 |
| <         | -1.71435  | 0.18008     |    0.00356829 |
| Go        | -5.83935  | 0.00291072  |   -0.121432   |
| ;         | -6.08935  | 0.00226687  |   -0.246432   |
| St        | -6.58935  | 0.00137493  |   -0.183932   |
| Os        | -6.65185  | 0.00129163  |   -0.433932   |
| Sweden    | -7.58935  | 0.000505808 |   -0.183932   |
| O         | -7.77685  | 0.00041933  |   -0.558932   |
| <p        | -8.15185  | 0.000288201 |   -0.246432   |
| Stockholm | -8.33935  | 0.000238927 |   -0.183932   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '<|im_start|>', '<|file_sep|>', '\t  \n', '.Category', '</tool_response>', ';**', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '  \n', ' **.**', '</', '.', '<\\/', ';', ';<', '.<', '**', ' <<<', ',<', ';</', '@\\', '="<', '<<<<', './.', '<<<', ' **■', '\t\n', '#/', ' <$']

Coverage: 5 calls; prompt slice -1:, then one position per decode.

Expected properties: ['Stockholm', 'SEK']. Answer label tokenizations: [[18782, 32393], [51076, 15560]]; reported probabilities cover only first tokens ('Stock', 'Tok'), not the full multi-token answers.
