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
    result = json.loads((root / "result.json").read_text())
    rows = sorted(
        [frontmatter(path) for path in (root / "conditions").glob("*/run.md")],
        key=lambda row: row["swap_log_odds_shift"], reverse=True,
    )
    source_output = rows[0]["source_output"]
    target_output = rows[0]["target_output"]
    table = tabulate(
        [[
            f'[{row["condition_id"]}]({row["log"]})',
            f'{row["swap_log_odds_shift"]:+.3f}',
            f'{row["p_target"]:.4f}', f'{row["p_source"]:.4f}',
            f'{row["valid_answer_mass"]:.3f}',
            f'{row["repeated_bigram_fraction"]:.3f}', repr(row["first_token"]),
            "N/A" if row["readout_overlap"] is None else f'{row["readout_overlap"]:.3f}',
        ] for row in rows],
        headers=[
            "condition", "swap log-odds↑", f"p({target_output})↑", f"p({source_output})↓",
            f"p({target_output})+p({source_output}) ↑",
            "repeat bigrams↓", "first token", "donor readout overlap↑",
        ],
        tablefmt="pipe",
        disable_numparse=True,
    )
    report = f"""---
conditions: {len(rows)}
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `{result['model']}` at revision `{result['revision']}`.
Code: `{result['git']}`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

{table}

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
"""
    (root / "run.md").write_text(report)
    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path)
    args = parser.parse_args()
    if args.root is None:
        candidates = sorted(
            [path.parent for path in Path("out").glob("*/conditions")
             if (path.parent / "result.json").exists()],
            key=lambda path: (path / "result.json").stat().st_mtime,
        )
        if not candidates:
            raise FileNotFoundError("no completed condition sweep in out/")
        args.root = candidates[-1]
    main(args.root)
