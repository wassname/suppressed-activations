---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 23
residual_index: 24
readout_block_index: 23
reverse: true
prompt_slice: '-3:'
k: 32
seed: 0
elapsed_seconds: 24.83
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 23, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, prompt slice -3: plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

Selection: four previously answer-correct English cases, four fixed new simple English prompts, and the previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: J-lens recovers hidden words better than the same-layer plain lens. The swap should change 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

| concept   | readout    |   hidden rank |   answer rank | joint pass   |
|:----------|:-----------|--------------:|--------------:|:-------------|
| Bulgaria  | J-lens     |           655 |           607 | False        |
| Bulgaria  | plain lens |         35232 |         64063 | False        |
| Iceland   | J-lens     |           140 |           230 | False        |
| Iceland   | plain lens |         57271 |          2035 | False        |
| Turkey    | J-lens     |          1368 |            48 | False        |
| Turkey    | plain lens |         22800 |          4673 | False        |
| Congo     | J-lens     |            13 |          6330 | True         |
| Congo     | plain lens |             0 |           360 | True         |
| Italy     | J-lens     |            63 |             3 | False        |
| Italy     | plain lens |          5820 |             0 | False        |
| Italy     | J-lens     |            25 |             4 | False        |
| Italy     | plain lens |         12847 |           177 | False        |
| dog       | J-lens     |            57 |            57 | False        |
| dog       | plain lens |         14384 |         73837 | False        |
| bird      | J-lens     |            13 |           330 | True         |
| bird      | plain lens |          6835 |        175150 | False        |

| condition            |   swap_log_odds_shift |       p4 |         p8 |   bare_answer_mass |        r2 |
|:---------------------|----------------------:|---------:|-----------:|-------------------:|----------:|
| Base                 |                 0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| J-lens swap          |                 0     | 0.946994 | 0.00723039 |           0.954225 | 0.0322581 |
| plain-lens swap      |                 0.125 | 0.947517 | 0.00638432 |           0.953901 | 0.0322581 |
| matched-random delta |                 0     | 0.943456 | 0.00720337 |           0.950659 | 0.0322581 |

Readout input: "The capital of the country with the national anthem 'Mila Rodino' is"

Baseline continuation (up to 8 tokens): ':\nA. Sofia\nB.'

Readout input: "The capital of the country with the national anthem 'Lofsöngur' is"

Baseline continuation (up to 8 tokens): ' Reykjavík.\nA.'

Readout input: "The country with the national anthem 'İstiklâl Marşı' is led by president"

Baseline continuation (up to 8 tokens): ' Recep Tayyip Erdoğan.\nA.'

Readout input: 'The country with Brazzaville as its capital is led by president'

Baseline continuation (up to 8 tokens): ' Denis Sassou Nguesso.\n'

Readout input: 'Fact: The capital of the country shaped like a boot is '

Baseline continuation (up to 8 tokens): 'rome.\nHypothesis: The'

Readout input: 'Fact: The currency used in the country shaped like a boot is '

Baseline continuation (up to 8 tokens): '100% gold.\nH'

Readout input: 'Fact: The number of legs on the animal that barks is '

Baseline continuation (up to 8 tokens): '4.\nHypothesis: The'

Readout input: 'Fact: The number of legs on the animal with feathers and a beak is '

Baseline continuation (up to 8 tokens): '2.\nHypothesis: The'

[Base](base/run.md)

