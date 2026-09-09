#!/usr/bin/env bash
# H2 per-layer yes/no decodability probe: dog and ant property. One GPU job. -- PI/[k3]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export HF_HUB_OFFLINE=1
rm -f h2_dog.json h2_ant.json
uv run --with pyarrow --with loguru --with accelerate scripts/h2_layer_probe.py \
  --target dog --source-prompt 'Question: Is the animal that spins webs a mammal?' \
  --target-prompt "Question: Is the animal that barks and is called man's best friend a mammal?" \
  --out h2_dog.json
uv run --with pyarrow --with loguru --with accelerate scripts/h2_layer_probe.py \
  --target ant --source-prompt 'Question: Does the animal that spins webs have antennae?' \
  --target-prompt 'Question: Does the animal that lives in colonies and follows pheromone trails have antennae?' \
  --out h2_ant.json
echo "BOTH DONE"
