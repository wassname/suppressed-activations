demo: notebook-run

demo-check: test
    uv run scripts/demo_check.py
    uv run scripts/figure.py

test:
    uv run --with torch --with numpy python -m scripts.test

notebook:
    uv run jupytext --sync nbs/demo.py

notebook-smoke:
    mkdir -p .local
    SUPPRESSED_ROOT=$PWD SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random \
    SUPPRESSED_REVISION=main SUPPRESSED_DEVICE=cpu SUPPRESSED_EARLY_LAYER=0 \
    SUPPRESSED_PEAK_LAYER=2 SUPPRESSED_OUTPUT_LAYER=5 \
    SUPPRESSED_INTERVENTION_LAYER=3 SUPPRESSED_RANK=2 SUPPRESSED_STRENGTH=0.125 \
    SUPPRESSED_TOKENS=4 \
    uv run jupytext --to ipynb --execute nbs/demo.py -o .local/demo-smoke.ipynb

notebook-run:
    SUPPRESSED_ROOT=$PWD uv run jupytext --to ipynb --execute nbs/demo.py -o nbs/demo.ipynb
    uv run scripts/notebook_check.py

notebook-check:
    uv run scripts/notebook_check.py

figure:
    uv run scripts/figure.py

intervention-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_intervention-sweep"
    uv run scripts/delayed_readout.py --sweep --output-dir "$output_dir"

intervention-sweep-union:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_intervention-sweep-union"
    uv run scripts/delayed_readout.py --sweep --aggregation union --output-dir "$output_dir"

oat-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_oat-sweep"
    uv run scripts/oat_sweep.py --output-dir "$output_dir"

causal-demo:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_causal-demo"
    uv run scripts/oat_sweep.py --sweep demo --prompt-mode raw --output-dir "$output_dir"

normalization-strength-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_normalization-strength-sweep"
    uv run scripts/oat_sweep.py --sweep normalization-strength --output-dir "$output_dir"

lexical-surface-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_lexical-surface-sweep"
    uv run scripts/oat_sweep.py --sweep lexical-surface --output-dir "$output_dir"

layer-position-strength-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_layer-position-strength-sweep"
    uv run scripts/oat_sweep.py --sweep layer-position-strength --output-dir "$output_dir"

layer-combo-sweep prompt_mode="chat-fact":
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_layer-combo-{{prompt_mode}}"
    uv run scripts/oat_sweep.py --sweep layer-combo --prompt-mode "{{prompt_mode}}" --output-dir "$output_dir"

persistent-generation-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_persistent-generation-chat-fact"
    uv run scripts/oat_sweep.py --sweep persistent-generation --prompt-mode chat-fact --output-dir "$output_dir"

persistent-direction-sweep:
    #!/usr/bin/env bash
    set -euo pipefail
    output_dir="out/$(date +%Y-%m-%d_%H%M%S)_persistent-direction-raw"
    uv run scripts/oat_sweep.py --sweep persistent-direction --prompt-mode raw --output-dir "$output_dir"

results:
    uv run scripts/results.py

check: test demo-check
    uv run --with torch python -m py_compile suppressed_activation_subspace.py scripts/*.py
