---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
prompt_slice: '0:'
k: 32
seed: 0
elapsed_seconds: 18.37
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, prompt slice 0: plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

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
| J-lens swap          |                -0.125 | 0.949041 | 0.00821081 |           0.957252 | 0.0322581 |
| plain-lens swap      |                 0.125 | 0.945972 | 0.00637391 |           0.952346 | 0.0322581 |
| matched-random delta |                 0.125 | 0.944858 | 0.00636641 |           0.951225 | 0.0322581 |

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

Coverage: 32 calls; prompt slice 0:, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', '___', '四肢', ' animals', ' furry', ' Gecko', ' ears', '尾巴', ' Humans', ' tails', ' Animals', ' limbs', '两只', ' humanoid', '____', '__.', '爪', 'dogs', '动物', ' dogs', ' teeth', ' canine', '双腿', '__', ' spiders', ' Dogs', ' cats', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the fact
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0523033 | 0.949041    |    0.00577217 |
|       2 | -4.4273    | 0.0119467   |   -0.119228   |
|       1 | -4.8023    | 0.00821081  |   -0.369228   |
|       8 | -4.8023    | 0.00821081  |    0.130772   |
|       6 | -4.8023    | 0.00821081  |    0.380772   |
|       0 | -5.1773    | 0.0056432   |   -0.244228   |
|       3 | -5.3023    | 0.00498011  |   -0.244228   |
|       5 | -6.3023    | 0.00183208  |   -0.119228   |
|       7 | -7.3648    | 0.00063315  |   -0.306728   |
|       9 | -7.4273    | 0.000594789 |   -0.369228   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' hypothesis', ' Facts', '这段话', ' statement', '上述事实', '事实和', ' statements', ' fatos', 'facts', '的事实', ' факты', ' inference', '_fact', ' sentence', ' premise', ' hypotheses', ' факт', '这句话', ' entail', ' Statement', ' imply', ' implication', '這句話', '事實', ' Statements', ' Sentence', ' conclusion']

Coverage: 32 calls; prompt slice 0:, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', 'dogs', ' humans', ' canine', ' Dogs', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' tails', ' Humans', '动物', ' leash', '____', ' limbs', ' teeth', ' pets', '犬', '__.', '__', ' Gecko', 'animals', ' bones', ' humanoid', '狗']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555422 | 0.945972    |    0.00253329 |
|       2 | -4.30554   | 0.0134936   |    0.00253344 |
|       1 | -4.43054   | 0.011908    |    0.00253344 |
|       0 | -4.93054   | 0.00722259  |    0.00253344 |
|       8 | -5.05554   | 0.00637391  |   -0.122467   |
|       3 | -5.18054   | 0.00562496  |   -0.122467   |
|       6 | -5.30554   | 0.00496401  |   -0.122467   |
|       5 | -6.30554   | 0.00182616  |   -0.122467   |
|       9 | -7.05554   | 0.000862615 |    0.00253344 |
|       7 | -7.11804   | 0.000810352 |   -0.0599666  |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' hypotheses', '这段话', ' Statement', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' premise', ' Sentence', ' prediction', ' hipote', ' assumption', ' deduction', ' sentences', ' entail', '?”,', '?”', ' conclusion', ' Hyp', ' logical', ' выше', 'sentence']

Coverage: 32 calls; prompt slice 0:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', ' animals', '___', ' humans', 'dogs', '四肢', ' Dogs', ' canine', ' ears', ' Animals', '尾巴', ' furry', ' Humans', ' tails', '____', '动物', ' leash', ' limbs', ' teeth', '__', ' pets', ' Gecko', '__.', '犬', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0567203 | 0.944858    |    0.00135522 |
|       2 | -4.30672   | 0.0134777   |    0.00135517 |
|       1 | -4.43172   | 0.011894    |    0.00135517 |
|       0 | -4.93172   | 0.00721408  |    0.00135517 |
|       3 | -5.05672   | 0.00636641  |    0.00135517 |
|       8 | -5.05672   | 0.00636641  |   -0.123645   |
|       6 | -5.30672   | 0.00495816  |   -0.123645   |
|       5 | -6.18172   | 0.00206687  |    0.00135517 |
|       9 | -6.93172   | 0.00097632  |    0.126355   |
|       7 | -7.05672   | 0.000861599 |    0.00135517 |

Final-decode readout: [' facts', ' factual', ' hypothesis', ' Fakta', '事实', ' fakta', ' Facts', ' statement', '这段话', '上述事实', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', ' hypotheses', ' inference', ' premise', '_fact', ' факт', ' sentence', ' implication', ' Statement', ' entail', ' conclusion', '事實', ' imply', '这句话', ' assertion', '這句話', ' Statements']

Coverage: 32 calls; prompt slice 0:, then one position per decode.
