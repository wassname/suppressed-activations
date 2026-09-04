figure:
    uv run scripts/figure.py

check:
    uv run scripts/figure.py
    uv run --with torch python -m py_compile suppressed_activation_subspace.py scripts/figure.py
