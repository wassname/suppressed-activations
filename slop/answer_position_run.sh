#!/usr/bin/env bash
# Answer-position displacement probe: prop-dog C=1.5 and prop-ant C=1.0 (positive control).
# One GPU job; loads model per animal via the probe. -- PI/[k3]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export HF_HUB_OFFLINE=1
DIR="slop/sota_ap"
mkdir -p "$DIR"
# prop-dog: source spider mammal? -> target dog mammal? (expect Yes). C=1.5.
uv run --with pyarrow --with loguru --with accelerate scripts/answer_position_probe.py \
  --prompt 'Question: Is the animal that spins webs a mammal?' \
  --target-prompt "Question: Is the animal that barks and is called man's best friend a mammal?" \
  --target dog --c-target 1.5 --out "$DIR/ap_prop_dog.json" --peak-layer 20 --output-layer 32
# prop-ant: source spider antennae? -> target ant antennae? (expect Yes, transferred at C=1.0). C=1.0.
uv run --with pyarrow --with loguru --with accelerate scripts/answer_position_probe.py \
  --prompt 'Question: Does the animal that spins webs have antennae?' \
  --target-prompt 'Question: Does the animal that lives in colonies and follows pheromone trails have antennae?' \
  --target ant --c-target 1.0 --out "$DIR/ap_prop_ant.json" --peak-layer 20 --output-layer 32
echo "BOTH DONE"
cat "$DIR"/*.json
