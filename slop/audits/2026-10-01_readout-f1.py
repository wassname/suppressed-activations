"""Per-prompt precision/recall/F1@32 of saved top-32 readouts against lexical alias labels. — PI/OpenAI
Labels use the repository prefix rule on the saved aliases only; translations/synonyms not listed count as false positives."""
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

from tabulate import tabulate
from transformers import AutoTokenizer

RUNS = {"English v3 (16)": "out/2026-09-30_125330_jlens-one-pass",
        "English v4 non-geography (8)": "out/2026-09-30_142814_jlens-one-pass",
        "translation (48)": "out/2026-09-30_125500_jlens-one-pass"}
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", local_files_only=True)
vocab = [tok.decode([i]) for i in range(len(tok))]


def hit(token, word):  # same rule as q.is_prefix_hit
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


def labelled(words):
    return {i for i, v in enumerate(vocab) if any(hit(v, w) for w in words)}


rows = []
for name, run in RUNS.items():
    for r in json.loads((Path(run) / "readout.json").read_text()):
        hidden_words = r["hidden_aliases"]
        said_words = sorted(set(r["answer_aliases"]) | set(r["actual_words"])) if r["intended_answer_observed"] else r["actual_words"]
        top = r["top32"]
        tp = sum(any(hit(t, w) for w in hidden_words) for t in top)
        said = sum(any(hit(t, w) for w in said_words) for t in top)
        n_label = len(labelled(hidden_words))
        precision, recall = tp / len(top), tp / n_label
        rows.append(dict(set=name, method=r["method"], concept=r["concept"], precision=precision, recall=recall,
                         f1=0.0 if tp == 0 else 2 * precision * recall / (precision + recall),
                         said_fraction=said / len(top), found=tp > 0, found_and_unsaid=tp > 0 and said == 0, n_label=n_label))
with open("slop/audits/2026-10-01_readout-f1.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
groups = defaultdict(list)
for r in rows:
    groups[r["set"], r["method"]].append(r)
summary = [dict(set=s, method=m, **{"F1@32": mean(r["f1"] for r in g), "P@32": mean(r["precision"] for r in g),
                "R@32": mean(r["recall"] for r in g), "said frac": mean(r["said_fraction"] for r in g),
                "found∧unsaid": sum(r["found_and_unsaid"] for r in g), "n": len(g)}) for (s, m), g in groups.items()]
summary.sort(key=lambda r: (r["set"], -r["F1@32"]))
print(tabulate(summary, headers="keys", tablefmt="pipe", floatfmt=".3f"))
