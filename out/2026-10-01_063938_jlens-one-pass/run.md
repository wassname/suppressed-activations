---
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
vjp_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt
country_swap: false
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: false
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: None
donor_checkpoint: None
donor_reflection: false
equal_donor_norm: false
relation: legs
elapsed_seconds: 10.45
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Fixed offline naming-gradient contrast addition, delta=(mean_spider-mean_dog) projected onto the unit mean VJP at It. VJPs use eight generic naming contexts, not the current input. No runtime gradients or later-layer feedback. Final prompt position receives delta; every decode receives0.25delta. Fixed seed0 random has the same requested norm. This is not literal component replacement; naming bias remains an alternative explanation. Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt. Arithmetic should retain4; its8/4 log-odds metric is diagnostic only.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Offline naming VJP projection; one frozen setting across two already-observed properties plus one arithmetic control. Eight generic preparatory contexts, no current-input preparation or dose selection. Eight generations total across the three properties; this call is one property. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |     p(4) |       p(8) |   answer_pair_mass |        r2 |
|:---------------------|------------------------:|---------:|-----------:|-------------------:|----------:|
| Base                 |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| offline naming VJP   |                   0.125 | 0.945985 | 0.00637399 |           0.952359 | 0.0322581 |
| matched-random delta |                   0.125 | 0.945995 | 0.00637406 |           0.952369 | 0.0322581 |

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

[offline naming VJP](offline-naming-vjp/run.md)

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

[matched-random delta](matched-random-delta/run.md)

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
