# Demo evidence manifest (historical Question-family full continuations)

Snapshots of the exact strings and settings shown in the README historical section.
Source of truth: batchwork worktree replay runs (development regression evidence,
heavily exposed: 12-29 runs each, never merged into the fresh evaluation set).

- legs-dog.json <- batchwork out/2026-09-10_replay-C1.5-legs-dog/result.json
  sha256 d9e5d8db0f63...
- legs-ant.json <- batchwork out/2026-09-10_replay-C1.5-legs-ant/result.json
  sha256 a9f5ba3ead2c...

Adjudication: slop/eval_fresh_adjudications.json (batchwork) - fresh-set candidate
6/12 primary pass, random control 1/12, machine-verified quotes, PI[claude].
Settings (both rows): Qwen/Qwen3.5-4B rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a,
rank 8, detector layers 18/20/32, intervention layer 20 (h20), 3 positions,
strength 1.5, match_component_norm true (recorded) with the branch not reading it,
restore_residual_norm false, continue_generation true, chat-assistant-prefill mode.
Reconstructed edit: h' = h + C(Delta - U U^T h) with no component-norm matching and
no residual renormalization in the executed branch. Base 58 tokens; dog 65; ant 65;
all end <|im_end|>. Byte/string/token verification (CPU only): batchwork
slop/research/demo-evidence/cpu-string-validation.txt (copy; original in batchwork .local/verify_logs/demo-evidence/).

Reconstructed and written by PI[glm-5p3-flash], 2026-09-13.

## Details moved off the main page (2026-09-13 burden reduction)

- Random-donor control on the fresh set: 1/12.
- The replay rows are development-exposed (12-29 runs each per row family) and are not
  pooled into the fresh-set score.
- The dog answer's "short history" sentence is factually weak (dog domestication
  predates most recorded history).
- The layer-20 family and the C=4 demo (layer 26, single final-token patch) are separate
  experiments; results are not pooled.
