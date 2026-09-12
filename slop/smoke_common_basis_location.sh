#!/usr/bin/env bash
# Tiny real-path smoke: location family (hook index + identity + persistence diagnostic). -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b15_smoke_location
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
# tiny twin of the location family: 5-layer model, h_0..h_5, blocks 0..4;
# locations L1 (early) and L5 (final residual); top8_union == full union at rank2/window2
run_spec () {
  uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-loc --condition-index "$1" \
    --output-dir "out/b15_smoke_location/$2" --target dog --prompt-mode chat-assistant-prefill \
    --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
    --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
}
run_spec 0 L1_top8
run_spec 1 L1_rand
run_spec 2 L5_top8
run_spec 3 L5_rand
run_spec 4 C0
python3 - <<'PY'
import json
from pathlib import Path
root = Path('out/b15_smoke_location')
rows = {n: json.loads((root / n / 'result.json').read_text())['rows'][0]
        for n in ('L1_top8', 'L1_rand', 'L5_top8', 'L5_rand', 'C0')}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# C0 identity
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids']
assert rec['C0']['perturbation_norm'] == 0.0
for n, r in rows.items():
    if n == 'C0':
        continue
    layer = r['config']['intervention_layer'][0]
    hooked = list(r['intervention_record'].keys())
    # intervention_record is keyed by RESIDUAL layer (= intervention_layer); the hooked block is layer-1
    assert [int(k) for k in hooked] == [layer], f'{n}: hook indexed residual layer {hooked}, expected [{layer}]'
    assert rec[n]['perturbation_norm'] > 0, f'{n} did not edit'
    assert rec[n]['decode_steps'] == len(r['generation']['token_ids']) - 1
    dp = r['persistence']['downstream_persistence_prefill']
    assert dp['final_residual_layer'] == 5  # tiny final residual index
    assert dp['edited_minus_clean_rel'] >= 0 and dp['P_edited_minus_clean_rel'] >= 0
    assert dp['clean_norm'] > 0
    print(f"{n}: layer {layer}, edit rel {dp['edited_minus_clean_rel']:.3f}, P-rel {dp['P_edited_minus_clean_rel']:.3f}")
print('SMOKE PASS location family: hook indices, C0 identity, both persistence norms')
PY
