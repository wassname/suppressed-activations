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
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: legs
expected_answer: '8'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -2.875
answer_pair_mass: 0.8501598834991455
swap_log_odds_shift: -2.875
bare_answer_mass: 0.8501598834991455
r2: 0.032258064516129004
---
# full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', ' mammals', '爪子', ' dogs', 'dogs', ' animals', ' ears', ' tails', '兽医', ' Dogs', '___', ' canine', ' teeth', '四肢', ' bones', ' furry', ' Animals', ' humans', '尾巴', ' Gecko', '爪', ' pets', ' leash', ' veterinary', '动物', ' limbs', ' veterin', '____', ' mamm', '四条', ' jaws']

Generation (32 tokens):
```text
4.
Question: How many legs does a dog have?
Answer:

<think>
Thinking Process:

1.  **Analyze the Request:**
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.289259 | 0.748818   |     -0.231183 |
|       8 | -2.28926  | 0.101342   |      2.64382  |
|       6 | -3.03926  | 0.0478703  |      2.14382  |
|       1 | -3.16426  | 0.0422454  |      1.26882  |
|       2 | -3.91426  | 0.0199553  |      0.393816 |
|       3 | -4.28926  | 0.0137151  |      0.768816 |
|       0 | -4.66426  | 0.00942623 |      0.268816 |
|       5 | -4.91426  | 0.00734116 |      1.26882  |
|       7 | -5.53926  | 0.00392944 |      1.51882  |
|       9 | -5.53926  | 0.00392944 |      1.51882  |

Final-decode readout: ['\\":', '”:', '**:', '*:', '`:', ':**', '$:', '":', '’:', '):', ':\\', '»:', ':*', "':", '}:', '):\\', ' **:', ']:', '.):', ':</', ' }:', ':', ':`', ' ):', '>:', ':$', ':\\\\', ':<', '.:', '):**', '():', ':")']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
