#!/usr/bin/env bash
# Tiny real-path smoke: span-corrected delta C0 identity + random-control path. -- PI/Grok
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b12_smoke_span_C2_rand
SRC=$'Question: How many legs does the animal that spins webs have?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: How many legs does the animal that barks and is called man'"'"'s best friend have?\nAnswer: '
uv run --offline scripts/oat_sweep.py --sweep smoke-span-correction --condition-index 2 \
  --output-dir out/b12_smoke_span_C2_rand --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output 8 --target-output 4 --prefill-instruction "$INSTR"
python3 - <<'PY'
import json
from pathlib import Path
r=json.loads(Path('out/b12_smoke_span_C2_rand/result.json').read_text())['rows'][0]
assert r['config']['span_correction'] and r['config']['strength']==2.0
assert r['config']['random_delta_seed']==0
rec=list(r['intervention_record'].values())[0]
assert rec['perturbation_norm']>0, 'random control perturb must be nonzero'
# delta is a random direction norm-matched in the span: applied_norm should be >0
print('SMOKE RANDOM PASS pert', round(rec['perturbation_norm'],3))
PY
