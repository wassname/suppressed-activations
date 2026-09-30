---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton
expected_answer: 'control'
n_tokens: 32
answer_0: 'outside'
answer_1: 'inside'
answer_log_odds_shift: 0.171875
answer_pair_mass: 6.124220703895844e-07
r2: 0.8064516129032258
---
# matched-random delta

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' Floor', ' Science', ' page', ' floor', ' Body', '\\""', '___', ' Guinness', ' website', ' Medical', ' Page', ' Bone', ' Museum', ' Doctor', ' Planet', ' Book', ' Smithsonian', ' Zoo', ' Monday', ' Biology', ' Number', ' Tuesday', ' seventh', ' list', '\\"\\', ' Bones', ' medical', ' Spot', ' Doctors', ' Medicine', ' List', ' Top']

Generation (32 tokens):
```text
1st floor of the 1st floor of the 1st floor of the 1st floor of the 1st floor of the 1st
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       1 | -1.01585 | 0.362093   |     0.128652  |
|       2 | -1.64085 | 0.193814   |     0.128652  |
|       3 | -2.26585 | 0.103741   |    -0.121347  |
|       4 | -2.39085 | 0.0915515  |    -0.121347  |
|       5 | -2.64085 | 0.0713004  |    -0.121347  |
|       6 | -3.01585 | 0.049004   |    -0.0588474 |
|       7 | -3.39085 | 0.0336799  |    -0.183847  |
|       9 | -3.39085 | 0.0336799  |    -0.0588474 |
|       8 | -3.70335 | 0.0246407  |    -0.246347  |
|       0 | -6.26585 | 0.00190009 |     0.628653  |

Final-decode readout: ['...).', '...', '....', '.', '.....', '!.', '...\\', '….', '..."', '.…', '…', '…..', '...)', '!', ' ….', "...'", '……', ',...', '\\.', '......', '.").', ')...', '..', '...,', '…).', '...”', '.!', '.).', '.......', '...(', ' ...', '.".']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
