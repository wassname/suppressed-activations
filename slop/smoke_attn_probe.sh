#!/usr/bin/env bash
# Tiny smoke for the property-answer attention dump probe. -- PI/[k3]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
uv run --offline python slop/property_attention_probe.py \
  --prompt 'Question: Is the animal that spins webs a mammal?\nAnswer: ' \
  --out slop/b14_attn_dump.json --max-new-tokens 2
python3 - <<'PY'
import json
from pathlib import Path
d=json.loads(Path('slop/b14_attn_dump.json').read_text())
assert 'answer_position_attention' in d and d['answer_position_attention'] is not None
assert 'top_k' in d and len(d['top_k'])>=3
print('SMOKE PASS: attention dump probe ran;',
      'answer pos', d.get('answer_position'), 'top1', d['top_k'][0])
PY
