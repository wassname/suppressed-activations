---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
block_index: 15
n_prompts: 8
---
# Offline donor calibration

Written by PI/OpenAI.

Four fixed generic prompts per concept, no experimental questions or answer labels. Raw last-position residual means; no normalisation or fitted strength. No experimental input was run.

SHOULD: means differ. Observed difference norm=1.071719. This does not establish useful steering.

| concept   | input repr                                                                                                                                                        |   residual norm |
|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------:|
| Sweden    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nConsider Sweden.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'     |         9.08537 |
| Sweden    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFocus on Sweden.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'     |         9.13523 |
| Sweden    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nPicture Sweden.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'      |         9.38958 |
| Sweden    | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nKeep Sweden in mind.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n' |         9.01693 |
| Japan     | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nConsider Japan.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'      |         9.17286 |
| Japan     | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFocus on Japan.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'      |         9.30509 |
| Japan     | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nPicture Japan.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'       |         9.41404 |
| Japan     | '<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nKeep Japan in mind.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'  |         9.01275 |

Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/donors.pt
run.md: /workspace/2026/suppressed-activations/out/2026-10-01_154008_jlens-one-pass/run.md
