"""Rebuild both leaderboards from published per-prompt evidence, without a model. — PI/OpenAI"""
import argparse
import gzip
import json
import os
from pathlib import Path
from statistics import mean

from tabulate import tabulate

from unspoken_concepts.metrics import delta_ci, f1, f1_ci

ROOT = Path(__file__).resolve().parents[2]
CONTROLS = {"mean over layers", "random subspace", "mean calibration text", "logit lens, best layer"}


def summarize(evidence):
    rows, methods = evidence["rows"], evidence["methods"]
    assert set(methods) == {r["transform"] for r in rows}
    base = [r for r in rows if r["transform"] == "random subspace" and r["role"] == "test"]
    keys = {(r["split"], r["word"]) for r in base}
    assert len(keys) == len(base) > 0
    result = []
    for name, method in methods.items():
        samples = [r for r in rows if r["transform"] == name and r["role"] == "test"]
        assert len(samples) == len(keys) and {(r["split"], r["word"]) for r in samples} == keys
        result.append(dict(name=name, **method, n=len(samples), f1=f1(samples), ci=f1_ci(samples),
                           delta="" if name in {"random subspace"} else delta_ci(samples, base),
                           found=mean(r["hidden"] for r in samples), leaked=mean(r["leaked"] for r in samples)))
    return sorted(result, key=lambda r: -r["f1"])


def tables(evidence, evidence_link):
    rows = summarize(evidence)
    geometry, unrestricted, detailed = [], [], []
    for row in rows:
        label = f'[{row["name"]}]({row["code"]} "{row["about"]}")'
        if row["name"] in CONTROLS:
            label = f"*{label}*"
        best = max(r["f1"] for r in rows if r["kind"] == row["kind"])
        value = f'{row["f1"]:.2f}'
        if row["f1"] == best:
            value = f"**{value}**"
        score = f'{value} ({row["ci"]})'
        if row["kind"] == "geometry":
            geometry.append({"method": label, "by": row["author"], "F1↑ (90% CI)": score})
        else:
            assert row["kind"] == "unrestricted"
            unrestricted.append({"method": label, "F1↑ (90% CI)": score,
                                 "external data": row["external_data"], "fitting / training": row["training"],
                                 "other extras": row["extras"]})
        detailed.append({"method": label, "F1↑ (90% CI)": score, "Δ vs random": row["delta"],
                         "found↑": f'{row["found"]:.0%}', "leaked↓": f'{row["leaked"]:.0%}',
                         "fitted on": row["fitted"], "kind": row["kind"]})
    render = lambda rs: tabulate(rs, headers="keys", tablefmt="pipe", disable_numparse=True)
    n = rows[0]["n"]
    caption = (f"Scored on {n} translation prompts. Brackets show 90% bootstrap intervals over prompts. "
               "Hover over a method for its description.")
    unrestricted_note = ("Same prompts and F1 as geometry-only; additional resources are listed per method. "
                         "External data means data beyond the supplied calibration texts and base model. "
                         "Published J-lens matrices were fitted on WikiText; their pinned source is in the evidence. "
                         "These are the previously reported reference results, not new runs.")
    detail = ("# Leaderboards\n\n## Geometry-only\n\n" + render(geometry) + "\n\n" + caption +
              "\n\n## Unrestricted methods\n\n" + render(unrestricted) + "\n\n" + unrestricted_note +
              "\n\n## Diagnostic scores\n\n" + render(detailed) +
              "\n\nF1 = 2TP / (2TP + FP + FN). Found is TP; leaked is input-or-output FP. "
              "A prompt can count as both. Δ is the paired F1 difference from random projection.\n\n" +
              f"[Per-prompt evidence and provenance]({evidence_link}). " +
              f"Source run: `{evidence['provenance']['source_run']}`, " +
              f"source commit: `{evidence['provenance']['source_commit']}`.\n")
    return render(geometry), render(unrestricted), caption, unrestricted_note, detail


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", nargs="?", type=Path, default=ROOT / "results/leaderboard.json.gz")
    args = parser.parse_args()
    with gzip.open(args.evidence, "rt") as f:
        evidence = json.load(f)
    link = Path(os.path.relpath(args.evidence, ROOT / "docs/leaderboard")).as_posix()
    geometry, unrestricted, caption, note, detail = tables(evidence, link)
    includes = ROOT / "docs/readme/includes"
    includes.mkdir(parents=True, exist_ok=True)
    for name, content in (("geometry", geometry), ("unrestricted", unrestricted), ("caption", caption),
                          ("unrestricted_caption", note)):
        (includes / f"{name}.md").write_text(content + "\n")
    (ROOT / "docs/leaderboard/README.md").write_text(detail)
    print(f"Rebuilt both leaderboards from {args.evidence}")


if __name__ == "__main__":
    main()
