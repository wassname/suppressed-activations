---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
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
vjp_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt
donor_checkpoint: None
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9523587226867676
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9523587226867676
r2: 0.032258064516129004
---
# offline naming VJP

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' tails', ' Humans', '动物', '____', ' leash', ' teeth', ' limbs', '犬', '__.', ' pets', ' Gecko', '__', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555289 | 0.945985    |    0.0025466  |
|       2 | -4.30553   | 0.0134937   |    0.00254631 |
|       1 | -4.43053   | 0.0119082   |    0.00254631 |
|       0 | -4.93053   | 0.00722268  |    0.00254631 |
|       8 | -5.05553   | 0.00637399  |   -0.122454   |
|       3 | -5.18053   | 0.00562503  |   -0.122454   |
|       6 | -5.30553   | 0.00496407  |   -0.122454   |
|       5 | -6.30553   | 0.00182618  |   -0.122454   |
|       9 | -7.05553   | 0.000862626 |    0.00254631 |
|       7 | -7.11803   | 0.000810362 |   -0.0599537  |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' hypothesis', ' Facts', ' fakta', ' statement', '上述事实', '这段话', '事实和', 'facts', '的事实', ' statements', ' fatos', ' факты', '_fact', ' inference', ' premise', ' hypotheses', ' факт', ' sentence', ' entail', ' Statement', '事實', ' implication', ' conclusion', ' imply', '这句话', ' Statements', ' assertion', 'Statement']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
