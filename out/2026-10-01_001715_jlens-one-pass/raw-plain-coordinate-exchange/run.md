---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
country_swap: true
coordinate_kind: raw plain
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
answer_log_odds_shift: 0.12499988079071045
answer_pair_mass: 0.5044295191764832
r2: 0.06451612903225812
---
# raw plain-coordinate exchange

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' London', ' Naples', ' Vienna', ' Barcelona', ' Berlin', ' France', ' Austria', ' Amsterdam', ' Buenos', ' Tokyo', ' Dublin', ' Munich', ' Germany', ' Oslo', 'Italy', ' Spain', ' Bogotá', ' Jakarta', ' Venice', ' Vatican', ' Bangkok', ' Greece', ' Athens', ' Budapest', ' Italian', ' Prague']

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
| Rome    | -0.686256 | 0.503458   |    -0.0208643 |
| Italy   | -1.93626  | 0.144243   |    -0.0208644 |
| Madrid  | -3.06126  | 0.0468288  |     0.104136  |
| in      | -3.24876  | 0.0388225  |     0.0416355 |
| the     | -3.81126  | 0.0221204  |     0.0416355 |
| Spain   | -3.93626  | 0.0195212  |     0.104136  |
| located | -4.37376  | 0.0126038  |    -0.0208645 |
| London  | -4.74876  | 0.00866247 |     0.0416355 |
| not     | -4.93626  | 0.00718144 |     0.0416355 |
| a       | -5.12376  | 0.00595362 |     0.0416355 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', ')**', '）**', '”**', '**', ' **“', ':**', ']**', '’**', '%**', ' **—', '.**', '**-', '。**', '):**', '**—', '*”', ').**', '：“', '软', '-**', '!**', '害', '"><?=', '.:**', '<think>', '”**.']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
