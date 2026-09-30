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
relation: currency
expected_answer: ' yen'
n_tokens: 32
answer_0: ' euro'
answer_1: ' yen'
answer_log_odds_shift: 0.25
answer_pair_mass: 0.0012638262705877423
r2: 0.032258064516129004
---
# raw J-coordinate exchange

Input:
```text
'Fact: The currency used in the country shaped like a boot is'
```

Prefill readout: [' euros', ' Dollars', ' dollars', ' Euros', ' USD', ' Dollar', '欧元', ' euro', '英镑', ' Bitcoin', ' Euro', ' called', ' dollar', ' currencies', ' dolar', ' EUR', '人民币', ' Italy', 'USD', '货币', ' **€', '-dollar', 'euros', 'Bitcoin', '美元', ' GBP', ' bitcoin', '叫做', ' Bitcoins', ' Peso', ' Germany', ' ($)']

Generation (32 tokens):
```text
 the Euro.
Hypothesis: The currency used in the country shaped like a boot is the Dollar.
Is the hypothesis true or false?

<think>
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| the     | -0.19292 | 0.824548   |    0.00818358 |
| called  | -3.63042 | 0.026505   |    0.00818372 |
| a       | -4.38042 | 0.0125201  |   -0.0543165  |
| Euro    | -4.50542 | 0.0110489  |   -0.116817   |
| not     | -4.56792 | 0.0103795  |    0.00818348 |
|         | -4.81792 | 0.00808358 |   -0.0543165  |
| known   | -5.31792 | 0.00490294 |    0.00818348 |
| Euros   | -5.63042 | 0.00358707 |   -0.116817   |
| used    | -5.75542 | 0.00316557 |   -0.116817   |
| Italy   | -5.75542 | 0.00316557 |   -0.0543165  |

Final-decode readout: [' Options', 'Options', ' options', ' Choices', '<think>', ' OPTIONS', '-options', 'OPTIONS', 'options', '选项', 'Choices', '_options', '**', ' choices', ' Answer', ' Option', '"**', ' **', ';**', '.Options', ' option', ' Answers', ' Logic', 'Option', '.**', ' **【', '.options', ' opciones', '。**', ')**', ' Choice', 'Answer']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
