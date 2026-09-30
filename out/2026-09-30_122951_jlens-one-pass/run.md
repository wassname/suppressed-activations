---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
prompt_slice: '-3:'
k: 32
seed: 0
decode_scale: 0.25
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
elapsed_seconds: 12.63
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 8 to 4. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step; decode deltas are multiplied by 0.25. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |      p(4) |      p(8) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|----------:|----------:|-------------------:|----------:|
| Base                            |            -7.45058e-09 | 0.0564207 | 0.882568  |           0.938989 | 0.0322581 |
| norm-matched J donor projection |             5.625       | 0.552322  | 0.0311599 |           0.583482 | 0.0322581 |
| full donor contrast             |             6.375       | 0.654436  | 0.0174401 |           0.671876 | 0.0645161 |
| matched-random delta            |             1.625       | 0.220458  | 0.679057  |           0.899515 | 0.0967742 |

[Base](base/run.md)

# Base

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', 'Spider', ' Spider', '蛛', ' claws', '-web', '___', ' venom', '爬', ' insects', '.\\', ' crawling', '四肢', '爪子', ' Gecko', ' limbs', '_web', ').\\', '网页', '昆虫', '�', '爬虫', ' claw', '____', ' eight', '后腿', ' lizard', '双腿', ' paw', '触角']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.124919 | 0.882568   |             0 |
|       4 | -2.87492  | 0.0564207  |             0 |
|       6 | -3.62492  | 0.0266513  |             0 |
|       1 | -4.62492  | 0.00980445 |             0 |
|       2 | -4.99992  | 0.00673849 |             0 |
|       3 | -5.12492  | 0.0059467  |             0 |
|       5 | -5.62492  | 0.00360685 |             0 |
|       7 | -5.74992  | 0.00318304 |             0 |
|       0 | -6.49992  | 0.00150356 |             0 |
|       9 | -6.56242  | 0.00141246 |             0 |

Final-decode readout: ['**:', '»:', '*:', ':**', '”:', '__:', '):', ':.', '：**', ':\\', ']:', '.):', '>:', ':', '：', ':</', '’:', '":', '+:', ':")', '#:', '():', ':".', '.:', '!:', '}:', ' **:', '):**', ':user', '):\\', '\\":', ')):']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

# norm-matched J donor projection

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' dogs', '____', ' Dogs', ' dog', '___', 'dogs', ' canine', ' ____', ' Dog', '__', '狗', ' ___', ' ______', ' __', '犬', ' leash', 'Dog', 'dog', ' paw', '\\"', '.\\', ' pets', '________', '__.', '_________', '狗的', ' animals', '_____', ' ________', '\\n', ' _____', ' pet']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that spins the best have?
Options:
A. 4
B. 5
C
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.593623 | 0.552322   |      2.2813   |
|       2 | -1.59362  | 0.203188   |      3.4063   |
|       1 | -2.71862  | 0.0659655  |      1.9063   |
|       6 | -3.09362  | 0.0453374  |      0.531296 |
|       3 | -3.34362  | 0.0353088  |      1.7813   |
|       8 | -3.46862  | 0.0311599  |     -3.3437   |
|       0 | -3.46862  | 0.0311599  |      3.0313   |
|       5 | -4.09362  | 0.0166787  |      1.5313   |
|       7 | -4.96862  | 0.00695271 |      0.781296 |
|       9 | -5.09362  | 0.00613575 |      1.4688   |

Final-decode readout: [' Answer', ' Options', ' Answers', ' Correct', '正确答案', ' Option', ' answer', '答案', ' ANSW', ' Explanation', 'answer', 'Answer', '选项', ' Analysis', ' Solution', ' Choices', 'correct', ' Please', ' Question', '_answer', ' Choice', ' answers', ' Incorrect', 'Correct', '回答', '的答案', ' Conclusion', ' Cannot', '答案是', ' Explain', '正确', 'Option']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' dogs', '.\\', '____', ' Dogs', ' canine', '___', 'dogs', '__', '.\\"', ' dog', '犬', '__.', '\\"\\', ' ____', ' pets', ' paw', 'dog', ' leash', '宠物', '狗', ' Dog', 'Dog', '\\"', ' __', '。\\', ' pet', '\\n', ').\\', ' animals', ' ___', ' ______', '狗的']

Generation (32 tokens):
```text
4.
Hypothesis: The animal that spins dog is 4.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.423981 | 0.654436   |     2.45094   |
|       2 | -1.79898  | 0.165467   |     3.20094   |
|       1 | -2.79898  | 0.060872   |     1.82594   |
|       0 | -3.04898  | 0.0474072  |     3.45094   |
|       3 | -3.92398  | 0.0197623  |     1.20094   |
|       8 | -4.04898  | 0.0174401  |    -3.92406   |
|       6 | -4.04898  | 0.0174401  |    -0.424062  |
|       5 | -4.79898  | 0.00823814 |     0.825938  |
|       9 | -5.42398  | 0.00440956 |     1.13844   |
|       7 | -5.67398  | 0.00343417 |     0.0759382 |

Final-decode readout: ['*\\', ':*', '{*', '...*', ')**', '*C', '：**', '-**', '**', ':**', '...**', '(**', '*(', ' *\\', '*:', '*)', ';*', ')*(', ',**', ')*', ';**', '"**', ',*', '"*', '):**', '*', '*"', '*B', '.*)', '*X', '.**', '**(']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' spiders', ' spider', '蜘蛛', ' Spider', 'Spider', ' claws', '___', '.\\', '蛛', '爬', ' ___', '...\\', ' paw', ' Gecko', '爪子', ' claw', '-web', ').\\', '\\"\\', ' crawling', '\\"', ' eight', '.\\"', ' venom', '____', ' crawl', '\\n', '__.', ' seven', ' __', '爬虫', '__']

Generation (32 tokens):
```text
8.
Question: How many legs does the animal that spins webs have?
Options:
A. 8
B. 8
C.
```

| token   |    log p |          p |   delta log p |
|:--------|---------:|-----------:|--------------:|
| 8       | -0.38705 | 0.679057   |      -0.26213 |
| 4       | -1.51205 | 0.220458   |       1.36287 |
| 2       | -3.63705 | 0.0263299  |       1.36287 |
| 1       | -3.88705 | 0.0205058  |       0.73787 |
| 6       | -3.88705 | 0.0205058  |      -0.26213 |
| 3       | -4.51205 | 0.0109759  |       0.61287 |
| 0       | -4.63705 | 0.00968623 |       1.86287 |
| 5       | -5.51205 | 0.00403782 |       0.11287 |
| 7       | -5.88705 | 0.00277515 |      -0.13713 |
|         | -6.26205 | 0.00190733 |       0.73787 |

Final-decode readout: [' Cannot', ' None', ' cannot', ' neither', ' Neither', ' none', 'Cannot', ' Impossible', ' impossible', ' Few', ' Options', ' NONE', ' Option', ' unsure', ' Never', ' eighty', 'cannot', ' Unable', ' inability', ' eight', ' Both', ' fewer', ' Unknown', ' unable', '都无法', ' nonexistent', ' NOTA', ' unknown', ' Unsure', ' Doesn', ' Undefined', ' D']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
