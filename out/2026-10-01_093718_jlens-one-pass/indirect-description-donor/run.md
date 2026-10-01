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
answer_log_odds_shift: -0.125
answer_pair_mass: 0.9524683952331543
swap_log_odds_shift: -0.125
bare_answer_mass: 0.9524683952331543
r2: 0.032258064516129004
---
# indirect-description donor

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', '___', ' animals', ' dogs', '四肢', ' humans', 'dogs', ' canine', ' Dogs', ' Animals', ' ears', '尾巴', ' furry', '动物', '____', ' tails', ' Gecko', ' teeth', ' Humans', ' limbs', '__', ' leash', '__.', ' bones', 'animals', '犬', '爪', '兽医', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0573128 | 0.944299    |   0.000762701 |
|       2 | -4.43231   | 0.011887    |  -0.124238    |
|       1 | -4.43231   | 0.011887    |   0.000762463 |
|       8 | -4.80731   | 0.00816978  |   0.125762    |
|       0 | -4.80731   | 0.00816978  |   0.125762    |
|       3 | -5.18231   | 0.005615    |  -0.124238    |
|       6 | -5.18231   | 0.005615    |   0.000762463 |
|       5 | -6.30731   | 0.00182292  |  -0.124238    |
|       7 | -7.11981   | 0.000808918 |  -0.0617375   |
|       9 | -7.18231   | 0.000759908 |  -0.124238    |

Final-decode readout: [' facts', ' factual', '事实', ' Fakta', ' hypothesis', ' Facts', ' fakta', ' statement', '这段话', '上述事实', '事实和', ' statements', ' fatos', 'facts', '的事实', ' факты', ' inference', ' premise', ' hypotheses', '_fact', ' факт', ' sentence', ' Statement', ' entail', ' implication', '事實', ' conclusion', ' imply', '这句话', ' Statements', ' assertion', 'Statement']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
