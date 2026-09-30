---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_norm: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_reflection: true
equal_donor_norm: false
relation: legs
elapsed_seconds: 28.74
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Conditional donor reflection: u=unit(mean(target)-mean(source)), c=(mean(target)+mean(source))/2, a=(h-c)@u, h'=h-2*min(a,0)*u. Raw generic means; no dose rescaling or current-input preparation. This is a new method, not the reference sparse J-space clamp. Full-strength update is evaluated at every covered call, and can be zero on the target side. Natural full-donor addition is not norm matched. Random uses one seed0 direction with the proposed reflection norm from its own current state; later gates/doses are not trajectory matched. The clean-target diagnostic runs after this experiment's conditions and never controls editing.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                         |   answer_log_odds_shift |     p(4) |       p(8) |   answer_pair_mass |        r2 |
|:----------------------------------|------------------------:|---------:|-----------:|-------------------:|----------:|
| Base                              |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| conditional donor reflection      |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| full donor contrast               |                  -0.375 | 0.934653 | 0.0103831  |           0.945036 | 0.0322581 |
| matched-random reflection control |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |

Clean source prefill donor margin: [1.0815346240997314]. Clean target margin: 1.153284. Expected source negative, target positive. [Post-intervention target diagnostic](clean_target_probe.json); no recentering or dose selection.

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

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 8; calls with nonzero applied updates: 0. Sum of requested/applied delta norms: 0.000000/0.000000. Per-call margins and doses are in interventions.json.

[conditional donor reflection](conditional-donor-reflection/run.md)

# conditional donor reflection

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

Final-decode readout: [' hypothesis', ' statement', ' statements', '这段话', ' hypotheses', '这句话', 'Statement', ' Statement', ' Statements', 'statement', '這句話', ' implication', 'Statements', ' prediction', '陈述', ' inference', ' sentence', ' assertion', ' premise', ' deduction', ' Sentence', '?”,', ' hipote', '?”', '以上', ' assumption', '大胆的', ' выше', '同志为', ' Prediction', ' logical', ' idea']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 8; calls with nonzero applied updates: 8. Sum of requested/applied delta norms: 8.335337/8.334859. Per-call margins and doses are in interventions.json.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '爪子', ' mammals', ' dogs', ' animals', ' humans', 'dogs', ' canine', ' Dogs', '___', ' ears', '四肢', '尾巴', ' Animals', ' furry', ' tails', ' Humans', ' leash', '动物', ' teeth', '____', '兽医', ' pets', ' limbs', '犬', ' Gecko', ' bones', '爪', 'animals', '两只', ' mamm']

Generation (32 tokens):
```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the fact
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

Final-decode readout: [' facts', ' factual', ' Fakta', '事实', ' hypothesis', ' fakta', ' Facts', ' statement', '这段话', 'facts', '事实和', '上述事实', ' fatos', '的事实', ' факты', ' факт', '_fact', ' statements', ' hypotheses', ' inference', ' premise', ' sentence', '事實', '这句话', ' Fakten', ' implication', '這句話', ' Statement', ' entail', '陈述', ' факта', ' fato']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 32. Sum of requested/applied delta norms: 45.770775/45.770176. Per-call margins and doses are in interventions.json.

[matched-random reflection control](matched-random-reflection-control/run.md)

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
