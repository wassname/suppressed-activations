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

check: test demo-check
    uv run --with torch python -m py_compile suppressed_activation_subspace.py scripts/*.py
