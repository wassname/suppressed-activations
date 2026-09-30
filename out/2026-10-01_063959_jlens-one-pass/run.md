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
relation: arithmetic_control
elapsed_seconds: 7.50
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 4. Positive answer_log_odds_shift favours 4 over 8; arithmetic should preserve4, not maximize a shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Fixed offline naming-gradient contrast addition, delta=(mean_spider-mean_dog) projected onto the unit mean VJP at It. VJPs use eight generic naming contexts, not the current input. No runtime gradients or later-layer feedback. Final prompt position receives delta; every decode receives0.25delta. Fixed seed0 random has the same requested norm. This is not literal component replacement; naming bias remains an alternative explanation. Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt. Arithmetic should retain4; its8/4 log-odds metric is diagnostic only.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Offline naming VJP projection; one frozen setting across two already-observed properties plus one arithmetic control. Eight generic preparatory contexts, no current-input preparation or dose selection. Eight generations total across the three properties; this call is one property. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: arithmetic remains4 with a coherent continuation; no random arithmetic condition was run.

No standalone readout benchmark in this intervention run.

| condition          |   answer_log_odds_shift |     p(4) |        p(8) |   answer_pair_mass |        r2 |
|:-------------------|------------------------:|---------:|------------:|-------------------:|----------:|
| Base               |                   0     | 0.985204 | 0.000544901 |           0.985749 | 0.0322581 |
| offline naming VJP |                   0.125 | 0.986494 | 0.000481503 |           0.986976 | 0.0322581 |

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

[offline naming VJP](offline-naming-vjp/run.md)

# offline naming VJP

Input:
```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Prefill readout: ['4', '__.', '.', '5', '.\\', ' {}.', '++.', '3', '+.', '?.', '\\.', '.?', ' quart', ' ?.', ' fours', '四是', '{}.', '?\\', 'four', '.\\"', '?', '-four', ' FOUR', ' fourth', '().', '_.', '6', ' ().', '四十', '？', '___', '____']

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
| 4       | -0.0135978 | 0.986494    |    0.00130908 |
| 5       | -5.6386    | 0.00355785  |   -0.123691   |
| 2       | -5.6386    | 0.00355785  |    0.00130892 |
| 3       | -5.8886    | 0.00277086  |   -0.123691   |
| 1       | -6.6386    | 0.00130886  |   -0.123691   |
| 6       | -7.2636    | 0.000700583 |   -0.123691   |
| 8       | -7.6386    | 0.000481503 |   -0.123691   |
| 0       | -8.0136    | 0.000330932 |   -0.123691   |
|         | -8.1386    | 0.000292046 |   -0.123691   |
| 7       | -8.5136    | 0.00020072  |   -0.0611906  |

Final-decode readout: [' analyze', 'analyze', '分析', '**', '**:', ' analyzes', ' Analy', '分析和', '分析一下', ')**', ':**', ' analyzing', ' analiz', '-**', '）**', ' analyzed', '):**', ']**', '分析的', '：**', ')**,', ' Analyzer', '*\\', 'analysis', ';**', '分析法', 'alyze', '分析了', ',**', 'analy', ' تحلیل', ' Analysis']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
