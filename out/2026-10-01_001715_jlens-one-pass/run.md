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
relation: capital
elapsed_seconds: 17.73
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  Rome to  Tokyo. Positive answer_log_odds_shift favours  Tokyo over  Rome; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Primary: raw pair-coordinate exchange h+V(swap(pinv(V)h)-pinv(V)h), V=([W_Italy;W_Japan]*gain @ J[15]).T (block15/output residual16). No column normalization or raw-score exchange in the primary. Unit J and raw plain are separate controls. Random uses one fixed seed0 direction with primary-update norm from its own current state; only prefill doses match. No preliminary current-input pass, donor preparation, sparse decomposition or clean-pass clamp. Not an exact reference reproduction. Clean target prefill follows all five conditions of this property, without feedback. Correct Base and coherent Tokyo AND yen under the same primary rule are required; bare-answer odds alone do not show identity. An article can make first-token metrics nondiagnostic. Inspect whether Base already names Italy; that would limit the hidden-concept claim. Observer is prompt-masked only, not certified speech exclusion. Basis rank and post-cast coordinate errors are recorded. Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 1.0. Concept token strings: (' Italy', ' Japan').

Selection: Fixed Italy-to-Japan capital/currency pair, chosen after failed animal transfer and polar readout. Five conditions per property, one configuration. Earlier trailing-space currency prompt answered100% gold; this exact no-space form was untested. Retain wrong baselines; no prompt or alternate-winner rescue. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  Rome toward  Tokyo with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                     |   answer_log_odds_shift |   p( Tokyo) |   p( Rome) |   answer_pair_mass |        r2 |
|:------------------------------|------------------------:|------------:|-----------:|-------------------:|----------:|
| Base                          |            -1.19209e-07 | 0.000875784 |   0.514072 |           0.514948 | 0.0645161 |
| raw J-coordinate exchange     |             0.0624999   | 0.00092665  |   0.510975 |           0.511901 | 0.0645161 |
| unit J-coordinate exchange    |             0.0624999   | 0.00092755  |   0.511471 |           0.512399 | 0.0645161 |
| raw plain-coordinate exchange |             0.125       | 0.000971902 |   0.503458 |           0.50443  | 0.0645161 |
| matched-random delta          |            -0.0625001   | 0.000818376 |   0.511356 |           0.512174 | 0.0645161 |

[Base](base/run.md)

# Base

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' Naples', ' London', ' Vienna', ' Barcelona', ' France', ' Berlin', ' Austria', ' Buenos', ' Amsterdam', ' Dublin', ' Tokyo', ' Munich', 'Italy', ' Germany', ' Oslo', ' Spain', ' Bogotá', ' Venice', ' Vatican', ' Italian', ' Jakarta', ' Greece', ' Bangkok', ' Athens', ' Prague', ' Switzerland']

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
| Rome    | -0.665392 | 0.514072   |             0 |
| Italy   | -1.91539  | 0.147284   |             0 |
| Madrid  | -3.16539  | 0.0421976  |             0 |
| in      | -3.29039  | 0.0372393  |             0 |
| the     | -3.85289  | 0.0212183  |             0 |
| Spain   | -4.04039  | 0.0175906  |             0 |
| located | -4.35289  | 0.0128695  |             0 |
| London  | -4.79039  | 0.0083092  |             0 |
| not     | -4.97789  | 0.00688857 |             0 |
| a       | -5.16539  | 0.00571083 |             0 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', ')**', '）**', '”**', '**', ' **“', ']**', ':**', '’**', '%**', ' **—', '.**', '**-', '。**', '):**', '**—', '*”', ').**', '软', '：“', '!**', '-**', '害', '.:**', '"><?=', '<think>', '”**.']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[raw J-coordinate exchange](raw-j-coordinate-exchange/run.md)

# raw J-coordinate exchange

Input:
```text
'Fact: The capital of the country shaped like a boot is'
```

Prefill readout: [' Italy', ' Madrid', ' Paris', ' Lisbon', ' Portugal', ' Rome', ' Naples', ' London', ' Vienna', ' Barcelona', ' Berlin', ' France', ' Austria', ' Buenos', ' Amsterdam', ' Tokyo', ' Dublin', ' Munich', ' Oslo', ' Germany', 'Italy', ' Spain', ' Jakarta', ' Bogotá', ' Venice', ' Bangkok', ' Vatican', ' Greece', ' Athens', ' Italian', ' Prague', ' Switzerland']

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
| Rome    | -0.671435 | 0.510975   |   -0.00604349 |
| Italy   | -1.92144  | 0.146397   |   -0.00604355 |
| Madrid  | -3.10894  | 0.0446485  |    0.0564563  |
| in      | -3.29644  | 0.0370149  |   -0.00604367 |
| the     | -3.85894  | 0.0210904  |   -0.00604367 |
| Spain   | -3.98394  | 0.0186123  |    0.0564563  |
| located | -4.35893  | 0.012792   |   -0.00604343 |
| London  | -4.73393  | 0.00879181 |    0.0564566  |
| not     | -4.92143  | 0.00728867 |    0.0564566  |
| a       | -5.17143  | 0.00567642 |   -0.00604343 |

Final-decode readout: ['**”', '：**', '</think>', '"**', '>**', ';**', '”**', '）**', ')**', '**', ':**', ' **“', '%**', ']**', '’**', ' **—', '.**', '。**', '**-', '):**', '*”', '软', '**—', ').**', '.:**', '-**', '!**', '害', '<think>', ':*', '：“', '"><?=']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[unit J-coordinate exchange](unit-j-coordinate-exchange/run.md)

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

[raw plain-coordinate exchange](raw-plain-coordinate-exchange/run.md)

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

[matched-random delta](matched-random-delta/run.md)

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
