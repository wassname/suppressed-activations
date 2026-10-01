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
reverse: false
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
elapsed_seconds: 5.31
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Readout-lens reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Lens fitted on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is 8 to 4. Positive answer_log_odds_shift favours 4 over 8; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Natural role-aligned generic donor mean addition at block15; final assistant-start prompt position, then0.25 strength on every cached decode. All prompts use the same nonthinking native-chat system frame. Previous literal-name donor retains its own norm; seed0 random matches the new donor norm and direction sign. Twelve conditions across three fixed development prompts; this call covers one. Both task frame and donor preparation changed. No current-input preparation, backward pass or later-layer feedback. Different natural norms prevent orientation-only attribution. Joint properties support assessment beyond a digit, not a universal success gate. Inspect exact text and retain wrong/capped outputs. Arithmetic should retain both4 and even; first-token log odds alone do not test joint consistency.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spider', ' dog').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                   |   answer_log_odds_shift |       p(4) |     p(8) |   answer_pair_mass |   r2 |
|:----------------------------|------------------------:|-----------:|---------:|-------------------:|-----:|
| Base                        |             1.93715e-07 | 0.00332051 | 0.920687 |           0.924007 |    0 |
| role-aligned donor          |             0.125       | 0.00376192 | 0.92051  |           0.924272 |    0 |
| previous literal-name donor |             0.25        | 0.00431205 | 0.931143 |           0.935455 |    0 |
| matched-random delta        |            -0.25        | 0.0026085  | 0.92869  |           0.931298 |    0 |

[Base](base/run.md)

# Base

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ';**', ' insects', ' Spider', '昆虫', ' claws', ';\\', ' venom', '爬', '；', ' crawling', '**;', '/web', ' insect', '两只', '-web', '四肢', '万只', ' mammals', '爬虫', '触角', '爬行', '肢', 'bugs', ' rept', '�', '蚣', ' humanoid']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0826352 | 0.920687    |             0 |
| 6       | -2.83264   | 0.0588575   |             0 |
| <       | -4.45764   | 0.0115897   |             0 |
| 4       | -5.70764   | 0.00332051  |             0 |
| eight   | -6.33264   | 0.00177734  |             0 |
| Eight   | -7.20764   | 0.000740907 |             0 |
| <think> | -7.83264   | 0.000396579 |             0 |
| 0       | -7.95764   | 0.00034998  |             0 |
| 1       | -8.14513   | 0.000290144 |             0 |
| <span   | -8.27013   | 0.000256051 |             0 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '<\\/', '；', '--;', '</tool_response>', '>;', ';;', '.;', '</', ' -->', ' <$', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', "';", '<<<<', '`;', ')', '؛', './.', ';.', '。']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[role-aligned donor](role-aligned-donor/run.md)

# role-aligned donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ';**', ' insects', '昆虫', ' Spider', ' claws', ';\\', '爬', ' venom', ' crawling', '；', '两只', '**;', '/web', '四肢', ' insect', ' mammals', '万只', '-web', '爬虫', 'bugs', ' rept', ' humanoid', '肢', '触角', '爬行', '蚣', '�']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0828269 | 0.92051     |  -0.000191726 |
| 6       | -2.83283   | 0.0588463   |  -0.000191689 |
| <       | -4.45783   | 0.0115875   |  -0.000191689 |
| 4       | -5.58283   | 0.00376192  |   0.124808    |
| eight   | -6.45783   | 0.0015682   |  -0.125192    |
| Eight   | -7.20783   | 0.000740765 |  -0.000191689 |
| 0       | -7.70783   | 0.000449297 |   0.249808    |
| <think> | -8.08283   | 0.000308797 |  -0.250191    |
| 1       | -8.08283   | 0.000308797 |   0.0623083   |
| <span   | -8.39533   | 0.000225921 |  -0.125192    |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '<\\/', '；', '--;', '>;', '</tool_response>', ';;', '.;', '</', ' -->', ' <$', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', '<<<<', "';", '。', '`;', './.', '؛', ')', ';.']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[previous literal-name donor](previous-literal-name-donor/run.md)

# previous literal-name donor

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', ';**', 'Spider', ' insects', '昆虫', ' Spider', ';\\', ' claws', '；', '**;', ' venom', '爬', ' crawling', ' mammals', '/web', '两只', ' insect', ' humanoid', '四肢', '*;', '万只', '肢', ' rept', '-web', '蚣', '爬虫', '触角', ' Creatures', '爬行']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0713423 | 0.931143    |     0.0112929 |
| 6       | -3.07134   | 0.0463589   |    -0.238707  |
| <       | -4.44634   | 0.0117214   |     0.0112929 |
| 4       | -5.44634   | 0.00431205  |     0.261293  |
| eight   | -6.07134   | 0.00230807  |     0.261293  |
| Eight   | -6.82134   | 0.00109026  |     0.386293  |
| 0       | -7.69634   | 0.000454486 |     0.261293  |
| <think> | -7.94634   | 0.000353954 |    -0.113707  |
| 1       | -8.13384   | 0.000293439 |     0.0112925 |
| <span   | -8.32134   | 0.000243269 |    -0.0512075 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '；', '--;', '>;', '<\\/', '.;', ';;', '</tool_response>', ' -->', ' <$', '</', ' <<<', '";', '<', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', "';", '؛', '`;', '。', '<<<<', ';.', './.', '.<']

Coverage: 4 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Prefill readout: [' spiders', '蜘蛛', ' spider', '蛛', 'Spider', ' insects', ';**', '昆虫', ' Spider', ' claws', ';\\', ' venom', '爬', ' crawling', '/web', '；', '四肢', ' insect', '两只', '**;', '万只', '-web', '触角', ' mammals', '爬虫', 'bugs', '肢', '蚣', '爬行', '�', ' humanoid', ' rept']

Generation (4 tokens):
```text
8; outside<|im_end|>
```

| token   |      log p |           p |   delta log p |
|:--------|-----------:|------------:|--------------:|
| 8       | -0.0739806 | 0.92869     |    0.0086546  |
| 6       | -2.94898   | 0.0523931   |   -0.116345   |
| <       | -4.44898   | 0.0116905   |    0.00865459 |
| 4       | -5.94898   | 0.0026085   |   -0.241345   |
| eight   | -6.57398   | 0.00139623  |   -0.241345   |
| Eight   | -7.32398   | 0.000659532 |   -0.116345   |
| <think> | -7.94898   | 0.000353022 |   -0.116345   |
| 0       | -8.19898   | 0.000274934 |   -0.241345   |
| 1       | -8.32398   | 0.000242628 |   -0.178845   |
| <span   | -8.38648   | 0.000227928 |   -0.116345   |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '</think>', ';', '<|im_start|>', '<think>', '.', '.Category', '<|file_sep|>', '--;', '<\\/', '；', '>;', '</tool_response>', ';;', '.;', ' -->', '</', ' <$', ' <<<', '<', '";', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', ';</', '<<<<', "';", '؛', '`;', './.', ';.', ')', '>>']

Coverage: 4 calls; prompt slice -1:, then one position per decode.
