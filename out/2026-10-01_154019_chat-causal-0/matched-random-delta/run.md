---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: false
country_swap: false
coordinate_kind: None
reverse: false
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
vjp_checkpoint: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: country_properties
expected_answer: 'control'
n_tokens: 5
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: -0.2500001788139343
answer_pair_mass: 0.807065486907959
r2: 0.0
---
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

Written by PI/OpenAI.
