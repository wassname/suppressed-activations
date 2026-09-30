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
expected_answer: 'control'
n_tokens: 32
answer_0: ' Rome'
answer_1: ' Tokyo'
answer_log_odds_shift: -0.06250011920928955
answer_pair_mass: 0.5121744871139526
r2: 0.06451612903225812
---
# matched-random delta

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' Naples', ' London', ' Vienna', ' Barcelona', ' France', ' Austria', ' Berlin', ' Buenos', ' Amsterdam', ' Dublin', ' Tokyo', 'Italy', ' Munich', ' Germany', ' Spain', ' Oslo', ' Venice', ' Bogotá', ' Vatican', ' Italian', ' Greece', ' Athens', ' Jakarta', ' Bangkok', ' Prague', ' Switzerland']

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
| Rome    | -0.670689 | 0.511356   |   -0.00529742 |
| Italy   | -1.85819  | 0.155955   |    0.0572026  |
| Madrid  | -3.17069  | 0.0419747  |   -0.00529766 |
| in      | -3.35819  | 0.0347982  |   -0.0677977  |
| the     | -3.85819  | 0.0211062  |   -0.00529766 |
| Spain   | -3.98319  | 0.0186261  |    0.0572023  |
| located | -4.35819  | 0.0128015  |   -0.00529766 |
| London  | -4.79569  | 0.0082653  |   -0.00529766 |
| not     | -4.98319  | 0.00685218 |   -0.00529766 |
| a       | -5.17069  | 0.00568065 |   -0.00529766 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', '”**', ')**', '）**', '**', ' **“', ':**', ']**', '’**', '%**', ' **—', '.**', '):**', '**-', '。**', '**—', '!**', '软', '：“', '*”', ').**', '-**', '.:**', '害', '"><?=', '”**.', '“This']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
