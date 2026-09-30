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
relation: currency
expected_answer: ' yen'
n_tokens: 32
answer_0: ' euro'
answer_1: ' yen'
answer_log_odds_shift: 4.76837158203125e-07
answer_pair_mass: 0.0014141533756628633
r2: 0.032258064516129004
---
# raw plain-coordinate exchange

Input:
```text
'Fact: The currency used in the country shaped like a boot is'
```

Prefill readout: [' euros', ' Dollars', ' Euros', ' dollars', ' USD', ' Dollar', '欧元', ' euro', '英镑', ' Bitcoin', ' Euro', ' called', ' currencies', ' EUR', ' dollar', ' dolar', ' Italy', '人民币', 'USD', ' **€', '货币', 'euros', '-dollar', 'Bitcoin', '美元', ' GBP', ' bitcoin', '叫做', ' Germany', ' Bitcoins', ' Peso', ' ($)']

Generation (32 tokens):
```text
 the Euro.
Hypothesis: The currency used in the country shaped like a boot is the Dollar.
Is the hypothesis true or false?

<think>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| the     | -0.201294 | 0.817672   |  -0.000190377 |
| called  | -3.63879  | 0.026284   |  -0.000190258 |
| a       | -4.32629  | 0.0132164  |  -0.000190258 |
| Euro    | -4.38879  | 0.0124157  |  -0.000190258 |
| not     | -4.57629  | 0.010293   |  -0.000190258 |
|         | -4.76379  | 0.00853317 |  -0.000190258 |
| known   | -5.32629  | 0.00486205 |  -0.000190258 |
| Euros   | -5.51379  | 0.00403078 |  -0.000190258 |
| used    | -5.63879  | 0.00355715 |  -0.000190258 |
| Italy   | -5.70129  | 0.00334164 |  -0.000190258 |

Final-decode readout: [' Options', 'Options', ' options', ' Choices', '<think>', ' OPTIONS', 'OPTIONS', '-options', 'options', '选项', 'Choices', '_options', '**', ' choices', ' Answer', '"**', ' Option', ' Answers', ' **', ';**', '.**', '.Options', ' **【', ' option', ' Logic', 'Option', '.options', ' opciones', '。**', 'Answer', ')**', ' Choice']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
