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
expected_answer: 'control'
n_tokens: 32
answer_0: ' euro'
answer_1: ' yen'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.0014187562046572566
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
'Fact: The currency used in the country shaped like a boot is'
```

Prefill readout: [' euros', ' Euros', ' Dollars', ' dollars', ' USD', '欧元', ' Dollar', ' euro', '英镑', ' Bitcoin', ' Euro', ' called', ' currencies', ' dollar', ' EUR', ' Italy', ' dolar', '人民币', 'USD', ' **€', '货币', 'euros', '-dollar', 'Bitcoin', '美元', ' GBP', ' bitcoin', '叫做', ' Peso', ' Bitcoins', ' France', ' Germany']

Generation (32 tokens):
```text
 the Euro.
Hypothesis: The currency used in the country shaped like a boot is the Dollar.
Is the hypothesis true or false?

<think>
```

| token   |     log p |          p |   delta log p |
|:--------|----------:|-----------:|--------------:|
| the     | -0.198045 | 0.820333   |    0.00305922 |
| called  | -3.63554  | 0.0263696  |    0.00305939 |
| a       | -4.38554  | 0.0124561  |   -0.0594406  |
| Euro    | -4.38554  | 0.0124561  |    0.00305939 |
| not     | -4.63554  | 0.00970082 |   -0.0594406  |
|         | -4.76054  | 0.00856094 |    0.00305939 |
| known   | -5.32304  | 0.00487788 |    0.00305939 |
| Euros   | -5.51054  | 0.0040439  |    0.00305939 |
| used    | -5.63554  | 0.00356873 |    0.00305939 |
| Italy   | -5.63554  | 0.00356873 |    0.0655594  |

Final-decode readout: [' Options', 'Options', ' options', '<think>', ' Choices', ' OPTIONS', 'OPTIONS', '-options', 'options', '选项', '**', 'Choices', '_options', ' Answer', ' choices', '"**', ' **', ' Option', '.**', ' Answers', ' **【', ';**', '。**', '.Options', ' Logic', ' option', 'Option', 'Answer', ')**', '.options', '-**', ' opciones']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
