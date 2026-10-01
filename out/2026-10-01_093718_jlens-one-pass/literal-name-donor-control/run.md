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
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.375
answer_pair_mass: 0.9450358152389526
swap_log_odds_shift: -0.375
bare_answer_mass: 0.9450358152389526
r2: 0.032258064516129004
---
# literal-name donor control

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', 'dogs', ' canine', ' Dogs', '___', ' ears', '四肢', '尾巴', ' Animals', ' furry', ' tails', ' Humans', ' leash', '动物', ' teeth', '____', '兽医', ' pets', ' limbs', '犬', ' Gecko', ' bones', '爪', 'animals', '两只', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |          p |   delta log p |
|--------:|-----------:|-----------:|--------------:|
|       4 | -0.0675803 | 0.934653   |   -0.00950475 |
|       1 | -4.19258   | 0.0151073  |    0.240495   |
|       2 | -4.31758   | 0.0133321  |   -0.0095048  |
|       8 | -4.56758   | 0.0103831  |    0.365495   |
|       6 | -4.94258   | 0.00713616 |    0.240495   |
|       0 | -4.94258   | 0.00713616 |   -0.0095048  |
|       3 | -5.06758   | 0.00629764 |   -0.0095048  |
|       5 | -5.94258   | 0.00262525 |    0.240495   |
|       9 | -6.69258   | 0.00124008 |    0.365495   |
|       7 | -6.81758   | 0.00109437 |    0.240495   |

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' hypothesis', ' fakta', ' Facts', ' statement', '这段话', '上述事实', '事实和', 'facts', '的事实', ' fatos', ' факты', ' statements', '_fact', ' факт', ' inference', ' hypotheses', ' premise', ' sentence', ' Statement', ' entail', '事實', '这句话', ' implication', ' conclusion', ' imply', ' Statements', '陈述', 'Statement']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
