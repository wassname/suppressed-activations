#!/usr/bin/env bash
# REAL tiny batch-dispatch: validate_specs + metadata stripping + both selectors/site/C0
# through the runner's actual __main__ path (tiny model, CPU). -- PI[glm-5p3-flash]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
cat > /tmp/selsite_spec_gen.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import sys
sys.path.insert(0, '.')
import scripts.oat_sweep as oat
import json
rows = oat.SWEEP_CONFIGS['smoke-common-basis-selsite']()
print('tiny twin rows:', [(v, c.intervention_layer, c.common_selector) for _, v, c in rows])
spec = []
for i, (axis, value, cfg) in enumerate(rows):
    spec.append({"output_dir": f"out/b23_smoke_selsite/{i}", "sweep": "smoke-common-basis-selsite",
                 "condition_index": i, "prompt_mode": "chat-assistant-prefill",
                 "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                 "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                 "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                 "lens_corpus_arrow": None, "target_concept": "dog",
                 "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                 "extraction_instruction": None, "selector_audit": False,
                 "expected_strength": cfg.strength, "expected_condition": value,
                 "expected_detector_layers": list(cfg.detector_layers)})
json.dump(spec, open('/tmp/selsite_tiny_spec.json', 'w'))
print('tiny spec written:', len(spec), 'entries')
PYEOF
uv run --offline /tmp/selsite_spec_gen.py
rm -rf out/b23_smoke_selsite
uv run --offline scripts/oat_sweep.py --batch-spec /tmp/selsite_tiny_spec.json
cat > /tmp/selsite_check.py <<'PYEOF'
import json
from pathlib import Path
for i, d in enumerate(sorted(Path('out/b23_smoke_selsite').iterdir())):
    r = json.load(open(d/'result.json'))['rows'][0]
    print(i, d.name, 'strength', r['config']['strength'], 'sel', r['config']['common_selector'],
          'layer', r['config']['intervention_layer'][0])
PYEOF
uv run --offline /tmp/selsite_check.py
