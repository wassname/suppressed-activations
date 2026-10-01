"""F1@k for k=1..32 from the ordered saved top-32 lists (same labels as readout-f1). — PI/OpenAI"""
import json
from functools import cache
from pathlib import Path
from statistics import mean

from tabulate import tabulate
from transformers import AutoTokenizer

RUNS = {"v3": "out/2026-09-30_125330_jlens-one-pass", "v4": "out/2026-09-30_142814_jlens-one-pass",
        "translation": "out/2026-09-30_125500_jlens-one-pass"}
METHODS = ["end-pass plain27", "end-pass J-lens", "end-pass erased0.5 J-lens", "rise-and-fall masked"]
KS = [1, 2, 4, 8, 16, 32]
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", local_files_only=True)
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(248320)))]


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


@cache
def n_labelled(words):
    return sum(any(hit(v, w) for w in words) for v in vocab)


extra = json.loads(Path("slop/audits/2026-10-01_rise-fall-readout.json").read_text())["rows"]
table = []
for name, run in RUNS.items():
    rows = json.loads((Path(run) / "readout.json").read_text()) + [r for r in extra if r["run"] == run]
    for method in METHODS:
        sel = [r for r in rows if r["method"] == method]
        line = {"set": name, "method": method, "n": len(sel)}
        for k in KS:
            f1s = []
            for r in sel:
                tp = sum(any(hit(t, w) for w in r["hidden_aliases"]) for t in r["top32"][:k])
                p, rec = tp / k, tp / n_labelled(tuple(r["hidden_aliases"]))
                f1s.append(0.0 if tp == 0 else 2 * p * rec / (p + rec))
            line[f"F1@{k}"] = mean(f1s)
        table.append(line)
print(tabulate(table, headers="keys", tablefmt="pipe", floatfmt=".3f"))
