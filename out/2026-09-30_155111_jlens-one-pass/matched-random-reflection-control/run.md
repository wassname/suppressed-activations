---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: None
donor_reflection: true
equal_donor_norm: false
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.9507830142974854
swap_log_odds_shift: 0.0
bare_answer_mass: 0.9507830142974854
r2: 0.032258064516129004
---
# matched-random reflection control

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', '___', ' humans', 'dogs', ' canine', ' Dogs', '四肢', ' Animals', ' ears', ' furry', '尾巴', ' tails', '动物', ' Humans', '____', ' leash', ' limbs', ' teeth', '犬', '__.', ' pets', '__', ' Gecko', 'animals', ' bones', ' humanoid', '两只']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
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

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' hypothesis', ' fakta', ' Facts', ' statement', '上述事实', '这段话', '事实和', ' statements', ' fatos', 'facts', '的事实', ' факты', ' premise', ' inference', ' hypotheses', '_fact', ' entail', ' факт', ' sentence', ' Statement', ' implication', ' imply', ' Statements', ' conclusion', '事實', ' assertion', '这句话', 'Statement']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 7. Sum of requested/applied delta norms: 8.152720/8.153608. Per-call margins and doses are in interventions.json.

Written by PI/OpenAI.
