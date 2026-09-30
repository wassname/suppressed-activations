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
expected_answer: ' euro'
n_tokens: 32
answer_0: ' euro'
answer_1: ' yen'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.0014144224114716053
r2: 0.032258064516129004
---
# Base

Input:
```text
'Fact: The currency used in the country shaped like a boot is'
```

Prefill readout: [' euros', ' Euros', ' Dollars', ' dollars', ' USD', '欧元', ' Dollar', ' euro', '英镑', ' Bitcoin', ' Euro', ' called', ' EUR', ' currencies', ' dollar', ' Italy', ' dolar', '人民币', 'USD', ' **€', '货币', 'euros', '-dollar', 'Bitcoin', '美元', ' GBP', ' bitcoin', '叫做', ' Peso', ' Bitcoins', ' Germany', ' France']

Generation (32 tokens):
```text
 the Euro.
Hypothesis: The currency used in the country shaped like a boot is the Dollar.
Is the hypothesis true or false?

<think>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| the     | -0.201104 | 0.817827   |             0 |
| called  | -3.6386   | 0.026289   |             0 |
| a       | -4.3261   | 0.0132189  |             0 |
| Euro    | -4.3886   | 0.0124181  |             0 |
| not     | -4.5761   | 0.0102949  |             0 |
|         | -4.7636   | 0.00853479 |             0 |
| known   | -5.3261   | 0.00486298 |             0 |
| Euros   | -5.5136   | 0.00403155 |             0 |
| used    | -5.6386   | 0.00355783 |             0 |
| Italy   | -5.7011   | 0.00334227 |             0 |

Final-decode readout: [' Options', 'Options', ' options', ' Choices', '<think>', ' OPTIONS', 'OPTIONS', '选项', 'options', '-options', 'Choices', '_options', '**', ' choices', ' Answer', '"**', ' Option', ' Answers', ' **', ' **【', ';**', '.Options', '.**', ' option', 'Option', ' Logic', '.options', '。**', ' opciones', 'Answer', ')**', ' Choice']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
