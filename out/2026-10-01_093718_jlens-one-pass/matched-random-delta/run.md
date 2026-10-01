---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: true
country_swap: false
coordinate_kind: None
reverse: true
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
vjp_checkpoint: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.9486119151115417
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9486119151115417
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', '___', ' dogs', ' animals', ' humans', '四肢', 'dogs', ' ears', ' canine', ' Dogs', ' Animals', '尾巴', ' tails', ' furry', ' Humans', ' leash', ' limbs', '____', '动物', ' teeth', ' Gecko', '__.', ' humanoid', '__', ' bones', '两只', ' pets', ' mamm', 'animals']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0603616 | 0.941424    |   -0.00228608 |
|       2 | -4.18536   | 0.0152167   |    0.122714   |
|       1 | -4.43536   | 0.0118508   |   -0.00228596 |
|       0 | -4.81036   | 0.00814492  |    0.122714   |
|       8 | -4.93536   | 0.00718786  |   -0.00228596 |
|       3 | -5.06036   | 0.00634327  |   -0.00228596 |
|       6 | -5.31036   | 0.00494014  |   -0.127286   |
|       5 | -6.18536   | 0.00205936  |   -0.00228596 |
|       9 | -6.99786   | 0.000913834 |    0.060214   |
|       7 | -7.06036   | 0.000858468 |   -0.00228596 |

Final-decode readout: [' hypothesis', ' statement', ' statements', ' Statement', '这段话', 'Statement', ' hypotheses', ' Statements', 'statement', '这句话', '這句話', 'Statements', ' implication', '陈述', ' sentence', ' assertion', ' inference', ' premise', ' Sentence', ' prediction', ' assumption', '?”,', '?”', ' sentences', ' deduction', ' entail', ' logical', ' hipote', 'statements', ' выше', ' assertions', ' conclusion']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
