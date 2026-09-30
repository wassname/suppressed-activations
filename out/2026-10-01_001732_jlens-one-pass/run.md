---
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
country_swap: true
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: false
swap_logits: false
plural: false
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_norm: None
donor_checkpoint: None
donor_reflection: false
equal_donor_norm: false
relation: currency
elapsed_seconds: 10.62
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  euro to  yen. Positive answer_log_odds_shift favours  yen over  euro; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+V(swap(pinv(V)h)-pinv(V)h), V=([W_Italy;W_Japan]*gain @ J[15]).T (block15/output residual16). No column normalization or raw-score exchange in the primary. Unit J and raw plain are separate controls. Random uses one fixed seed0 direction with primary-update norm from its own current state; only prefill doses match. No preliminary current-input pass, donor preparation, sparse decomposition or clean-pass clamp. Not an exact reference reproduction. Clean target prefill follows all five conditions of this property, without feedback. Correct Base and coherent Tokyo AND yen under the same primary rule are required; bare-answer odds alone do not show identity. An article can make first-token metrics nondiagnostic. Inspect whether Base already names Italy; that would limit the hidden-concept claim. Observer is prompt-masked only, not certified speech exclusion. Basis rank and post-cast coordinate errors are recorded. Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 1.0. Concept token strings: (' Italy', ' Japan').

Selection: Fixed Italy-to-Japan capital/currency pair, chosen after failed animal transfer and polar readout. Five conditions per property, one configuration. Earlier trailing-space currency prompt answered100% gold; this exact no-space form was untested. Retain wrong baselines; no prompt or alternate-winner rescue. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  euro toward  yen with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |     p( yen) |   p( euro) |   answer_pair_mass |        r2 |
|:------------------------------|------------------------:|------------:|-----------:|-------------------:|----------:|
| Base                          |             0           | 2.11556e-05 | 0.00139327 |         0.00141442 | 0.0322581 |
| raw J-coordinate exchange     |             0.25        | 2.41695e-05 | 0.00123966 |         0.00126383 | 0.0322581 |
| unit J-coordinate exchange    |             0.1875      | 2.40774e-05 | 0.00131458 |         0.00133866 | 0.0322581 |
| raw plain-coordinate exchange |             4.76837e-07 | 2.11516e-05 | 0.001393   |         0.00141415 | 0.0322581 |
| matched-random delta          |             0           | 2.12205e-05 | 0.00139754 |         0.00141876 | 0.0322581 |

[Base](base/run.md)

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

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

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

[unit J-coordinate exchange](unit-j-coordinate-exchange/run.md)

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

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

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

[matched-random delta](matched-random-delta/run.md)

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
