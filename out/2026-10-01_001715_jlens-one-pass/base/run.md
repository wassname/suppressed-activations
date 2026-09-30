---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
country_swap: true
coordinate_kind: raw J
reverse: false
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: None
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: capital
expected_answer: ' Rome'
n_tokens: 32
answer_0: ' Rome'
answer_1: ' Tokyo'
answer_log_odds_shift: -1.1920928955078125e-07
answer_pair_mass: 0.5149480104446411
r2: 0.06451612903225812
---
# Base

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' Naples', ' London', ' Vienna', ' Barcelona', ' France', ' Berlin', ' Austria', ' Buenos', ' Amsterdam', ' Dublin', ' Tokyo', ' Munich', 'Italy', ' Germany', ' Oslo', ' Spain', ' Bogotá', ' Venice', ' Vatican', ' Italian', ' Jakarta', ' Greece', ' Bangkok', ' Athens', ' Prague', ' Switzerland']

Generation (32 tokens):
```text
 Rome.
Hypothesis: The capital of the country shaped like a boot is not Rome.
Is the hypothesis true or false?

<think>

</think>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| Rome    | -0.665392 | 0.514072   |             0 |
| Italy   | -1.91539  | 0.147284   |             0 |
| Madrid  | -3.16539  | 0.0421976  |             0 |
| in      | -3.29039  | 0.0372393  |             0 |
| the     | -3.85289  | 0.0212183  |             0 |
| Spain   | -4.04039  | 0.0175906  |             0 |
| located | -4.35289  | 0.0128695  |             0 |
| London  | -4.79039  | 0.0083092  |             0 |
| not     | -4.97789  | 0.00688857 |             0 |
| a       | -5.16539  | 0.00571083 |             0 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', ')**', '）**', '”**', '**', ' **“', ']**', ':**', '’**', '%**', ' **—', '.**', '**-', '。**', '):**', '**—', '*”', ').**', '软', '：“', '!**', '-**', '害', '.:**', '"><?=', '<think>', '”**.']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
