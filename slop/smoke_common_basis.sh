#!/usr/bin/env bash
# Tiny real-path smoke: common-basis replacement h' = h + C (P_d d_p − P_s h_p). -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b13_smoke_common
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis --condition-index "$1" \
    --output-dir "out/b13_smoke_common/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 per_token
run 1 full_union
run 2 top8_union
run 3 random_shared8
run 4 C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b13_smoke_common')
rows = {name: json.loads((root / name / 'result.json').read_text())['rows'][0]
        for name in ('per_token', 'full_union', 'top8_union', 'random_shared8', 'C0')}
rec = {name: list(r['intervention_record'].values())[0] for name, r in rows.items()}
c0, others = rows['C0'], {k: v for k, v in rows.items() if k != 'C0'}
assert c0['config']['common_basis'] == 'per_token' and c0['config']['strength'] == 0.0
assert c0['generation']['token_ids'] == c0['base_generation']['token_ids'], 'C=0 not identity'
assert rec['C0']['perturbation_norm'] == 0.0
for name, r in others.items():
    assert r['config']['strength'] == 1.5 and r['config']['common_basis'] != 'none'
    assert rec[name]['perturbation_norm'] > 0, f'{name} did not edit'
    assert rec[name]['decode_steps'] == len(r['generation']['token_ids']) - 1
    assert len(rec[name]['replacement_trace']) == rec[name]['decode_steps'] + 1
    assert rec[name]['total_applied_norm'] > 0
    p = r['persistence']
    assert p['edit_equation'].startswith("h' = h + C (P_d d_p - P_s h_p)")
    assert len(p['donor_state_norms']) == 2  # positions=2, offsets 1..2
# C=0 exact-identity plus each construction editing: shape/coverage path verified
print('SMOKE PASS common-basis: identity + 4 constructions edit, coverage traced')
PY
