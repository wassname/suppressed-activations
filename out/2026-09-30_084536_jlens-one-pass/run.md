---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
k: 32
seed: 0
elapsed_seconds: 22.98
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, final three prompt positions plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

Selection: four previously answer-correct English cases, four fixed new simple English prompts, and the previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. This is the second observer layer tested; edit layer/strength remain the successful midpoint configuration. One causal pair is not a generalisation rate.

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
| J-lens swap          |                -0.125 | 0.946402 | 0.00818798 |           0.95459  | 0.0322581 |
| plain-lens swap      |                 0     | 0.943443 | 0.00720328 |           0.950646 | 0.0322581 |
| matched-random delta |                 0.125 | 0.944874 | 0.00636651 |           0.95124  | 0.0322581 |

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

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', '___', ' animals', '四肢', ' furry', '尾巴', ' ears', ' Gecko', ' Humans', ' tails', ' Animals', ' dogs', 'dogs', ' limbs', '____', ' canine', ' humanoid', '动物', ' Dogs', '__.', '两只', ' teeth', '爪', '__', ' leash', 'animals', ' mamm', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0550877 | 0.946402    |    0.00298785 |
|       2 | -4.55509   | 0.0105136   |   -0.247012   |
|       1 | -4.55509   | 0.0105136   |   -0.122012   |
|       8 | -4.80509   | 0.00818798  |    0.127988   |
|       6 | -4.80509   | 0.00818798  |    0.377988   |
|       0 | -5.05509   | 0.00637681  |   -0.122012   |
|       3 | -5.18009   | 0.00562751  |   -0.122012   |
|       5 | -6.30509   | 0.00182699  |   -0.122012   |
|       7 | -7.11759   | 0.00081072  |   -0.0595121  |
|       9 | -7.24259   | 0.000715458 |   -0.184512   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' Facts', ' hypothesis', ' statement', '上述事实', '这段话', '事实和', '的事实', 'facts', ' fatos', ' факты', ' statements', '_fact', ' inference', ' факт', ' sentence', ' premise', ' hypotheses', '事實', '这句话', ' Statement', ' entail', ' imply', ' implication', ' Statements', ' conclusion', '這句話', ' Sentence']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', '____', ' leash', ' teeth', ' limbs', ' Gecko', '__.', '__', ' pets', '犬', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0582194 | 0.943443    |  -0.000143856 |
|       2 | -4.30822   | 0.0134575   |  -0.000144005 |
|       1 | -4.43322   | 0.0118762   |  -0.000144005 |
|       8 | -4.93322   | 0.00720328  |  -0.000144005 |
|       0 | -4.93322   | 0.00720328  |  -0.000144005 |
|       3 | -5.05822   | 0.00635687  |  -0.000144005 |
|       6 | -5.18322   | 0.00560992  |  -0.000144005 |
|       5 | -6.18322   | 0.00206377  |  -0.000144005 |
|       9 | -6.93322   | 0.000974857 |   0.124856    |
|       7 | -7.05822   | 0.000860309 |  -0.000144005 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', ' Statement', '这段话', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' assumption', ' hipote', ' deduction', '?”,', '?”', ' entail', ' sentences', ' выше', ' conclusion', ' logical', ' Hyp', '以上']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' humans', ' animals', 'dogs', '___', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', ' leash', '____', ' teeth', ' limbs', ' pets', '犬', '__.', ' Gecko', '__', 'animals', ' humanoid', '兽医', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0567041 | 0.944874    |    0.00137144 |
|       2 | -4.3067    | 0.0134779   |    0.00137138 |
|       1 | -4.4317    | 0.0118942   |    0.00137138 |
|       0 | -4.9317    | 0.0072142   |    0.00137138 |
|       3 | -5.0567    | 0.00636651  |    0.00137138 |
|       8 | -5.0567    | 0.00636651  |   -0.123629   |
|       6 | -5.3067    | 0.00495824  |   -0.123629   |
|       5 | -6.1817    | 0.0020669   |    0.00137138 |
|       9 | -6.9317    | 0.000976336 |    0.126371   |
|       7 | -7.0567    | 0.000861613 |    0.00137138 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', ' Statement', '这段话', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' assumption', ' hipote', '?”', ' sentences', ' deduction', ' entail', ' logical', ' Hyp', ' conclusion', '同志为', ' выше']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.
