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
relation: arithmetic_control
elapsed_seconds: 6.79
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours 4 over 8; arithmetic should preserve4, not maximize a shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Ordinary addition of the natural spider-minus-dog mean from eight fixed indirect descriptions, captured at final It. No runtime preparation, gradient, projection or fitted strength. Last prompt position plus quarter-strength continuous decode. Literal-name donor control retains its own natural norm; seed0 random matches the new donor norm. Different norms and prefix lengths prevent attributing a difference solely to semantic alignment. Ten generations across three properties; this call covers one. Arithmetic should retain4. Not component isolation.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Indirect-description donor preparation; ordinary unrescaled addition on two already-observed properties plus arithmetic. Eight fixed offline contexts; natural literal-name donor and seed0 norm-matched random controls. Ten generations total; no heldout cases consumed. Natural norm changes remain a confound. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 with a coherent continuation; no random arithmetic condition was run.

No standalone readout benchmark in this intervention run.

| condition                  |   answer_log_odds_shift |     p(4) |        p(8) |   answer_pair_mass |        r2 |
|:---------------------------|------------------------:|---------:|------------:|-------------------:|----------:|
| Base                       |                       0 | 0.985204 | 0.000544901 |           0.985749 | 0.0322581 |
| indirect-description donor |                       0 | 0.984637 | 0.000544587 |           0.985181 | 0.0645161 |

[Base](base/run.md)

# Base

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.', '5', '.\\', ' {}.', '++.', '3', '?.', '+.', '\\.', '.?', ' quart', ' fours', ' ?.', '{}.', '?\\', '四是', '.\\"', 'four', '?', '-four', ' FOUR', '().', ' fourth', '_.', ' ().', '6', '？', '四十', '___', '.*']

Generation (32 tokens):
```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0149069 | 0.985204    |             0 |
| 5       | -5.51491   | 0.0040263   |             0 |
| 2       | -5.63991   | 0.0035532   |             0 |
| 3       | -5.76491   | 0.00313569  |             0 |
| 1       | -6.51491   | 0.00148119  |             0 |
| 6       | -7.13991   | 0.000792826 |             0 |
| 8       | -7.51491   | 0.000544901 |             0 |
| 0       | -7.88991   | 0.000374504 |             0 |
|         | -8.01491   | 0.000330499 |             0 |
| 9       | -8.38991   | 0.000227148 |             0 |

Final-decode readout: [' analyze', 'analyze', '分析', '**', '**:', ' analyzes', ' Analy', '分析和', '分析一下', ')**', ':**', ' analyzing', ' analiz', '-**', '）**', ' analyzed', '):**', '分析的', ']**', '：**', ' Analyzer', ')**,', 'analysis', '*\\', '分析法', ';**', 'alyze', '分析了', ',**', 'analy', ' تحلیل', '的分析']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[indirect-description donor](indirect-description-donor/run.md)

# indirect-description donor

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.\\', '.', '++.', '\\.', '5', '3', '?.', ' {}.', '+.', '.?', ' fours', '?\\', ' quart', '四是', ' ?.', '?', '.\\"', 'four', '-four', ' FOUR', '_.', ' fourth', '{}.', '___', '.*', '6', ' ().', '().', '____', '？']

Generation (32 tokens):
```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>

</think>

Yes, the fact
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0154827 | 0.984637    |  -0.000575786 |
| 5       | -5.51548   | 0.00402398  |  -0.000576019 |
| 2       | -5.51548   | 0.00402398  |   0.124424    |
| 3       | -5.64048   | 0.00355115  |   0.124424    |
| 1       | -6.64048   | 0.0013064   |  -0.125576    |
| 6       | -7.14048   | 0.000792369 |  -0.000576019 |
| 8       | -7.51548   | 0.000544587 |  -0.000576019 |
|         | -8.07798   | 0.000310296 |  -0.063076    |
| 0       | -8.14048   | 0.000291496 |  -0.250576    |
| 7       | -8.45298   | 0.000213263 |  -0.000576019 |

Final-decode readout: [' facts', '事实', ' factual', ' Facts', 'facts', '的事实', ' fakta', '_fact', '事實', '事实和', ' Fakta', ' факты', ' Fakten', ' fatos', ' факт', ' Fakt', ' premise', '认定事实', ' факта', ' fakt', '_FACT', ' fato', '事実', ' statement', '上述事实', ' **', ' answer', ' hypothesis', ' **【', ' faptul', ' факти', '事实证明']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
