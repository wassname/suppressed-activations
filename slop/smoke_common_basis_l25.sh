#!/usr/bin/env bash
# Tiny real-path smoke: L25-family common-basis (intervention at tiny output layer). -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b14_smoke_common_l25
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-l25 --condition-index "$1" \
    --output-dir "out/b14_smoke_common_l25/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 per_token
run 1 full_union
run 2 C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b14_smoke_common_l25')
rows = {n: json.loads((root / n / 'result.json').read_text())['rows'][0]
        for n in ('per_token', 'full_union', 'C0')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids'], 'C=0 not identity'
assert rec['C0']['perturbation_norm'] == 0.0
for n in ('per_token', 'full_union'):
    assert rec[n]['perturbation_norm'] > 0, f'{n} did not edit'
    assert rec[n]['decode_steps'] == len(rows[n]['generation']['token_ids']) - 1
    p = rows[n]['persistence']
    assert p['intervention_layer'] == 4
    assert 'state_norms_L20_L25' in p, 'layer-norm diagnostics missing'
    assert p['state_norms_L20_L25'] == {}, 'tiny model should skip L20/L25 diagnostics'
    assert 'union_support' in p
print('SMOKE PASS l25-family: identity + edits + coverage; layer diagnostics guarded')
PY
