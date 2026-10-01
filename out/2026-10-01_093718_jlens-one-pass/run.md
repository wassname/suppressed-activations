---
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
vjp_checkpoint: None
indirect_donor: true
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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/donors.pt
donor_reflection: false
equal_donor_norm: false
relation: legs
elapsed_seconds: 10.84
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Ordinary addition of the natural spider-minus-dog mean from eight fixed indirect descriptions, captured at final It. No runtime preparation, gradient, projection or fitted strength. Last prompt position plus quarter-strength continuous decode. Literal-name donor control retains its own natural norm; seed0 random matches the new donor norm. Different norms and prefix lengths prevent attributing a difference solely to semantic alignment. Ten generations across three properties; this call covers one. Arithmetic should retain4. Not component isolation.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Indirect-description donor preparation; ordinary unrescaled addition on two already-observed properties plus arithmetic. Eight fixed offline contexts; natural literal-name donor and seed0 norm-matched random controls. Ten generations total; no heldout cases consumed. Natural norm changes remain a confound. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                  |   answer_log_odds_shift |     p(4) |       p(8) |   answer_pair_mass |        r2 |
|:---------------------------|------------------------:|---------:|-----------:|-------------------:|----------:|
| Base                       |                   0     | 0.943579 | 0.00720431 |           0.950783 | 0.0322581 |
| indirect-description donor |                  -0.125 | 0.944299 | 0.00816978 |           0.952468 | 0.0322581 |
| literal-name donor control |                  -0.375 | 0.934653 | 0.0103831  |           0.945036 | 0.0322581 |
| matched-random delta       |                   0     | 0.941424 | 0.00718786 |           0.948612 | 0.0322581 |

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

[indirect-description donor](indirect-description-donor/run.md)

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

[literal-name donor control](literal-name-donor-control/run.md)

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

[matched-random delta](matched-random-delta/run.md)

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
