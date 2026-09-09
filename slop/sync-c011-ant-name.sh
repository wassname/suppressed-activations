#!/usr/bin/env bash
set -euo pipefail
uv run --offline scripts/oat_sweep.py --output-dir out/2026-09-09_sync-c011-ant-name --target ant --sweep synchronized-attenuation --condition-index 11 --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: What is the animal that spins webs called?
Answer: ' --target-prompt 'Question: What is the animal that lives in colonies and follows pheromone trails called?
Answer: ' --source-output Spider --target-output Ant --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.'
