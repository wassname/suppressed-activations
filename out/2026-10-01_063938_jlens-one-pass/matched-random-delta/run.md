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
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.125
answer_pair_mass: 0.9523686170578003
swap_log_odds_shift: 0.125
bare_answer_mass: 0.9523686170578003
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', '___', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', '尾巴', ' furry', ' tails', ' Humans', '动物', ' leash', '____', ' limbs', ' teeth', '犬', ' pets', ' Gecko', '__.', '__', 'animals', ' humanoid', '两只', ' bones']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0555184 | 0.945995    |    0.00255709 |
|       2 | -4.30552   | 0.0134939   |    0.0025568  |
|       1 | -4.43052   | 0.0119083   |    0.0025568  |
|       0 | -4.93052   | 0.00722276  |    0.0025568  |
|       8 | -5.05552   | 0.00637406  |   -0.122443   |
|       3 | -5.18052   | 0.00562509  |   -0.122443   |
|       6 | -5.30552   | 0.00496412  |   -0.122443   |
|       5 | -6.30552   | 0.0018262   |   -0.122443   |
|       9 | -7.05552   | 0.000862635 |    0.0025568  |
|       7 | -7.11802   | 0.000810371 |   -0.0599432  |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' hypothesis', ' Facts', ' fakta', ' statement', '这段话', '上述事实', '事实和', 'facts', '的事实', ' statements', ' fatos', ' факты', ' inference', '_fact', ' premise', ' hypotheses', ' факт', ' sentence', ' entail', ' Statement', '事實', ' implication', ' conclusion', ' imply', '这句话', ' Statements', ' assertion', 'Statement']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
