#!/usr/bin/env bash
# Tiny smoke: joint-removal/restricted algebra, support asserts, six-site equivalent, C0. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b18_smoke_joint
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-joint --condition-index "$1" \
    --output-dir "out/b18_smoke_joint/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 original
run 1 joint_removal
run 2 restricted_inject
run 3 joint_C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b18_smoke_joint')
rows = {n: json.loads((root/n/'result.json').read_text())['rows'][0]
        for n in ('original','joint_removal','restricted_inject','joint_C0')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# C0 identity (joint removal path)
assert rows['joint_C0']['generation']['token_ids'] == rows['joint_C0']['base_generation']['token_ids']
assert all(r['perturbation_norm'] == 0.0 for r in rows['joint_C0']['intervention_record'].values())
for n in ('original','joint_removal','restricted_inject'):
    assert rec[n]['perturbation_norm'] > 0, f'{n} did not edit'
    p = rows[n]['persistence']
    assert p['interval_layers'] == [1, 2, 3, 4, 5]  # tiny interval = all 5 boundaries
    if n == 'joint_removal':
        assert p['removal_span'] == 'joint' and p['removal_rank'] >= 8
    if n == 'restricted_inject':
        assert p['inject_restricted'] and p['removal_span'] == 'source'
    # multi-site coverage: all interval layers recorded decode steps
    for k, r in rows[n]['intervention_record'].items():
        assert r['decode_steps'] == len(rows[n]['generation']['token_ids']) - 1
print('SMOKE PASS joint/restricted: algebra paths, support asserts, interval coverage, C0 identity')
PY
