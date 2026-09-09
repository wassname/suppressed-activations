#!/usr/bin/env bash
set -euo pipefail
uv run --offline scripts/oat_sweep.py --output-dir out/2026-09-09_local-c3-dog-name --target dog --sweep attenuation-local --condition-index 3 --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: What is the animal that spins webs called?
Answer: ' --target-prompt 'Question: What is the animal that barks and is called man'"'"'s best friend called?
Answer: ' --source-output Spider --target-output Dog --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.'
