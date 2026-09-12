#!/usr/bin/env bash
# Tiny smoke: ablation arms - injection-only, removal-only, A replay, C0; same applied delta. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b22_smoke_ablation
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-ablation --condition-index "$1" \
    --output-dir "out/b22_smoke_ablation/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 injection_only
run 1 removal_only
run 2 A_replay
run 3 C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b22_smoke_ablation')
rows = {n: json.loads((root/n/'result.json').read_text())['rows'][0]
        for n in ('injection_only','removal_only','A_replay','C0')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# C0 identity
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids']
# applied delta VECTOR equality across injection-only / A (same runtime, same construction)
h_inj = rows['injection_only']['persistence']['applied_delta_sha256']
h_A = rows['A_replay']['persistence']['applied_delta_sha256']
assert h_inj == h_A, 'applied delta vectors differ between arms'
# ops engaged: injection-only = additive (perturbation > 0), removal-only = removal
assert rec['injection_only']['perturbation_norm'] > 0
assert rec['removal_only']['perturbation_norm'] > 0
# removal-only removes: no delta hash change... both have hashes (same delta computed) but
# removal-only does not APPLY it - sanity: the removal-only equation has no additive term
assert rows['removal_only']['config']['removal_only'] is True
assert rows['injection_only']['config']['removal_only'] is False
# mapping: layer 2 residual
assert [int(k) for k in rows['injection_only']['intervention_record']] == [2]
print('SMOKE PASS ablation: applied-delta vector equality (injection-only == A), removal-only engaged, C0 identity')
PY
