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
relation: currency
expected_answer: ' yen'
n_tokens: 32
answer_0: ' euro'
answer_1: ' yen'
answer_log_odds_shift: 0.1875
answer_pair_mass: 0.0013386572245508432
r2: 0.032258064516129004
---
# unit J-coordinate exchange

Input:
```text
'Fact: The currency used in the country shaped like a boot is'
```

Prefill readout: [' euros', ' Dollars', ' Euros', ' dollars', ' USD', ' Dollar', '欧元', ' euro', '英镑', ' Bitcoin', ' called', ' Euro', ' dollar', ' currencies', ' EUR', ' dolar', '人民币', ' Italy', 'USD', ' **€', '货币', 'euros', '-dollar', 'Bitcoin', '美元', ' GBP', ' bitcoin', '叫做', ' Bitcoins', ' ($)', ' Peso', ' Germany']

Generation (32 tokens):
```text
 the Euro.
Hypothesis: The currency used in the country shaped like a boot is the Dollar.
Is the hypothesis true or false?

<think>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| the     | -0.196738 | 0.821406   |    0.00436579 |
| called  | -3.63424  | 0.026404   |    0.00436592 |
| a       | -4.32174  | 0.0132768  |    0.00436592 |
| Euro    | -4.44674  | 0.0117167  |   -0.0581341  |
| not     | -4.57174  | 0.01034    |    0.00436592 |
|         | -4.75924  | 0.00857214 |    0.00436592 |
| known   | -5.32174  | 0.00488426 |    0.00436592 |
| Euros   | -5.63424  | 0.0035734  |   -0.120634   |
| used    | -5.69674  | 0.0033569  |   -0.0581341  |
| in      | -5.82174  | 0.00296245 |   -0.0581341  |

Final-decode readout: [' Options', 'Options', ' options', '<think>', ' Choices', ' OPTIONS', '-options', 'OPTIONS', 'options', '选项', 'Choices', '_options', '**', ' choices', ' Answer', '"**', ' Option', ';**', ' **', '.**', ' option', '.Options', ' Answers', ' **【', ' Logic', 'Option', '.options', '。**', ' opciones', 'Answer', ')**', ' Choice']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
