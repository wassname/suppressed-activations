#!/usr/bin/env bash
# Historical reproduction: synchronized-ant condition 011 on current HEAD.
# Prompt argv byte-identical to the recorded original; only --condition-index
# (single-condition run) and --output-dir differ. -- PI/OpenAI
set -euo pipefail
uv run --offline 'scripts/oat_sweep.py' '--sweep' 'synchronized-attenuation' '--condition-index' '11' '--target' 'ant' '--prompt-mode' 'chat-assistant-prefill' '--max-new-tokens' '128' '--output-dir' 'out/2026-09-09_repro-sync-ant-c011' '--source-prompt' 'Question: How many legs does the animal that spins webs have? Answer: ' '--target-prompt' 'Question: How many legs does the animal that lives in colonies and follows pheromone trails have? Answer: ' '--prefill-instruction' 'Complete the following fact. Then describe the animal in three sentences.' '--extraction-instruction' 'Complete the following fact, then explain your answer.'
