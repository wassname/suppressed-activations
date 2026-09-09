#!/usr/bin/env bash
# CPU real-path check: fresh vs shared-model batch on tiny model. Worktree scratch.
# Fresh argv is generated from slop/b09_batch_spec.json (single source of truth).
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu SUPPRESSED_LOAD_LOG=$PWD/slop/b09_load_calls.log
export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=24 MKL_NUM_THREADS=24
rm -f slop/b09_load_calls.log
rm -rf out/b09_cpu_fresh_dog out/b09_cpu_fresh_ant out/b09_cpu_batch_dog out/b09_cpu_batch_ant out/b09_cpu_batch_dog_repeat
eval "$(python3 slop/b08_fresh_argv.py slop/b09_batch_spec.json 0 out/b09_cpu_fresh_dog dog)"
eval "$(python3 slop/b08_fresh_argv.py slop/b09_batch_spec.json 1 out/b09_cpu_fresh_ant ant)"
uv run --offline scripts/oat_sweep.py --batch-spec slop/b09_batch_spec.json
python3 slop/b09_compare.py
