---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
block_index: 15
n_prompts: 8
---
# Offline donor calibration

Written by PI/OpenAI.

Four fixed generic templates per animal, no leg-count question or answer labels. Raw last-position residual means; no normalisation or fitted strength. No experimental input was run.

SHOULD: means differ. Observed difference norm=0.920599. This does not establish useful steering.

| concept   | input repr                                                                                                                                                          |   residual norm |
|:----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------:|
| spider    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nConsider a spider.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'     |         9.08589 |
| spider    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFocus on a spider.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'     |         9.26172 |
| spider    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nPicture a spider.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'      |         9.248   |
| spider    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nKeep a spider in mind.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n' |         9.1077  |
| dog       | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nConsider a dog.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'        |         9.08389 |
| dog       | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFocus on a dog.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'        |         9.2794  |
| dog       | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nPicture a dog.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'         |         9.18537 |
| dog       | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nKeep a dog in mind.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'    |         9.08487 |

Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_132306_jlens-one-pass/donors.pt
run.md: /workspace/2026/suppressed-activations/out/2026-10-01_132306_jlens-one-pass/run.md
