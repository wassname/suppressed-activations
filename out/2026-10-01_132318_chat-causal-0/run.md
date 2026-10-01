---
reflection_coordinate_checkpoint: None
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
vjp_checkpoint: None
indirect_donor: false
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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_132306_jlens-one-pass/donors.pt
donor_reflection: false
equal_donor_norm: false
relation: joint_properties
elapsed_seconds: 8.14
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 4 to 8. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. Previous literal-name donor retains its own norm; seed0 random matches the new donor norm and direction sign. Twelve conditions across three fixed development prompts; this call covers one. Both task frame and donor preparation changed. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 4 toward 8 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                   |   answer_log_odds_shift |     p(4) |        p(8) |   answer_pair_mass |   r2 |
|:----------------------------|------------------------:|---------:|------------:|-------------------:|-----:|
| Base                        |                  0      | 0.980738 | 1.74364e-05 |           0.980755 |    0 |
| role-aligned donor          |                 -0.0625 | 0.980628 | 1.85589e-05 |           0.980647 |    0 |
| previous literal-name donor |                 -0.4375 | 0.978527 | 2.69451e-05 |           0.978554 |    0 |
| matched-random delta        |                 -0.1875 | 0.979867 | 2.10136e-05 |           0.979888 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ' mammals', ' humanoid', ';', ' humans', '**;', ' Humans', ';\\', ';;', '四肢', ';$', 'Humans', '__;', '人类的', '_;', '__:', ';</', 'animals', '*;', '.;', '»;', '%;', ' Animals', '人类', '>;', 'dogs', ' animals', '两只', ' paw', '动物', '؛']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0194503 | 0.980738    |             0 |
| <       | -4.26945   | 0.0139895   |             0 |
| 2       | -6.39445   | 0.0016708   |             0 |
| 0       | -6.76945   | 0.00114833  |             0 |
| 3       | -7.51945   | 0.000542431 |             0 |
| ;       | -8.33195   | 0.000240702 |             0 |
| Four    | -8.39445   | 0.000226119 |             0 |
| 1       | -8.64445   | 0.000176101 |             0 |
| four    | -8.89445   | 0.000137148 |             0 |
| <think> | -8.89445   | 0.000137148 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', '`;', ';.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>;', '";', ';;', '</tool_response>', ';**', '.;', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[role-aligned donor](role-aligned-donor/run.md)

# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', ' mammals', ' humanoid', ';\\', '**;', ';;', ' humans', ';$', ' Humans', '四肢', '__;', 'Humans', '.;', '*;', '_;', ';</', '»;', '%;', '人类的', ' paw', '>;', ' Animals', 'animals', '__:', '؛', 'dogs', '人类', ' animals', '两只', '";']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0195618 | 0.980628    |   -0.00011153 |
| <       | -4.26956   | 0.0139879   |   -0.00011158 |
| 2       | -6.39456   | 0.00167062  |   -0.00011158 |
| 0       | -6.76956   | 0.0011482   |   -0.00011158 |
| 3       | -7.51956   | 0.00054237  |   -0.00011158 |
| ;       | -8.20706   | 0.000272721 |    0.124888   |
| Four    | -8.33206   | 0.000240675 |    0.0623884  |
| 1       | -8.64456   | 0.000176082 |   -0.00011158 |
| <think> | -8.70706   | 0.000165414 |    0.187388   |
| four    | -8.83206   | 0.000145977 |    0.0623884  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '`;', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '";', '>;', ';;', '</tool_response>', ';**', '.;', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[previous literal-name donor](previous-literal-name-donor/run.md)

# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ' mammals', ' humanoid', ' humans', '四肢', ' Humans', 'Humans', ';', ';\\', '**;', ';;', ';$', '人类', 'animals', '人类的', ' paw', '__;', ' Animals', ' animals', '两只', 'dogs', '动物', '__:', ' claws', ';</', '»;', '_;', '*;', '%;', '.;', '双腿']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0217072 | 0.978527    |   -0.00225691 |
| <       | -4.14671   | 0.0158164   |    0.122743   |
| 2       | -6.52171   | 0.00147116  |   -0.127257   |
| 0       | -6.64671   | 0.00129829  |    0.122743   |
| 3       | -7.39671   | 0.000613269 |    0.122743   |
| ;       | -8.02171   | 0.000328259 |    0.310243   |
| 1       | -8.39671   | 0.000225609 |    0.247743   |
| Four    | -8.52171   | 0.000199099 |   -0.127257   |
| <think> | -8.64671   | 0.000175704 |    0.247743   |
| four    | -8.95921   | 0.000128548 |   -0.0647573  |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '`;', '";', '</tool_response>', ';;', '>;', ';**', ' -->', '.;', "';", '*;', '<', '</', ' <<<', '<\\/', '؛', ';<', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [';**', '；', ';', '**;', ' humanoid', ' mammals', ';;', ';\\', ' humans', ';$', ' Humans', '__;', '四肢', 'Humans', '_;', '*;', ';</', '.;', '»;', '%;', '>;', '人类的', '__:', ' {};', '؛', '人类', '";', ' [];', ' Animals', 'animals', '`;', ' animals']

Generation (4 tokens):
```text
4; inside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 4       | -0.0203389 | 0.979867    |  -0.000888612 |
| <       | -4.27034   | 0.013977    |  -0.000888824 |
| 2       | -6.27034   | 0.00189159  |   0.124111    |
| 0       | -6.52034   | 0.00147317  |   0.249111    |
| 3       | -7.39534   | 0.000614108 |   0.124111    |
| ;       | -8.14534   | 0.000290084 |   0.186611    |
| Four    | -8.20784   | 0.000272509 |   0.186611    |
| 1       | -8.52034   | 0.000199372 |   0.124111    |
| four    | -8.64534   | 0.000175945 |   0.249111    |
| <think> | -8.83284   | 0.000145864 |   0.0616112   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '.', '<think>', '<|file_sep|>', '.Category', '**;', '**', '；', '--;', ';.', '`;', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '>;', '";', '</tool_response>', ';;', '.;', ';**', ' -->', "';", '<', '*;', '</', ';<', '؛', ' <<<', '<\\/', ';charset']

Coverage: 4 calls; prompt slice -1:, then one position per decode.
