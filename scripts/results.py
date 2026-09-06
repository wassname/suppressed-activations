# /// script
# requires-python = ">=3.12"
# dependencies = ["tabulate>=0.9"]
# ///
"""Build an OAT sweep table from condition run.md frontmatter. Written by Codex/gpt-5.6-sol."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tabulate import tabulate


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path}")
    block = text.split("---\n", 2)[1]
    return {
        key: json.loads(value)
        for line in block.splitlines()
        for key, value in [line.split(": ", 1)]
    }


def main(root: Path) -> None:
    rows = [frontmatter(path) for path in sorted((root / "conditions").glob("*/run.md"))]
    table = tabulate(
        [[
            row["axis"], row["value"], "yes" if row["is_default"] else "",
            f'{row["swap_log_odds_shift"]:+.3f}', f'{row["valid_answer_mass"]:.3f}',
            f'{row["repeated_bigram_fraction"]:.3f}', repr(row["first_token"]),
            f'{row["readout_overlap"]:.3f}', f'[{row["condition_id"]}]({row["log"]})',
        ] for row in rows],
        headers=[
            "axis", "value", "default", "swap log-odds ↑", "p(4)+p(8) ↑",
            "repeat bigrams ↓", "first token", "donor readout overlap ↑", "log",
        ],
        tablefmt="pipe",
        disable_numparse=True,
    )
    report = f"""---
conditions: {len(rows)}
metric: "swap_log_odds_shift"
---

# One-at-a-time intervention sweep

Each section varies one axis while all other values stay at the single default. Rows are in
enumeration order, not sorted by outcome. Each log contains the exact prompt, readouts,
top-token distribution, and generated continuation.

{table}

-- Codex/gpt-5.6-sol
"""
    (root / "run.md").write_text(report)
    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path)
    args = parser.parse_args()
    if args.root is None:
        candidates = sorted(Path("out").glob("*_oat-sweep"))
        if not candidates:
            raise FileNotFoundError("no out/*_oat-sweep directory")
        args.root = candidates[-1]
    main(args.root)
