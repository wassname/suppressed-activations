#!/usr/bin/env bash
# Tiny real-path smoke: span-corrected delta C=0 identity. -- PI/Grok
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b11_smoke_span_C0 out/b11_smoke_span_C2
SRC=$'Question: What is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: What is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
uv run --offline scripts/oat_sweep.py --sweep smoke-span-correction --condition-index 0 \
  --output-dir out/b11_smoke_span_C0 --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
uv run --offline scripts/oat_sweep.py --sweep smoke-span-correction --condition-index 1 \
  --output-dir out/b11_smoke_span_C2 --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
python3 - <<'PY'
import json
from pathlib import Path
c0=json.loads(Path('out/b11_smoke_span_C0/result.json').read_text())['rows'][0]
c2=json.loads(Path('out/b11_smoke_span_C2/result.json').read_text())['rows'][0]
assert c0['config']['span_correction'] and c0['config']['strength']==0.0
assert c0['generation']['token_ids']==c0['base_generation']['token_ids'], 'C=0 not identity'
assert list(c0['intervention_record'].values())[0]['perturbation_norm']==0.0
assert c2['config']['strength']==2.0
assert list(c2['intervention_record'].values())[0]['perturbation_norm']>0
print('SMOKE PASS C0 identity, C2 pert', list(c2['intervention_record'].values())[0]['perturbation_norm'])
PY
