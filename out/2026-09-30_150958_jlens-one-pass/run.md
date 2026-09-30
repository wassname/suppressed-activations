---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
block_index: 19
residual_index: 20
readout_block_index: 23
reverse: true
swap_logits: false
plural: false
prompt_slice: '-3:'
k: 32
seed: 0
decode_scale: 1.0
donor_norm: None
donor_checkpoint: None
equal_donor_norm: false
relation: legs
elapsed_seconds: 10.95
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 19, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention: unit-direction coordinate swap. No source/donor activation extraction. Coordinate equation: h + V(swap(pinv(V)h) - pinv(V)h). Raw-score variant: h + pinv(V).T(swap(V.T h) - V.T h), swapping unnormalised lens numerators rather than guaranteed semantic features.  Schedule: prompt and continuous decode. Prompt slice -3:; decode deltas are multiplied by 1.0. Concept token strings: (' spider', ' dog').

Selection: Explicit intervention-only test: zero standalone readout benchmark cases; source/target prompts are the unchanged built-in legs relation. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |     p(4) |       p(8) |   answer_pair_mass |        r2 |
|:---------------------|------------------------:|---------:|-----------:|-------------------:|----------:|
| Base                 |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| J-lens swap          |                   0     | 0.948358 | 0.0072408  |           0.955599 | 0.0322581 |
| plain-lens swap      |                   0.125 | 0.945994 | 0.00637405 |           0.952368 | 0.0322581 |
| matched-random delta |                   0.125 | 0.944239 | 0.00636223 |           0.950601 | 0.0322581 |

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

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' humans', ' animals', '___', '四肢', ' dogs', 'dogs', ' ears', ' Animals', ' canine', ' furry', '尾巴', ' Dogs', ' Humans', ' tails', '动物', ' Gecko', '____', ' limbs', ' teeth', ' leash', ' humanoid', '__.', '__', '两只', 'animals', ' bones', ' pets', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0530233 | 0.948358    |    0.00505222 |
|       2 | -4.42802   | 0.0119381   |   -0.119948   |
|       1 | -4.55302   | 0.0105353   |   -0.119948   |
|       8 | -4.92802   | 0.0072408   |    0.00505209 |
|       0 | -5.05302   | 0.00638999  |   -0.119948   |
|       3 | -5.17802   | 0.00563914  |   -0.119948   |
|       6 | -5.17802   | 0.00563914  |    0.00505209 |
|       5 | -6.30302   | 0.00183076  |   -0.119948   |
|       9 | -7.11552   | 0.000812395 |   -0.0574479  |
|       7 | -7.17802   | 0.000763175 |   -0.119948   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' fakta', ' hypothesis', ' Facts', ' statement', '上述事实', '这段话', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', '_fact', ' inference', ' факт', ' hypotheses', ' premise', ' sentence', '事實', ' entail', ' Statement', '这句话', ' implication', ' conclusion', ' imply', ' Statements', '陈述', ' assertion']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', '___', 'dogs', '四肢', ' Dogs', ' canine', ' ears', ' Animals', '尾巴', ' furry', ' tails', ' Humans', '动物', '____', ' leash', ' teeth', ' limbs', ' Gecko', '__.', ' pets', '犬', '__', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555194 | 0.945994    |    0.00255607 |
|       2 | -4.30552   | 0.0134939   |    0.00255585 |
|       1 | -4.43052   | 0.0119083   |    0.00255585 |
|       0 | -4.93052   | 0.00722275  |    0.00255585 |
|       8 | -5.05552   | 0.00637405  |   -0.122444   |
|       3 | -5.18052   | 0.00562508  |   -0.122444   |
|       6 | -5.30552   | 0.00496412  |   -0.122444   |
|       5 | -6.30552   | 0.0018262   |   -0.122444   |
|       9 | -7.05552   | 0.000862634 |    0.00255585 |
|       7 | -7.11802   | 0.00081037  |   -0.0599442  |

Final-decode readout: [' facts', ' factual', '事实', ' hypothesis', ' Fakta', ' Facts', ' fakta', ' statement', '上述事实', '这段话', '事实和', 'facts', ' fatos', '的事实', ' факты', ' statements', ' premise', ' hypotheses', '_fact', ' inference', ' факт', ' sentence', ' entail', ' Statement', '事實', ' conclusion', ' imply', ' implication', '这句话', ' Statements', 'statement', 'Statement']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', 'dogs', '___', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' Humans', ' tails', '动物', ' leash', '____', ' limbs', ' teeth', ' pets', '犬', ' Gecko', 'animals', '__.', '__', ' humanoid', '兽医', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0573761 | 0.944239    |   0.000699442 |
|       2 | -4.30738   | 0.0134688   |   0.00069952  |
|       1 | -4.43238   | 0.0118862   |   0.00069952  |
|       0 | -4.93238   | 0.00720935  |   0.00069952  |
|       3 | -5.05738   | 0.00636223  |   0.00069952  |
|       8 | -5.05738   | 0.00636223  |  -0.1243      |
|       6 | -5.18238   | 0.00561465  |   0.00069952  |
|       5 | -6.18238   | 0.00206551  |   0.00069952  |
|       9 | -6.93238   | 0.00097568  |   0.1257      |
|       7 | -7.05738   | 0.000861035 |   0.00069952  |

Final-decode readout: [' hypothesis', ' statement', ' statements', '这段话', ' Statement', ' hypotheses', 'Statement', '这句话', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' sentence', ' inference', '陈述', ' assertion', ' Sentence', ' premise', ' prediction', '?”,', ' assumption', ' deduction', '?”', ' entail', ' hipote', ' sentences', ' logical', ' conclusion', ' Hyp', ' выше', '以上']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
