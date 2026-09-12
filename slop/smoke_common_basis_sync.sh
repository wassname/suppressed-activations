#!/usr/bin/env bash
# Tiny smoke: sync-donor common_replace — mapping, equal token-ID histories, C0 both paths,
# bitwise prefill equality between frozen and sync arms. -- PI[claude]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
rm -rf out/b16_smoke_sync
SRC=$'Question: what is the animal that spins webs called?\nAnswer: '
INSTR='Answer the question with the answer first. Then describe the animal in three sentences.'
DOG=$'Question: what is the animal that barks and is called man'"'"'s best friend called?\nAnswer: '
uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-sync --condition-index 0 \
  --output-dir out/b16_smoke_sync/sync --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-sync --condition-index 1 \
  --output-dir out/b16_smoke_sync/C0_sync --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
uv run --offline scripts/oat_sweep.py --sweep smoke-common-basis-sync --condition-index 2 \
  --output-dir out/b16_smoke_sync/frozen --target dog --prompt-mode chat-assistant-prefill \
  --max-new-tokens 4 --source-prompt "$SRC" --target-prompt "$DOG" \
  --source-output Spider --target-output Dog --prefill-instruction "$INSTR"
python3 - <<'PY'
import json, hashlib
from pathlib import Path
root = Path('out/b16_smoke_sync')
fz = json.loads((root/'frozen/result.json').read_text())['rows'][0]
sy = json.loads((root/'sync/result.json').read_text())['rows'][0]
c0 = json.loads((root/'C0_sync/result.json').read_text())['rows'][0]
# C0 sync identity
assert c0['generation']['token_ids'] == c0['base_generation']['token_ids'], 'C0 sync not identity'
# bitwise prefill construction check: frozen vs sync steered first-step logits identical
assert fz['first_logits_sha256']['steered'] == sy['first_logits_sha256']['steered'], 'prefill logits differ between arms'
assert fz['generation']['token_ids'][0] == sy['generation']['token_ids'][0], 'first token differs'
# histories equal + donor conditioning recorded
rec = list(sy['intervention_record'].values())[0]
hist = rec['synchronized_history']
assert hist['source_tokens'] == hist['donor_tokens']
assert 'source-selected tokens' in hist['donor_conditioning']
# sync edited (strength 1.5)
assert rec['perturbation_norm'] > 0
# decode coverage
assert rec['decode_steps'] == len(sy['generation']['token_ids']) - 1
print('SMOKE PASS sync: C0 identity, bitwise prefill equality, equal histories, coverage')
PY
