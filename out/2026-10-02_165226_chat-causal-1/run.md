---
raw_coordinate_exchange: true
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
vjp_checkpoint: None
indirect_donor: false
country_swap: false
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: false
prompt_slice: '0:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: None
donor_reflection: false
equal_donor_norm: false
relation: country_properties
elapsed_seconds: 5.38
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is Brasília to Berlin. Positive answer_log_odds_shift favours first token 'Br' over 'Berlin'; reverse success has a negative shift. Probabilities/log odds cover first tokens only, not full multi-token answers. Joint properties and parity are assessed from complete text; capital-token mass is not an arithmetic coherence measure. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+scale*V(swap(pinv(V)h)-pinv(V)h). V uses the fixed (' Germany', ' Brazil') embedding rows, final norm gain and J[15]; no column normalization. Raw plain exchange and one fixed GPU-float32 seed0 random direction are controls. Random matches the primary formula's requested update norm on its own current state, not later primary states or realized BF16 norms. No donor forward, current-input preparation, backward, later-layer feedback or post-condition target prefill. The same symmetric operator is used in both directions and arithmetic, with prefill scale1 and decode0.25. Not raw-score swapping, unit reflection or exact reference replication. Judge capital/currency separately and jointly from full text; first-token scores cover Stock/Tok only. Observer is prompt-masked only, not certified speech exclusion. Wrong/capped cases stay in the denominator.  Schedule: prompt and continuous decode. Prompt slice 0:; decode deltas are multiplied by 0.25. Concept token strings: (' Germany', ' Brazil').

Selection: /workspace/2026/suppressed-activations/data/country_pairs_allpos_v1/germany_brazil_joint.json declares the fixed development cases; no per-case condition selection. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes Brasília toward Berlin with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p(first='Br') |   p(first='Berlin') |   first_token_pair_mass |   r2 |
|:------------------------------|------------------------:|----------------:|--------------------:|------------------------:|-----:|
| Base                          |                  0      |      0.940432   |         1.30214e-05 |                0.940445 |    0 |
| raw J-coordinate exchange     |                -15.6875 |      0.00998209 |         0.898559    |                0.908541 |    0 |
| raw plain-coordinate exchange |                 -0.1875 |      0.934129   |         1.56016e-05 |                0.934145 |    0 |
| matched-random delta          |                 -0.0625 |      0.942625   |         1.38935e-05 |                0.942639 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Rio de Janeiro, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Bogotá', ' Buenos', ' Brasília', ' Caracas', ' Madrid', ' Jakarta', 'Madrid', ' Lisbon', 'Paris', ' São', ' Ciudad', 'São', ' Manaus', 'city', 'Jakarta', ' Amsterdam', 'London', ' Paris', ' Curitiba', ' Berlin', '里约', ' Cidade', ' Oslo', ' NYC', ' Lagos', ' Lisboa', 'Barcelona', ' Miami', ' Sao', ' Nairobi', ' Habana', 'Berlin']

