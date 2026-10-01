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
relation: skeleton_body
elapsed_seconds: 10.25
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Ordinary addition of the natural spider-minus-dog mean from eight fixed indirect descriptions, captured at final It. No runtime preparation, gradient, projection or fitted strength. Last prompt position plus quarter-strength continuous decode. Literal-name donor control retains its own natural norm; seed0 random matches the new donor norm. Different norms and prefix lengths prevent attributing a difference solely to semantic alignment. Ten generations across three properties; this call covers one. Arithmetic should retain4. Not component isolation.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Indirect-description donor preparation; ordinary unrescaled addition on two already-observed properties plus arithmetic. Eight fixed offline contexts; natural literal-name donor and seed0 norm-matched random controls. Ten generations total; no heldout cases consumed. Natural norm changes remain a confound. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                  |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:---------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                       |                    0    |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| indirect-description donor |                    0    |     0.237425 |      0.209527 |           0.446952 | 0.0322581 |
| literal-name donor control |                   -0.25 |     0.223296 |      0.253027 |           0.476323 | 0.0322581 |
| matched-random delta       |                    0    |     0.243081 |      0.214518 |           0.457599 | 0.0322581 |

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

[indirect-description donor](indirect-description-donor/run.md)

# indirect-description donor

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', '___', '____', ' ____', ' lowest', ' lower', ' ________', ' abdomen', '________', ' ___', ' bottom', ' highest', ' inside', ' outer', ' left', ' _____', ' ______', ' right', '_____', ' middle', ' outskirts', '_.', ' downside', ' upper', '__.', ' __', ' skull', ' _.', ' bones', '__']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |   log p |         p |   delta log p |
|:--------|--------:|----------:|--------------:|
| inside  | -1.4379 | 0.237425  |   -0.0715289  |
| outside | -1.5629 | 0.209527  |   -0.0715289  |
| left    | -3.0004 | 0.049767  |    0.240971   |
| right   | -3.3129 | 0.0364103 |    0.240971   |
| ground  | -3.6879 | 0.0250244 |   -0.0715289  |
| surface | -3.8129 | 0.022084  |   -0.00902891 |
| far     | -3.9379 | 0.019489  |   -0.00902891 |
| end     | -4.0629 | 0.017199  |   -0.00902891 |
| bottom  | -4.0629 | 0.017199  |    0.115971   |
| same    | -4.1254 | 0.016157  |   -0.00902891 |

Final-decode readout: ['?\\', '?**', '?”', '**?', ' true', '？**', ' TRUE', '?“', '?</', '”?', ' logically', '？”', 'true', '?', ' **“', '?”,', '()?', 'TRUE', ' True', '?",', ' logical', '?)', ')?', '.?', '?’', '？', '?$', '?<', 'True', ' truthful', '?:', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[literal-name donor control](literal-name-donor-control/run.md)

# literal-name donor control

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', '___', ' lowest', '____', ' ____', ' upside', ' side', ' ________', ' lower', ' highest', '________', ' ___', ' _____', ' outer', ' inside', ' abdomen', ' bottom', '_____', ' ______', ' longest', '_.', ' middle', ' outskirts', ' left', '__.', ' __', ' right', '_\\', '__', ' downside', ' upper', ' skull']

Generation (32 tokens):
```text
 outside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the inside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.37426 | 0.253027  |    0.117117   |
| inside  | -1.49926 | 0.223296  |   -0.132883   |
| left    | -3.31176 | 0.0364521 |   -0.0703831  |
| ground  | -3.56176 | 0.0283889 |    0.0546169  |
| surface | -3.62426 | 0.0266689 |    0.179617   |
| right   | -3.68676 | 0.0250531 |   -0.132883   |
| far     | -3.93676 | 0.0195114 |   -0.00788307 |
| end     | -4.06176 | 0.0172187 |   -0.00788307 |
| same    | -4.12426 | 0.0161755 |   -0.00788307 |
| bottom  | -4.12426 | 0.0161755 |    0.0546169  |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' TRUE', '?“', ' true', '?</', '”?', ' logically', '?', '?”,', '？”', ' **“', '()?', ' logical', 'true', '?",', 'TRUE', '?’', ')?', '?)', '?<', '？', '?$', ' True', '.?', ' Logical', '?:', 'True', '?*']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', ' lower', ' ____', '____', ' highest', ' ________', ' abdomen', ' inside', ' bottom', ' ___', '________', ' _____', ' outer', ' left', '_____', '_.', ' bones', ' ______', ' right', ' upper', ' skull', ' downside', ' bone', ' middle', ' outskirts', ' longest', ' same', '__.']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.41436 | 0.243081  |    -0.0479877 |
| outside | -1.53936 | 0.214518  |    -0.0479877 |
| left    | -3.10186 | 0.0449654 |     0.139513  |
| right   | -3.35186 | 0.0350191 |     0.202013  |
| ground  | -3.53936 | 0.0290319 |     0.0770125 |
| surface | -3.97686 | 0.0187444 |    -0.172987  |
| end     | -4.03936 | 0.0176087 |     0.0145125 |
| bottom  | -4.10186 | 0.0165419 |     0.0770125 |
| far     | -4.10186 | 0.0165419 |    -0.172987  |
| same    | -4.10186 | 0.0165419 |     0.0145125 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', '?“', ' true', '?</', ' TRUE', '”?', ' logically', ' **“', '？”', '?”,', '?', '()?', '?",', '?)', ' logical', '.?', ')?', '?’', 'true', '？', 'TRUE', '?$', '?<', '?:', ' True', ' truthful', '?*', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
