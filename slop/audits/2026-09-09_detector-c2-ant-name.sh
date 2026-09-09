#!/usr/bin/env bash
# PREPARED, NOT QUEUED (GPU held; repro 862/863 first). Construction comparison:
# original-detector fixed-delta L20, window D8_20_32, matchedFalse (condition 2).
# Prompt argv byte-identical to fixed-band-ant-name record. -- PI/OpenAI
set -euo pipefail
uv run --offline 'scripts/oat_sweep.py' '--sweep' 'template-detector' '--condition-index' '2' '--target' 'ant' '--prompt-mode' 'chat-assistant-prefill' '--max-new-tokens' '128' '--output-dir' 'out/2026-09-09_detector-c2-ant-name' '--source-prompt' 'Question: What is the animal that spins webs called?
Answer: ' '--target-prompt' 'Question: What is the animal that lives in colonies and follows pheromone trails called?
Answer: ' '--source-output' 'Spider' '--target-output' 'Ant' '--prefill-instruction' 'Answer the question with the answer first. Then describe the animal in three sentences.' '--extraction-instruction' 'Complete the following fact, then explain your answer.'