Generation (7 tokens):
```text
Brasilia; BRL<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Br       | -0.0614159 | 0.940432    |             0 |
| Brazil   | -3.56142   | 0.0283986   |             0 |
| B        | -4.18642   | 0.0152007   |             0 |
| <        | -4.81142   | 0.00813633  |             0 |
| <br      | -6.93642   | 0.000971746 |             0 |
| Brasília | -7.06142   | 0.000857563 |             0 |
| Rio      | -7.18642   | 0.000756797 |             0 |
| <B       | -7.31142   | 0.000667871 |             0 |
| Bras     | -7.56142   | 0.000520138 |             0 |
| São      | -7.56142   | 0.000520138 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '.', '<|im_start|>', '</', '</tool_response>', '  \n', ';', '<|file_sep|>', '**', '.Category', '\\', '\\n', '<', '\t  \n', '\n   \n', '<br', '-Americ', '.<', '<<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' -->', '"<', ',<', ' <<<', ')', '@\\', '.ht', '<\\/', '\t\n']

Coverage: 7 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Brasília', 'BRL']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Rio de Janeiro, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Berlin', 'Berlin', 'Paris', ' Amsterdam', ' Madrid', 'Madrid', ' Frankfurt', ' Bogotá', ' Lisbon', ' Buenos', ' Munich', ' Vienna', 'London', ' Oslo', ' Brasília', ' Paris', ' Jakarta', '巴黎', ' Prague', ' Budapest', ' Caracas', 'Germany', ' Zurich', ' Stuttgart', ' Karlsruhe', 'city', ' berlin', '柏林', 'Barcelona', ' Stockholm', ' London', ' Hamburg']

Generation (4 tokens):
```text
Berlin; EUR<|im_end|>
```

| token   |     log p |           p |   delta log p |
|:--------|----------:|------------:|--------------:|
| Berlin  | -0.106963 | 0.898559    |     11.142    |
| B       | -3.23196  | 0.0394799   |      0.954453 |
| <       | -3.48196  | 0.030747    |      1.32945  |
| Br      | -4.60696  | 0.00998209  |     -4.54555  |
| Ber     | -4.85696  | 0.00777406  |     10.142    |
| Bern    | -5.85696  | 0.00285992  |      6.39195  |
| Brazil  | -6.35696  | 0.00173463  |     -2.79555  |
| <B      | -6.85696  | 0.0010521   |      0.454453 |
| Bundes  | -7.10696  | 0.00081938  |      6.20445  |
| <span   | -7.16946  | 0.000769736 |      1.20445  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', ' incorrect', ' Incorrect', '</think>', 'incorrect', '错误', '错误的', ' incorrectly', 'Incorrect', '是错误的', ' Wrong', '的错误', ' mistakenly', '不正确', ' mistake', ' -->', '错的', '  \n', '错', '\t  \n', ' FALSE', 'Wrong', '</tool_response>', '<|im_start|>', ' WRONG', ' ERROR', ';', ' errone', ' wrong', ' misplaced', ' <--']

Coverage: 4 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Berlin', 'EUR']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

# raw plain-coordinate exchange

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Rio de Janeiro, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Bogotá', ' Buenos', ' Brasília', ' Caracas', ' Madrid', ' Jakarta', 'Madrid', ' Lisbon', 'Paris', ' São', ' Ciudad', 'São', ' Manaus', ' Amsterdam', 'Jakarta', 'city', 'London', ' Paris', ' Curitiba', ' Berlin', '里约', ' Oslo', ' NYC', ' Lagos', ' Cidade', ' Lisboa', 'Barcelona', ' Miami', ' Sao', ' Nairobi', ' Habana', ' Barcelona']

Generation (7 tokens):
```text
Brasilia; BRL<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Br       | -0.0681404 | 0.934129    |   -0.00672457 |
| Brazil   | -3.44314   | 0.0319641   |    0.118275   |
| B        | -4.06814   | 0.0171092   |    0.118275   |
| <        | -4.81814   | 0.0080818   |   -0.00672483 |
| <br      | -6.81814   | 0.00109375  |    0.118275   |
| Brasília | -6.94314   | 0.000965234 |    0.118275   |
| Rio      | -6.94314   | 0.000965234 |    0.243275   |
| <B       | -7.31814   | 0.000663395 |   -0.00672483 |
| Bras     | -7.44314   | 0.000585444 |    0.118275   |
| São      | -7.50564   | 0.000549973 |    0.0557752  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '.', '<|im_start|>', '</', '</tool_response>', '  \n', ';', '**', '<|file_sep|>', '.Category', '\\', '\\n', '\t  \n', '<', '-Americ', '<br', '\n   \n', '.<', '<<<<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ' -->', '"<', ',<', ' <<<', ')', '@\\', '.ht', '<\\/', '\t\n']

Coverage: 7 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Berlin', 'EUR']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Rio de Janeiro, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' Bogotá', ' Buenos', ' Brasília', ' Caracas', ' Madrid', ' Jakarta', ' Lisbon', 'Madrid', ' São', 'Paris', 'São', ' Ciudad', ' Manaus', 'city', 'Jakarta', ' Amsterdam', 'London', ' Paris', ' Curitiba', '里约', ' Berlin', ' Cidade', ' NYC', ' Lagos', 'Argentina', ' Oslo', ' Sao', ' Miami', ' Lisboa', ' Nairobi', 'Barcelona', ' Habana']

Generation (7 tokens):
```text
Brasilia; BRL<|im_end|>
```

| token    |      log p |           p |   delta log p |
|:---------|-----------:|------------:|--------------:|
| Br       | -0.0590871 | 0.942625    |    0.00232873 |
| Brazil   | -3.55909   | 0.0284648   |    0.00232887 |
| B        | -4.43409   | 0.0118659   |   -0.247672   |
| <        | -4.80909   | 0.0081553   |    0.0023284  |
| <br      | -6.80909   | 0.0011037   |    0.127328   |
| Brasília | -6.80909   | 0.0011037   |    0.252328   |
| Rio      | -7.05909   | 0.000859562 |    0.127328   |
| São      | -7.18409   | 0.000758561 |    0.377328   |
| <B       | -7.18409   | 0.000758561 |    0.127328   |
| Bras     | -7.49659   | 0.000554975 |    0.0648284  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', '<think>', '.', '<|im_start|>', '</', ';', '</tool_response>', '  \n', '**', '<|file_sep|>', '.Category', '\\', '\\n', '\t  \n', '<', '\n   \n', '.<', '-Americ', '<br', '<<<<', ' -->', '"<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ',<', ' <<<', ')', '@\\', '.ht', '\n  \n', '\t\n']

Coverage: 7 calls; prompt slice 0:, then one position per decode.

Expected properties: ['Brasília', 'BRL']. Answer label tokenizations: [[91149], [6614, 299, 72802]]; reported probabilities cover only first tokens ('Berlin', 'Br'), not the full multi-token answers.
