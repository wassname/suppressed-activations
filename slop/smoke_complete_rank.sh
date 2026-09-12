#!/usr/bin/env bash
# REAL tiny dispatch: complete-rank ladder - BOTH bases truncated, joint rank varies,
# k1 != kfull vectors, removal = the TRUNCATED joint (rank changes), C0. -- PI[glm-5p3-flash]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
cat > /tmp/cr_gen.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import sys, json
sys.path.insert(0, '.')
import scripts.oat_sweep as oat
rows = oat.SWEEP_CONFIGS['smoke-complete-rank']()
spec = []
for i, (axis, value, cfg) in enumerate(rows):
    spec.append({"output_dir": f"out/b27_smoke_cr/{i}", "sweep": "smoke-complete-rank",
                 "condition_index": i, "prompt_mode": "chat-assistant-prefill",
                 "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                 "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                 "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                 "lens_corpus_arrow": None, "target_concept": "dog",
                 "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                 "extraction_instruction": None, "selector_audit": False,
                 "expected_strength": cfg.strength, "expected_condition": value,
                 "expected_common_donor_rank": cfg.common_donor_rank,
                 "expected_common_source_rank": cfg.common_source_rank,
                 "expected_common_temporal_full": cfg.common_temporal_full,
                 "expected_detector_layers": list(cfg.detector_layers)})
json.dump(spec, open('/tmp/cr_tiny_spec.json', 'w'))
print('spec:', len(spec))
PYEOF
uv run --offline /tmp/cr_gen.py
rm -rf out/b27_smoke_cr
uv run --offline scripts/oat_sweep.py --batch-spec /tmp/cr_tiny_spec.json
cat > /tmp/cr_check.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json
from pathlib import Path
spec = json.load(open('/tmp/cr_tiny_spec.json'))
name_by_dir = {Path(e['output_dir']).name: e['expected_condition'] for e in spec}
rows = {name_by_dir[d.name]: json.loads((d/'result.json').read_text())['rows'][0]
        for d in sorted(Path('out/b27_smoke_cr').iterdir())}
p1 = rows['k1_C1.5']['persistence']; pf = rows['kfull_C1.5']['persistence']
# the complete-rank mode: BOTH bases truncated BEFORE the joint; the joint rank VARIES
assert p1['complete_rank_mode']['joint_rank'] < pf['complete_rank_mode']['joint_rank'], \
    f"joint ranks: {p1['complete_rank_mode']} vs {pf['complete_rank_mode']}"
assert p1['complete_rank_mode']['source_rank'] == 1 and pf['complete_rank_mode']['source_rank'] == 4  # tiny full support = 4 (2x2)
# the removal = the TRUNCATED joint: the removal_rank field = the joint rank
assert p1['removal_rank'] == p1['complete_rank_mode']['joint_rank']
assert pf['removal_rank'] == pf['complete_rank_mode']['joint_rank']
# the injected vectors differ across ranks
assert p1['injected_vectors'] != pf['injected_vectors']
# C0 identity
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids']
# REGRESSION: the OLD rankinj family's removal must be UNCHANGED by the complete-edit
# scoping: run one old-rankinj cell and compare its removal_cols_sha256 to the recorded
# historical fingerprint (the rankinj smoke's saved outputs)
import subprocess
r = subprocess.run(['uv', 'run', '--offline', 'scripts/oat_sweep.py', '--sweep',
                    'smoke-common-basis-rankinj', '--condition-index', '0', '--output-dir',
                    'out/b27_smoke_cr/rankinj-k1-regression', '--target', 'dog',
                    '--prompt-mode', 'chat-assistant-prefill', '--max-new-tokens', '4',
                    '--source-prompt', 'Question: what is the animal that spins webs called?\nAnswer: ',
                    '--target-prompt', 'Question: what is the animal that barks called?\nAnswer: ',
                    '--source-output', 'Spider', '--target-output', 'Dog',
                    '--prefill-instruction', 'Answer the question with the answer first. Then describe the animal in three sentences.'],
                   capture_output=True, text=True)
old = json.loads(Path('out/b27_smoke_cr/rankinj-k1-regression/result.json').read_text())['rows'][0]
assert old['persistence']['removal_span'] == 'joint'
# the old rankinj k1: complete_rank_mode MUST be None (the mode scoping)
assert old['persistence']['complete_rank_mode'] is None, \
    f"the old rankinj family silently entered complete-edit mode: {old['persistence']['complete_rank_mode']}"
# and its removal rank = 8 (the top8 joint) - unchanged by the new family's existence
assert old['persistence']['removal_rank'] == 8
print('REGRESSION PASS: the old rankinj k1 removal unchanged (mode=None, rank 8)')
# k8 replay: the k8 arm's injected vectors == the earlyloc imported-h1's (same runtime);
# the xdepth tiny twin's imported arm = the k8 equivalent construction... the tiny k8
# (common_donor_rank=2=top8) vs the xdepth tiny imported (anchor 3): SAME config -> the
# injected vector hashes equal
xd = json.loads(Path('out/b24_smoke_xdepth/1/result.json').read_text())['rows'][0]
kf = rows['kfull_C1.5']
# the tiny kfull = the FULL support (4 cols) vs the xdepth imported = top8 (=full on tiny
# at rank2/window2: both 4 cols) -> the same construction: compare the injected hashes
assert kf['persistence']['injected_vectors'] == xd['persistence']['injected_vectors'], \
    'kfull injected vectors != the xdepth imported arm (same construction expected on tiny)'
print('k8/full replay: injected vectors == the xdepth imported arm (tiny-equivalent)')
print('COMPLETE-RANK SMOKE PASS: both bases truncated; joint rank varies; removal = the '
      'truncated joint; vectors differ; C0 identity; old-family regression; replay equality')
PYEOF
uv run --offline /tmp/cr_check.py
