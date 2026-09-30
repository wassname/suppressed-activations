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
relation: skeleton_body
elapsed_seconds: 9.52
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Fixed offline naming-gradient contrast addition, delta=(mean_spider-mean_dog) projected onto the unit mean VJP at It. VJPs use eight generic naming contexts, not the current input. No runtime gradients or later-layer feedback. Final prompt position receives delta; every decode receives0.25delta. Fixed seed0 random has the same requested norm. This is not literal component replacement; naming bias remains an alternative explanation. Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt. Arithmetic should retain4; its8/4 log-odds metric is diagnostic only.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Offline naming VJP projection; one frozen setting across two already-observed properties plus one arithmetic control. Eight generic preparatory contexts, no current-input preparation or dose selection. Eight generations total across the three properties; this call is one property. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition            |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:---------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                 |                   0     |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| offline naming VJP   |                  -0.125 |     0.231157 |      0.231157 |           0.462314 | 0.0322581 |
| matched-random delta |                  -0.125 |     0.234368 |      0.234368 |           0.468735 | 0.0322581 |

[Base](base/run.md)

# Base

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', ' ___', '________', ' outer', ' bottom', ' _____', '_____', ' ______', ' skull', ' left', ' middle', '_.', ' right', ' upper', ' longest', ' bones', ' bone', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.36637 | 0.25503   |             0 |
| outside | -1.49137 | 0.225063  |             0 |
| left    | -3.24137 | 0.0391101 |             0 |
| right   | -3.55387 | 0.0286136 |             0 |
| ground  | -3.61637 | 0.02688   |             0 |
| surface | -3.80387 | 0.0222843 |             0 |
| far     | -3.92887 | 0.0196658 |             0 |
| end     | -4.05387 | 0.017355  |             0 |
| same    | -4.11637 | 0.0163035 |             0 |
| bottom  | -4.17887 | 0.0153157 |             0 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', '?“', ' TRUE', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', '?",', 'true', 'TRUE', ')?', '.?', '?)', ' logical', '?’', '？', '?$', ' True', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[offline naming VJP](offline-naming-vjp/run.md)

# offline naming VJP

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', '________', ' ___', ' outer', ' bottom', ' _____', '_____', ' ______', ' left', '_.', ' upper', ' right', ' middle', ' skull', ' bones', ' bone', ' longest', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.46466 | 0.231157  |     0.0267152 |
| inside  | -1.46466 | 0.231157  |    -0.0982848 |
| left    | -3.21466 | 0.040169  |     0.0267153 |
| right   | -3.46466 | 0.0312837 |     0.0892153 |
| ground  | -3.58966 | 0.0276078 |     0.0267153 |
| surface | -3.77716 | 0.0228876 |     0.0267153 |
| far     | -3.83966 | 0.0215009 |     0.0892153 |
| same    | -4.08966 | 0.0167449 |     0.0267153 |
| end     | -4.08966 | 0.0167449 |    -0.0357847 |
| bottom  | -4.15216 | 0.0157304 |     0.0267153 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', '?“', ' TRUE', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', '?",', 'true', 'TRUE', ')?', '?)', ' logical', '.?', '?’', '？', '?$', ' True', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', '________', ' ___', ' outer', ' bottom', ' _____', ' ______', '_____', ' skull', ' left', '_.', ' right', ' middle', ' upper', ' longest', ' bones', ' bone', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.45086 | 0.234368  |     0.0405091 |
| inside  | -1.45086 | 0.234368  |    -0.0844909 |
| left    | -3.26336 | 0.0382594 |    -0.0219908 |
| right   | -3.51336 | 0.0297965 |     0.0405092 |
| ground  | -3.57586 | 0.0279912 |     0.0405092 |
| surface | -3.76336 | 0.0232055 |     0.0405092 |
| far     | -3.88836 | 0.0204788 |     0.0405092 |
| same    | -4.07586 | 0.0169775 |     0.0405092 |
| end     | -4.07586 | 0.0169775 |    -0.0219908 |
| bottom  | -4.13836 | 0.0159489 |     0.0405092 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', ' TRUE', '?“', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', 'true', 'TRUE', '?",', ')?', '?)', ' logical', '.?', '?’', '？', ' True', '?$', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
