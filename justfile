demo:
    uv run scripts/demo.py
    uv run scripts/figure.py

demo-check: test
    uv run scripts/demo_check.py
    uv run scripts/figure.py

test:
    uv run --with torch python -m scripts.test

figure:
    uv run scripts/figure.py

check: test demo-check
    uv run --with torch python -m py_compile suppressed_activation_subspace.py scripts/*.py
