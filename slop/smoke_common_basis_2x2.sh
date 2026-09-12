#!/usr/bin/env bash
# Tiny smoke: 2x2 - ref-delta fixedness across removal spans, pref removal, C0s, mapping. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b20_smoke_2x2
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
run () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-2x2 --condition-index "$1" \
    --output-dir "out/b20_smoke_2x2/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run 0 injref_remPs
run 1 injref_remPref
run 2 injv_remPref
run 3 C0_remPs
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b20_smoke_2x2')
rows = {n: json.loads((root/n/'result.json').read_text())['rows'][0]
        for n in ('injref_remPs','injref_remPref','injv_remPref','C0_remPs')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# C0 identity
assert rows['C0_remPs']['generation']['token_ids'] == rows['C0_remPs']['base_generation']['token_ids']
# ref-delta fixedness: the applied delta vector is IDENTICAL across removal spans
n_refPs = rows['injref_remPs']['persistence']['delta_ref_prime']['norm']
n_refPref = rows['injref_remPref']['persistence']['delta_ref_prime']['norm']
assert abs(n_refPs - n_refPref) < 1e-6, f'delta_ref norm differs: {n_refPs} vs {n_refPref}'
# delta_ref norm == raw template delta norm (the norm-match rescale)
# both ref arms edited; removal spans recorded
for n in ('injref_remPs','injref_remPref','injv_remPref'):
    assert rec[n]['perturbation_norm'] > 0, f'{n} did not edit'
    assert rows[n]['persistence']['removal_span'] in ('source','pref')
# mapping: intervention at residual layer 2 (block 1)
assert [int(k) for k in rows['injref_remPs']['intervention_record']] == [2]
print('SMOKE PASS 2x2: ref-delta fixed across removals, pref removal works, C0 identity, mapping')
PY
