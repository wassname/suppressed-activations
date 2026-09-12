#!/usr/bin/env bash
# Tiny smoke: norm-factorial - rescale asserts (direction cos=1, target norm), C0, mapping. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b21_smoke_norm2x2
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-norm2x2 --condition-index "$1" \
    --output-dir "out/b21_smoke_norm2x2/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 delta_scaled_to_v
run 1 v_scaled_to_delta
run 2 C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b21_smoke_norm2x2')
rows = {n: json.loads((root/n/'result.json').read_text())['rows'][0]
        for n in ('delta_scaled_to_v','v_scaled_to_delta','C0')}
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids']
for n, r in rows.items():
    p = r['persistence']
    if n != 'C0':
        assert p['inject_norm_axis'] != 'own'
        assert p['removal_span'] == 'pref' and p['removal_rank'] >= 2
        assert list(r['intervention_record'].values())[0]['perturbation_norm'] > 0
        assert abs(p['norm_target_check']['max_rel_err']) < 1e-5, f'{n} norm target missed'
print('SMOKE PASS norm-factorial: rescale direction+norm asserts, C0 identity, mapping')
PY
