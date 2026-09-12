#!/usr/bin/env bash
# Tiny smoke: interval re-correction — multi-site hooks, C0 identity, per-layer donor mapping,
# final-layer coverage. Tiny model: 5 blocks, interval = h1..h5 (5 sites; the real interval
# is 6 sites h25..h30, verified in the family definition + batch assertions). -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b17_smoke_interval
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-interval --condition-index 0 \
  --output-dir out/b17_smoke_interval/interval --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-interval --condition-index 1 \
  --output-dir out/b17_smoke_interval/C0 --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b17_smoke_interval')
iv = json.loads((root/'interval/result.json').read_text())['rows'][0]
c0 = json.loads((root/'C0/result.json').read_text())['rows'][0]
# C0 identity across the whole interval
assert c0['generation']['token_ids'] == c0['base_generation']['token_ids'], 'C0 interval not identity'
assert all(r['perturbation_norm'] == 0.0 for r in c0['intervention_record'].values())
# multi-site: EVERY interval layer hooked and edited
rec = iv['intervention_record']
assert sorted(int(k) for k in rec) == [1, 2, 3, 4, 5], f'sites: {list(rec)}'
for k, r in rec.items():
    assert r['perturbation_norm'] > 0, f'layer {k} did not edit'
    assert r['decode_steps'] == len(iv['generation']['token_ids']) - 1
# correct layer->donor mapping: per-layer donor state norms must DIFFER across layers
pl = iv['persistence']['per_layer_donor_norms']
norms = {L: v['donor_state_norms']['1'] for L, v in pl.items()}
assert len(set(round(v, 3) for v in norms.values())) == 5, f'donor states identical across layers? {norms}'
# final selected-layer coverage: the last interval layer (5) recorded decode calls
assert rec['5']['decode_steps'] == len(iv['generation']['token_ids']) - 1
print('SMOKE PASS interval: 5/5 tiny sites edited, C0 identity, per-layer donor mapping varies, final-layer coverage')
PY
