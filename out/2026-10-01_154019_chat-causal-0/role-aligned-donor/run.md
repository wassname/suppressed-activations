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
expected_answer: 'Tokyo'
n_tokens: 5
answer_0: 'Stockholm'
answer_1: 'Tokyo'
answer_log_odds_shift: -1.9371509552001953e-07
answer_pair_mass: 0.8235886096954346
r2: 0.0
---
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

Written by PI/OpenAI.
