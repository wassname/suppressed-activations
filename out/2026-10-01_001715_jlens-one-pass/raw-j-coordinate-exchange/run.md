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
expected_answer: ' Tokyo'
n_tokens: 32
answer_0: ' Rome'
answer_1: ' Tokyo'
answer_log_odds_shift: 0.06249988079071045
answer_pair_mass: 0.5119014382362366
r2: 0.06451612903225812
---
# raw J-coordinate exchange

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' Naples', ' London', ' Vienna', ' Barcelona', ' Berlin', ' France', ' Austria', ' Buenos', ' Amsterdam', ' Tokyo', ' Dublin', ' Munich', ' Oslo', ' Germany', 'Italy', ' Spain', ' Jakarta', ' Bogotá', ' Venice', ' Bangkok', ' Vatican', ' Greece', ' Athens', ' Italian', ' Prague', ' Switzerland']

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
| Rome    | -0.671435 | 0.510975   |   -0.00604349 |
| Italy   | -1.92144  | 0.146397   |   -0.00604355 |
| Madrid  | -3.10894  | 0.0446485  |    0.0564563  |
| in      | -3.29644  | 0.0370149  |   -0.00604367 |
| the     | -3.85894  | 0.0210904  |   -0.00604367 |
| Spain   | -3.98394  | 0.0186123  |    0.0564563  |
| located | -4.35893  | 0.012792   |   -0.00604343 |
| London  | -4.73393  | 0.00879181 |    0.0564566  |
| not     | -4.92143  | 0.00728867 |    0.0564566  |
| a       | -5.17143  | 0.00567642 |   -0.00604343 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', '”**', '）**', ')**', '**', ':**', ' **“', '%**', ']**', '’**', ' **—', '.**', '。**', '**-', '):**', '*”', '软', '**—', ').**', '.:**', '-**', '!**', '害', '<think>', ':*', '：“', '"><?=']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
