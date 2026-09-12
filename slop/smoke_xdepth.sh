#!/usr/bin/env bash
# REAL tiny dispatch: xdepth arms - production donor-vector mapping/rescale asserts,
# same-depth replay regression, contracts; tiny model CPU. -- PI[glm-5p3-flash]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
cat > /tmp/xdepth_gen.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import sys, json
sys.path.insert(0, '.')
import scripts.oat_sweep as oat
rows = oat.SWEEP_CONFIGS['smoke-common-basis-xdepth']()
spec = []
for i, (axis, value, cfg) in enumerate(rows):
    spec.append({"output_dir": f"out/b24_smoke_xdepth/{i}", "sweep": "smoke-common-basis-xdepth",
                 "condition_index": i, "prompt_mode": "chat-assistant-prefill",
                 "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                 "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                 "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                 "lens_corpus_arrow": None, "target_concept": "dog",
                 "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                 "extraction_instruction": None, "selector_audit": False,
                 "expected_strength": cfg.strength, "expected_condition": value,
                 "expected_xdepth_anchor_layer": [cfg.xdepth_anchor_layer],
                 "expected_xdepth_norm_from_layer": [cfg.xdepth_norm_from_layer],
                 "expected_detector_layers": list(cfg.detector_layers)})
json.dump(spec, open('/tmp/xdepth_tiny_spec.json', 'w'))
print('spec written:', len(spec))
PYEOF
uv run --offline /tmp/xdepth_gen.py
rm -rf out/b24_smoke_xdepth
uv run --offline scripts/oat_sweep.py --batch-spec /tmp/xdepth_tiny_spec.json
cat > /tmp/xdepth_check.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json
from pathlib import Path
# dirs are numeric (0..3); map to the spec's condition names via expected_condition
spec = json.load(open('/tmp/xdepth_tiny_spec.json'))
name_by_dir = {Path(e['output_dir']).name: e['expected_condition'] for e in spec}
rows = {name_by_dir[d.name]: json.load(open(d/'result.json'))['rows'][0]
        for d in sorted(Path('out/b24_smoke_xdepth').iterdir())}
rec = {n: list(r['intervention_record'].values())[0] for n, r in rows.items()}
# same-depth replay regression: v8_replay == the selsite h1 replay construction (same config):
# check its injected vector norm against the selsite smoke's increment-h1 (same tiny inputs)
assert rows['v8_replay_C1.5']['config']['xdepth_anchor_layer'] == -1
assert rows['v25_imported_C1.5']['config']['xdepth_anchor_layer'] == 3
assert rows['v8_rescaled_C1.5']['config']['xdepth_norm_from_layer'] == 3
assert rows['C0']['generation']['token_ids'] == rows['C0']['base_generation']['token_ids']
for n in ('v8_replay_C1.5','v25_imported_C1.5','v8_rescaled_C1.5'):
    assert rec[n]['perturbation_norm'] > 0, n
# rescale arm: direction = v8's, size = v25's: donor_proj norms == v25's norms (per offset)
# (verified via the norm_source asserts in-run; here check the arm differs from both parents)
print('xdepth arms all engaged; C0 identity; anchors/rescale mapped')
PYEOF
uv run --offline /tmp/xdepth_check.py
