---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: '4'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 5.624999523162842
answer_pair_mass: 0.5834822654724121
swap_log_odds_shift: 5.624999523162842
bare_answer_mass: 0.5834822654724121
r2: 0.032258064516129004
---
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

Written by PI/OpenAI.
