#!/usr/bin/env bash
# Historical reproduction: local-dog condition 003 on current HEAD.
# Prompt argv byte-identical to the recorded original; only --condition-index
# (single-condition run) and --output-dir differ. -- PI/OpenAI
set -euo pipefail
uv run --offline 'scripts/oat_sweep.py' '--sweep' 'attenuation-local' '--condition-index' '3' '--target' 'dog' '--prompt-mode' 'chat-assistant-prefill' '--max-new-tokens' '128' '--output-dir' 'out/2026-09-09_repro-local-dog-c003' '--source-prompt' 'Fact: The animal that spins webs is called a' '--target-prompt' 'Fact: The animal that barks is called a' '--source-output' ' spider' '--target-output' ' dog' '--prefill-instruction' 'Complete the following fact. Then describe the animal in three sentences.' '--extraction-instruction' 'Complete the following fact, then explain your answer.'