# Base

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' tails', '动物', ' Humans', '____', ' leash', ' limbs', ' teeth', '犬', '__.', ' pets', '__', ' Gecko', 'animals', ' bones', ' humanoid', '两只']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0580755 | 0.943579    |             0 |
|       2 | -4.30808   | 0.0134594   |             0 |
|       1 | -4.43308   | 0.0118779   |             0 |
|       8 | -4.93308   | 0.00720431  |             0 |
|       0 | -4.93308   | 0.00720431  |             0 |
|       3 | -5.05808   | 0.00635778  |             0 |
|       6 | -5.18308   | 0.00561072  |             0 |
|       5 | -6.18308   | 0.00206407  |             0 |
|       7 | -7.05808   | 0.000860432 |             0 |
|       9 | -7.05808   | 0.000860432 |             0 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', ' assumption', ' hipote', ' sentences', '?”,', ' deduction', ' entail', '?”', ' logical', ' выше', ' conclusion', '以上', ' Hyp']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', '___', ' humans', ' animals', '四肢', ' ears', '尾巴', ' Animals', ' furry', ' tails', ' Gecko', ' Humans', '____', ' limbs', '动物', '__.', 'dogs', ' dogs', ' teeth', ' leash', ' canine', ' humanoid', '__', ' bones', '两只', '爪', ' mamm', ' Dogs', 'animals']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0544622 | 0.946994    |     0.0036133 |
|       2 | -4.42946   | 0.0119209   |    -0.121387  |
|       1 | -4.42946   | 0.0119209   |     0.003613  |
|       8 | -4.92946   | 0.00723039  |     0.003613  |
|       0 | -5.05446   | 0.0063808   |    -0.121387  |
|       3 | -5.17946   | 0.00563103  |    -0.121387  |
|       6 | -5.17946   | 0.00563103  |     0.003613  |
|       5 | -6.30446   | 0.00182813  |    -0.121387  |
|       7 | -7.11696   | 0.000811227 |    -0.058887  |
|       9 | -7.11696   | 0.000811227 |    -0.058887  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' assumption', ' deduction', ' sentences', ' hipote', '?”,', ' entail', '?”', ' logical', ' выше', ' conclusion', ' Hyp', '以上']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' animals', ' humans', '___', '四肢', ' dogs', ' ears', ' Animals', '尾巴', 'dogs', ' canine', ' furry', ' tails', ' Humans', ' Dogs', '动物', '____', ' limbs', ' leash', ' Gecko', ' teeth', '__.', '__', ' humanoid', ' bones', ' pets', '两只', 'animals', '兽医']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0539107 | 0.947517    |    0.00416481 |
|       2 | -4.42891   | 0.0119275   |   -0.120835   |
|       1 | -4.42891   | 0.0119275   |    0.0041647  |
|       0 | -4.92891   | 0.00723438  |    0.0041647  |
|       8 | -5.05391   | 0.00638432  |   -0.120835   |
|       3 | -5.17891   | 0.00563414  |   -0.120835   |
|       6 | -5.30391   | 0.00497211  |   -0.120835   |
|       5 | -6.30391   | 0.00182914  |   -0.120835   |
|       9 | -7.05391   | 0.000864023 |    0.0041647  |
|       7 | -7.11641   | 0.000811675 |   -0.0583353  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', '陈述', ' inference', ' assertion', ' Sentence', ' premise', ' prediction', ' assumption', ' hipote', '?”,', ' sentences', ' entail', '?”', ' deduction', ' logical', ' выше', ' conclusion', '同志为', ' Hyp']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', ' animals', '___', 'dogs', ' humans', ' Dogs', ' canine', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' Humans', '动物', ' leash', ' tails', '____', ' limbs', '犬', ' Gecko', ' pets', '__.', ' teeth', '__', 'animals', '狗', ' bones', ' humanoid']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0582056 | 0.943456    |  -0.000130136 |
|       2 | -4.30821   | 0.0134577   |  -0.000130177 |
|       1 | -4.43321   | 0.0118764   |  -0.000130177 |
|       8 | -4.93321   | 0.00720337  |  -0.000130177 |
|       0 | -4.93321   | 0.00720337  |  -0.000130177 |
|       3 | -5.05821   | 0.00635696  |  -0.000130177 |
|       6 | -5.18321   | 0.00560999  |  -0.000130177 |
|       5 | -6.18321   | 0.0020638   |  -0.000130177 |
|       9 | -6.93321   | 0.000974871 |   0.12487     |
|       7 | -7.05821   | 0.00086032  |  -0.000130177 |

Final-decode readout: [' hypothesis', ' statement', ' statements', '这段话', ' hypotheses', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' hipote', ' assumption', ' sentences', '?”', ' entail', ' deduction', ' conclusion', ' выше', ' logical', ' Hyp', 'sentence']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
