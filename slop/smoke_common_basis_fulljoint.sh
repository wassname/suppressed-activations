#!/usr/bin/env bash
# Tiny smoke: full-temporal joint removal - support, containment, all sites, C0. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b19_smoke_fulljoint
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-fulljoint --condition-index "$1" \
    --output-dir "out/b19_smoke_fulljoint/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 fulljoint
run 1 top8joint
run 2 fulljoint_random
run 3 fulljointC0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b19_smoke_fulljoint')
rows = {n: json.loads((root/n/'result.json').read_text())['rows'][0]
        for n in ('fulljoint','top8joint','fulljoint_random','fulljointC0')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# C0 identity
assert rows['fulljointC0']['generation']['token_ids'] == rows['fulljointC0']['base_generation']['token_ids']
for n in ('fulljoint','top8joint','fulljoint_random'):
    p = rows[n]['persistence']
    assert p['removal_span'] == 'joint'
    assert p['interval_layers'] == [1, 2, 3, 4, 5]
    for k, r in rows[n]['intervention_record'].items():
        assert r['decode_steps'] == len(rows[n]['generation']['token_ids']) - 1
        assert r['perturbation_norm'] > 0
print('SMOKE PASS full-joint: support/containment asserts held, all sites, C0 identity')
PY
