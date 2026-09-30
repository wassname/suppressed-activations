---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
country_swap: true
coordinate_kind: unit J
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
answer_pair_mass: 0.5123987793922424
r2: 0.06451612903225812
---
# unit J-coordinate exchange

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' London', ' Naples', ' Vienna', ' Barcelona', ' Berlin', ' France', ' Austria', ' Buenos', ' Tokyo', ' Amsterdam', ' Dublin', ' Munich', ' Oslo', 'Italy', ' Germany', ' Spain', ' Bogotá', ' Jakarta', ' Venice', ' Bangkok', ' Athens', ' Vatican', ' Greece', ' Budapest', ' Italian', ' Prague']

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
| Rome    | -0.670464 | 0.511471   |   -0.00507241 |
| Italy   | -1.92046  | 0.146539   |   -0.00507247 |
| Madrid  | -3.10796  | 0.0446919  |    0.0574274  |
| in      | -3.29546  | 0.0370508  |   -0.00507259 |
| the     | -3.85796  | 0.0211109  |   -0.00507259 |
| Spain   | -3.98296  | 0.0186303  |    0.0574274  |
| located | -4.35796  | 0.0128044  |   -0.00507259 |
| London  | -4.73296  | 0.00880035 |    0.0574274  |
| not     | -4.98296  | 0.00685372 |   -0.00507259 |
| a       | -5.17046  | 0.00568193 |   -0.00507259 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', '”**', '）**', ')**', '**', ':**', ' **“', '%**', ']**', '’**', ' **—', '.**', '。**', '**-', '):**', '*”', '软', '**—', ').**', '.:**', '-**', '害', '!**', '<think>', '：“', ':*', '"><?=']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
