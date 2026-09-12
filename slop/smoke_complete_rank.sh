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
print('COMPLETE-RANK SMOKE PASS: both bases truncated; joint rank varies (k1 < kfull); '
      'removal = the truncated joint; vectors differ; C0 identity')
PYEOF
uv run --offline /tmp/cr_check.py
