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
relation: skeleton_body
elapsed_seconds: 16.70
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Conditional donor reflection: u=unit(mean(target)-mean(source)), c=(mean(target)+mean(source))/2, a=(h-c)@u, h'=h-2*min(a,0)*u. Raw generic means; no dose rescaling or current-input preparation. This is a new method, not the reference sparse J-space clamp. Full-strength update is evaluated at every covered call, and can be zero on the target side. Natural full-donor addition is not norm matched. Random uses one seed0 direction with the proposed reflection norm from its own current state; later gates/doses are not trajectory matched. The clean-target diagnostic runs after this experiment's conditions and never controls editing.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                         |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:----------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                              |                    0    |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| conditional donor reflection      |                    0    |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| full donor contrast               |                   -0.25 |     0.223296 |      0.253027 |           0.476323 | 0         |
| matched-random reflection control |                    0    |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |

Clean source prefill donor margin: [1.1945807933807373]. Clean target margin: 1.415897. Expected source negative, target positive. [Post-intervention target diagnostic](clean_target_probe.json); no recentering or dose selection.

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

Source-side calls: 7; calls with nonzero applied updates: 0. Sum of requested/applied delta norms: 0.000000/0.000000. Per-call margins and doses are in interventions.json.

[conditional donor reflection](conditional-donor-reflection/run.md)

# conditional donor reflection

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

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', '?“', ' true', '?</', ' TRUE', '”?', ' logically', '?”,', '？”', ' **“', '?', '()?', '?",', '?)', 'true', ' logical', ')?', '?’', '.?', 'TRUE', '？', '?<', '?$', ' True', '?:', ' Logical', '?*', 'True']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 7. Sum of requested/applied delta norms: 6.920554/6.922254. Per-call margins and doses are in interventions.json.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', '___', ' lowest', '____', ' ____', ' upside', ' side', ' ________', ' lower', ' highest', '________', ' ___', ' _____', ' outer', ' inside', ' abdomen', ' bottom', '_____', ' ______', ' longest', '_.', ' middle', ' outskirts', ' left', '__.', ' __', ' right', '_\\', '__', ' downside', ' upper', ' skull']

Generation (32 tokens):
```text
 outside.
Question: Is the skeleton of the dog on the outside or inside?
Options:
A. outside
B. inside
C. not
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

Final-decode readout: [' wording', ' comparative', ' phrase', '-relative', ' comparison', ' logic', ' referring', ' relational', ' reasoning', ' phrases', ' comparisons', ' facts', ' analogy', ' comparing', ' referencing', ' terminology', ' Comparison', '_relative', ' refer', ' trivia', ' Phrase', ' paraph', ' factual', ' relativo', ' rhetorical', ' refers', ' synonyms', ' gramm', ' description', ' relativa', ' Comparative', ' reference']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 32. Sum of requested/applied delta norms: 45.770775/45.770494. Per-call margins and doses are in interventions.json.

[matched-random reflection control](matched-random-reflection-control/run.md)

# matched-random reflection control

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

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', ' TRUE', '?“', '?</', '”?', ' logically', ' **“', '？”', '?”,', '?', '()?', 'true', '?",', ' logical', 'TRUE', '?)', ')?', '.?', ' True', '?’', '?$', '？', '?<', ' truthful', '?:', 'True', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 7. Sum of requested/applied delta norms: 6.920554/6.921530. Per-call margins and doses are in interventions.json.
