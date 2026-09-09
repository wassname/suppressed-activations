#!/usr/bin/env bash
# Tiny real-path smoke for span-correction-sweep: C=1 and in-span projected random. -- PI/[k3]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b13_smoke_C1 out/b13_smoke_inspan
SRC=$'Question: How many legs does the animal that spins webs have?\nAnswer: '
INS='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: How many legs does the animal that barks and is called man'"'"'s best friend have?\nAnswer: '
uv run --offline scripts/oat_sweep.py --sweep smoke-span-correction --condition-index 3 \
  --output-dir out/b13_smoke_C1 --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output 8 --target-output 4 --prefill-instruction "$INS"
uv run --offline scripts/oat_sweep.py --sweep smoke-span-correction --condition-index 4 \
  --output-dir out/b13_smoke_inspan --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output 8 --target-output 4 --prefill-instruction "$INS"
python3 - <<'PY'
import json
from pathlib import Path
c1=json.loads(Path('out/b13_smoke_C1/result.json').read_text())['rows'][0]
ci=json.loads(Path('out/b13_smoke_inspan/result.json').read_text())['rows'][0]
assert c1['config']['span_correction'] and c1['config']['strength']==1.0 and not c1['config']['random_in_span']
assert ci['config']['span_correction'] and ci['config']['strength']==2.0 and ci['config']['random_in_span']
rec1=list(c1['intervention_record'].values())[0]
reci=list(ci['intervention_record'].values())[0]
assert rec1['perturbation_norm']>0 and reci['perturbation_norm']>0
# in-span random delta is projected into U: its applied norm should reflect in-span magnitude
print('C1 pert', round(rec1['perturbation_norm'],3), '| inspan C2 pert', round(reci['perturbation_norm'],3))
print('SMOKE PASS: C=1 and in-span random paths run')
PY
